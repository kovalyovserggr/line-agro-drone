# runs_index.md

Легкий індекс сирих файлів у `experiments/raw/` (по одному рядку на файл,
без наративу — наратив і трактування результатів див. `RESULTS_LOG.md`).

| Файл | Дата | Команда запуску | T_pm сітка | N реплікацій | Статус |
|---|---|---|---|---|---|
| `raw/pilot_20260911.csv` | 2026-09-11 | `run_parametric_study.py --t-pm 1000 24000 --reps 2 --lim-drones 10 --max-ticks 30000 --seed-base 1000` | {1000, 24000} (крайні точки) | 4 | усі 4 — `timeout_at_max_ticks`; негативний, але інформативний результат — див. DECISIONS.md D8 |
| `raw/pilot_d13_20260911.csv` | 2026-09-11 | `run_parametric_study.py --t-pm 6000 24000 --reps 5 --lim-drones 10 --max-ticks 30000 --n-filament-suppliers 5 --seed-base 1000` | {6000, 24000} | 10 | усі 10 — `timeout_at_max_ticks`; дедлок відсутній (D9-D12 діють), але завершення все ще недосяжне за 3·10⁶с — див. DECISIONS.md D14 |


| `raw/results_full_20260911.csv` | 2026-09-11 | `PYTHONPATH=src python experiments/run_parametric_study.py --t-pm 1000 2000 4000 6000 8000 12000 16000 24000 --reps 20 --lim-drones 10 --max-ticks 50000 --n-filament-suppliers 5 --seed-base 1000 --out experiments/raw/results_full_20260911.csv` | {1000, 2000, 4000, 6000, 8000, 12000, 16000, 24000} | 160 (8×20) | усі 160 — `completed`, 10/10 дронів; seed 1000–1019; n_filament_suppliers=5. Команду відновлено за параметрами в CSV і підтверджено повтором однієї репліки (T_pm=1000, seed=1000: makespan 2071900 с); max-ticks не впливає на результат — найдовша репліка 36 224 тіки |
Формат команди для запису — повний виклик, напр.:


```
PYTHONPATH=src python experiments/run_parametric_study.py \
    --t-pm 1000 2000 4000 6000 8000 12000 16000 24000 \
    --reps 20 --lim-drones 10 --max-ticks 50000 \
    --out experiments/raw/results_YYYYMMDD.csv
```
