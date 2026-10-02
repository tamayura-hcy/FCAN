# FCAN 最良結果記録（best）

- データプロトコル：`--cell_split CELL_split_2025`
- シード：固定 `[42, 123, 777, 2024, 3407]`（論文の全結果はこの5つの固定シードを使用し、結果による選別は行っていません）
- 主要指標：**EMA 教師の固定エポック acc**（`--final_metric ema`、デフォルト）
- シードあたり実行回数：`-i 1`
- データソース：`best/SUMMARY.txt`（最良設定×5シードのバッチ、全10指標）

---

## 1. タスクごとの最良設定と精度

| タスク | ソースエポック es | ターゲットエポック et | EMA acc（5シード平均±標準偏差） | 備考 |
|---|---|---|---|---|
| **A-B** (BOE→TMI) | **5** | **8** | **0.9558 ± 0.0153** | 低周波増強 P070A20（`--src_ll_prob 0.7 --src_ll_alpha 2.0`） |
| **A-C** (BOE→CELL) | **4** | **15** | **0.8774 ± 0.0245** | 追加ハイパーパラメータ `--lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01` |
| **B-C** (TMI→CELL) | **8** | **15** | **0.9212 ± 0.0101** | 追加ハイパーパラメータ `--lambda_caco 0.01 --lambda_batch_ang 0.5` |

---

## 2. シードごとの内訳（et エポック時点の EMA acc）

### A-B（es=5, et=8, P070A20：src_ll_prob=0.7, src_ll_alpha=2.0）

| シード | EMA acc |
|---|---|
| 42 | 0.9641 |
| 123 | 0.9499 |
| 777 | 0.9314 |
| 2024 | 0.9662 |
| 3407 | 0.9673 |
| **平均** | **0.9558** |

### A-C（es=4, et=15, 最終エポック）

| シード | EMA acc（第15エポック） |
|---|---|
| 42 | 0.8943 |
| 123 | 0.8638 |
| 777 | 0.8961 |
| 2024 | 0.8405 |
| 3407 | 0.8925 |
| **平均** | **0.8774** |

### B-C（es=8, et=15, λ_caco=0.01, λ_batch_ang=0.5）

| シード | EMA acc |
|---|---|
| 42 | 0.9158 |
| 123 | 0.9176 |
| 777 | 0.9176 |
| 2024 | 0.9158 |
| 3407 | 0.9391 |
| **平均** | **0.9212** |

---

## 3. 最終実験コマンド設定（3タスク×5シード＝15ラン）

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

## 4. 補足

- 全10指標（acc/auc/recall/precision/f1/bacc/specificity/kappa/gmean/mcc、平均±標準偏差）は `best/SUMMARY.txt`、集計表は `comparison_results_summary.md` を参照。
- 一括自動実行には `run_final_fea.py` を利用可能（上記設定に合わせて更新すること）。
