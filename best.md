# FCAN 最优结果记录（best）

- 数据协议：`--cell_split CELL_split_2025`
- 种子：固定 `[42, 123, 777, 2024, 3407]`（论文全部结果均用这 5 个固定种子，不按结果筛选）
- 主指标：**EMA 教师固定轮 acc**（`--final_metric ema`，默认）
- 每种子运行次数：`-i 1`
- 数据来源：`best/SUMMARY.txt`（三任务最优方案 × 5 种子跑批，完整 10 指标）

---

## 一、每任务最优配置与精度

| 任务 | 源域轮 es | 目标域轮 et | EMA acc（5 种子 mean ± std） | 说明 |
|---|---|---|---|---|
| **A-B** (BOE→TMI) | **5** | **8** | **0.9558 ± 0.0153** | 低频增广 P070A20（`--src_ll_prob 0.7 --src_ll_alpha 2.0`） |
| **A-C** (BOE→CELL) | **4** | **15** | **0.8774 ± 0.0245** | 附加超参 `--lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01` |
| **B-C** (TMI→CELL) | **8** | **15** | **0.9212 ± 0.0101** | 附加超参 `--lambda_caco 0.01 --lambda_batch_ang 0.5` |

---

## 二、per-seed 明细（et 轮处 EMA acc）

### A-B（es=5, et=8，P070A20：src_ll_prob=0.7, src_ll_alpha=2.0）
| seed | EMA acc |
|---|---|
| 42 | 0.9641 |
| 123 | 0.9499 |
| 777 | 0.9314 |
| 2024 | 0.9662 |
| 3407 | 0.9673 |
| **mean** | **0.9558** |

### A-C（es=4, et=15，末轮）
| seed | EMA acc（第 15 轮） |
|---|---|
| 42 | 0.8943 |
| 123 | 0.8638 |
| 777 | 0.8961 |
| 2024 | 0.8405 |
| 3407 | 0.8925 |
| **mean** | **0.8774** |

### B-C（es=8, et=15, λ_caco=0.01, λ_batch_ang=0.5）
| seed | EMA acc |
|---|---|
| 42 | 0.9158 |
| 123 | 0.9176 |
| 777 | 0.9176 |
| 2024 | 0.9158 |
| 3407 | 0.9391 |
| **mean** | **0.9212** |

---

## 三、最终实验命令配置（3 任务 × 5 seeds = 15 run）

### A-B
```bash
python main.py --only BOE->TMI -es 5 -et 8 --seed 42  -i 1 --cell_split CELL_split_2025 --src_ll_prob 0.7 --src_ll_alpha 2.0
python main.py --only BOE->TMI -es 5 -et 8 --seed 123 -i 1 --cell_split CELL_split_2025 --src_ll_prob 0.7 --src_ll_alpha 2.0
python main.py --only BOE->TMI -es 5 -et 8 --seed 777 -i 1 --cell_split CELL_split_2025 --src_ll_prob 0.7 --src_ll_alpha 2.0
python main.py --only BOE->TMI -es 5 -et 8 --seed 2024 -i 1 --cell_split CELL_split_2025 --src_ll_prob 0.7 --src_ll_alpha 2.0
python main.py --only BOE->TMI -es 5 -et 8 --seed 3407 -i 1 --cell_split CELL_split_2025 --src_ll_prob 0.7 --src_ll_alpha 2.0
```

### A-C
```bash
python main.py --only BOE->CELL -es 4 -et 15 --seed 42  -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01
python main.py --only BOE->CELL -es 4 -et 15 --seed 123 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01
python main.py --only BOE->CELL -es 4 -et 15 --seed 777 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01
python main.py --only BOE->CELL -es 4 -et 15 --seed 2024 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01
python main.py --only BOE->CELL -es 4 -et 15 --seed 3407 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01
```

### B-C
```bash
python main.py --only TMI->CELL -es 8 -et 15 --seed 42  -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.5
python main.py --only TMI->CELL -es 8 -et 15 --seed 123 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.5
python main.py --only TMI->CELL -es 8 -et 15 --seed 777 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.5
python main.py --only TMI->CELL -es 8 -et 15 --seed 2024 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.5
python main.py --only TMI->CELL -es 8 -et 15 --seed 3407 -i 1 --cell_split CELL_split_2025 --lambda_caco 0.01 --lambda_batch_ang 0.5
```

---

## 四、备注

- 完整 10 指标（acc/auc/recall/precision/f1/bacc/specificity/kappa/gmean/mcc，mean±std）见 `best/SUMMARY.txt`，汇总表见 `comparison_results_summary.md`。
- 若需批量自动运行，可用 `run_final_fea.py`（按上述配置更新）。
