"""
低频强度扰动：破坏"低频强度=类"捷径（shortcut learning 抑制）。
Low-frequency (LL) strength perturbation: break the "low-frequency strength = class" shortcut.

原理（基于 DWT 域差异诊断）：
  - 域差异/类捷径主要编码在低频（LL 子带）：BOE AMD LL mean=0.459 vs TMI AMD=0.313，
    BOE 内 AMD(0.459)>>NORMAL(0.313) → 模型靠"低频强度"区分 AMD（捷径）。
  - 该捷径在 TMI 失效（TMI AMD≈NORMAL 低频）。
  - 解法：源域训练时随机扰动 LL 子带能量（亮度和对比度），让"低频强度"在源域就不可靠
    → 逼模型改学可迁移的局部形态特征（drusen）。
  （Rationale: the domain shift / class shortcut lives mainly in the LL subband, so perturbing
    LL energy in source training forces the model to learn transferable local morphology instead）

安全保证（Safety guarantees）：
  - 只改 LL（低频）能量；LH/HL/HH（结构边缘）与系数符号（Haar 的"相位"）完全不动
    → 结构位置/形态保留。（Only LL energy changes; LH/HL/HH structure and Haar sign are untouched）
  - 每样本独立随机增益 k=(1+α)^u（指数公式，恒正，α=1 时 k∈[0.5,2]，不会全黑/反相）。

仅对开了 --src_ll_aug 的源域训练生效。
"""
import torch
import torch.nn.functional as F


def haar_dwt2d(x):
    """One-level 2D Haar DWT, stride 2.

    Returns (B, 4, C, H/2, W/2) with sub-bands ordered [LL, LH, HL, HH].
    """
    B, C, H, W = x.shape
    assert H % 2 == 0 and W % 2 == 0, 'Haar DWT requires even H, W'
    w_ll = torch.tensor([[1, 1], [1, 1]], dtype=torch.float32, device=x.device) / 2.0
    w_lh = torch.tensor([[1, -1], [1, -1]], dtype=torch.float32, device=x.device) / 2.0
    w_hl = torch.tensor([[1, 1], [-1, -1]], dtype=torch.float32, device=x.device) / 2.0
    w_hh = torch.tensor([[1, -1], [-1, 1]], dtype=torch.float32, device=x.device) / 2.0
    base = torch.stack([w_ll, w_lh, w_hl, w_hh], dim=0)          # (4, 2, 2)
    weight = base.unsqueeze(0).expand(C, 4, 2, 2).reshape(4 * C, 2, 2).unsqueeze(1)
    out = F.conv2d(x, weight, stride=2, groups=C)                # (B, 4*C, H/2, W/2)
    # 输出通道顺序 [ch0:s0, ch0:s1, ...] → 先拆 (C,4) 再转置为 (4,C)
    out = out.view(B, C, 4, H // 2, W // 2).permute(0, 2, 1, 3, 4)
    return out


def haar_idwt2d_fixed(subbands):
    """One-level 2D Haar iDWT: reconstructs an image from [LL, LH, HL, HH].

    Synthesis kernels (orthonormal Haar, /2 normalization, paired with the stride-2 analysis):
      LL: [[1,1],[1,1]]/2  LH: [[1,-1],[1,-1]]/2  HL: [[1,1],[-1,-1]]/2  HH: [[1,-1],[-1,1]]/2
    """
    B, _, C, h, w = subbands.shape
    device = subbands.device
    LL, LH, HL, HH = subbands[:, 0], subbands[:, 1], subbands[:, 2], subbands[:, 3]

    def _wt(k):
        k = torch.tensor(k, dtype=torch.float32, device=device).view(1, 1, 2, 2)
        return k.expand(C, 1, 2, 2).contiguous()

    w_ll = _wt([[1, 1], [1, 1]]) / 2.0
    w_lh = _wt([[1, -1], [1, -1]]) / 2.0
    w_hl = _wt([[1, 1], [-1, -1]]) / 2.0
    w_hh = _wt([[1, -1], [-1, 1]]) / 2.0

    y_ll = F.conv_transpose2d(LL, w_ll, stride=2, groups=C)
    y_lh = F.conv_transpose2d(LH, w_lh, stride=2, groups=C)
    y_hl = F.conv_transpose2d(HL, w_hl, stride=2, groups=C)
    y_hh = F.conv_transpose2d(HH, w_hh, stride=2, groups=C)
    return y_ll + y_lh + y_hl + y_hh


def ll_strength_augment(x, alpha=0.5, p=0.5, keep_dc=True, clamp_out=True):
    """对一批图像做 DWT LL 子带能量扰动。

    Parameters
    ----------
    x : Tensor (B, C, H, W)，图像张量（通常 [0,1]），H,W 需为偶数
    alpha : float，扰动强度。k = (1+alpha)^u, u~U(-1,1)，k∈[1/(1+α), 1+α]，
        恒为正（不会全黑/反相），乘性对称（×s 与 ÷s 等价）。α=1 → k∈[0.5,2]
    p : float，应用概率（0~1），否则原样返回
    keep_dc : bool
        True  → 只扰动对比度（LL 的 AC 分量缩放），保持整体亮度（DC）[默认]
        False → 亮度和对比度一起扰（破坏"低频强度"捷径更彻底）
    clamp_out : bool，重建后裁剪回原图数值范围（防止溢出）
    """
    if x.dim() != 4:
        raise ValueError('ll_strength_augment expects (B,C,H,W), got {}'.format(tuple(x.shape)))
    B, C, H, W = x.shape
    if H % 2 != 0 or W % 2 != 0:
        return x
    if torch.rand(1).item() > p:
        return x

    sub = haar_dwt2d(x)              # (B, 4, C, H/2, W/2)  [LL, LH, HL, HH]
    LL = sub[:, 0]                   # (B, C, H/2, W/2)

    # 每样本独立随机低频增益（指数公式：恒正，永不退化/反相）
    # k = (1+alpha)^u, u~U(-1,1) → k∈[1/(1+α), 1+α]，乘性对称
    u = 2.0 * torch.rand(B, 1, 1, 1, device=x.device) - 1.0   # U(-1,1)
    k = (1.0 + alpha) ** u                                    # [B,1,1,1]

    if keep_dc:
        # 只缩放 AC（对比度），DC（亮度）保持：LL_new = mean + k*(LL-mean)
        mu = LL.mean(dim=(2, 3), keepdim=True)
        LL_new = mu + k * (LL - mu)
    else:
        # 亮度+对比度一起扰（破坏"低频强度"捷径最彻底）
        LL_new = LL * k

    sub_aug = torch.stack([LL_new, sub[:, 1], sub[:, 2], sub[:, 3]], dim=1)
    x_aug = haar_idwt2d_fixed(sub_aug)  # (B, C, H, W)

    if clamp_out and x_aug.min() >= 0.0 and x_aug.max() <= 1.0:
        x_aug = x_aug.clamp(0.0, 1.0)
    return x_aug


def ll_energy(x):
    """返回 (B,) 每张图的 LL 子带能量（平方均值），用于诊断。"""
    sub = haar_dwt2d(x)
    LL = sub[:, 0]
    return (LL ** 2).mean(dim=(1, 2, 3))
