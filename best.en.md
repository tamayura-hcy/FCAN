# FCAN Best Results Record

- Data protocol: `--cell_split CELL_split_2025`
- Seeds: fixed `[42, 123, 777, 2024, 3407]` (all paper results use these five fixed seeds, no outcome-based filtering)
- Main metric: **EMA-teacher fixed-epoch acc** (`--final_metric ema`, default)
- Runs per seed: `-i 1`
- Data source: `best/SUMMARY.txt` (best configs x 5 seeds, all 10 metrics)

---

## 1. Best config and accuracy per task

| Task | src epochs (es) | tgt epochs (et) | EMA acc (5-seed mean ± std) | Notes |
|---|---|---|---|---|
| **A-B** (BOE→TMI) | **5** | **8** | **0.9558 ± 0.0153** | Low-frequency augmentation P070A20 (`--src_ll_prob 0.7 --src_ll_alpha 2.0`) |
| **A-C** (BOE→CELL) | **4** | **15** | **0.8774 ± 0.0245** | Extra hyperparameters `--lambda_caco 0.01 --lambda_batch_ang 0.001 --alpha_scon 0.01` |
| **B-C** (TMI→CELL) | **8** | **15** | **0.9212 ± 0.0101** | Extra hyperparameters `--lambda_caco 0.01 --lambda_batch_ang 0.5` |

---

## 2. Per-seed details (EMA acc at the et epoch)

### A-B (es=5, et=8, P070A20: src_ll_prob=0.7, src_ll_alpha=2.0)

| seed | EMA acc |
|---|---|
| 42 | 0.9641 |
| 123 | 0.9499 |
| 777 | 0.9314 |
| 2024 | 0.9662 |
| 3407 | 0.9673 |
| **mean** | **0.9558** |

### A-C (es=4, et=15, last epoch)

| seed | EMA acc (epoch 15) |
|---|---|
| 42 | 0.8943 |
| 123 | 0.8638 |
| 777 | 0.8961 |
| 2024 | 0.8405 |
| 3407 | 0.8925 |
| **mean** | **0.8774** |

### B-C (es=8, et=15, λ_caco=0.01, λ_batch_ang=0.5)

| seed | EMA acc |
|---|---|
| 42 | 0.9158 |
| 123 | 0.9176 |
| 777 | 0.9176 |
| 2024 | 0.9158 |
| 3407 | 0.9391 |
| **mean** | **0.9212** |

---

## 3. Final experiment command config (3 tasks x 5 seeds = 15 runs)

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

## 4. Notes

- All 10 metrics (acc/auc/recall/precision/f1/bacc/specificity/kappa/gmean/mcc, mean±std) are in `best/SUMMARY.txt`; the summary table is in `comparison_results_summary.md`.
- For automated batch runs, use `run_final_fea.py` (update it with the configs above).
