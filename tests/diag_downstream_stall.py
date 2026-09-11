"""Діагностика нового стопору (пілот pilot_d14_extended.csv, 2026-09-11):
збільшення --max-ticks з 30000 до 100000 (10-кратний запас модельного часу)
дало ІДЕНТИЧНІ drones_made на кожному з 10 seed — отже, лінія не "повільна",
а десь до t=3*10^6с впирається в СПРАВЖНІЙ, постійний стопор (по аналогії з
класом багів D11/D12, але, судячи з усього, вже не на Type0/TypePL, а десь
у ланцюжку дискретних деталей Type1-Type21 / вузли 17-26).

Стратегія: прогнати ОДНУ реплiку (найгірший випадок з pilot_d14: T_pm=24000,
seed=1002, n_filament_suppliers=5, drones_made застряг на 2) до ticks, що
свідомо перевищують точку стопору, і зробити повний знімок стану:
  - для кожного Type0..Type22: склад, вироблено (get_produced), квота
    (resource_limits*limit_drones), скільки вузлів фізично виробляють цей
    тип і в якому вони стані;
  - для кожного вузла: id, статус, поточна операція (якщо є), reserved/produced
    по його власних типах;
  - усі pending-запити в ResourceManager: хто просить, що просить, скільки
    тіків чекає.

Використання:
    PYTHONPATH=src python tests/diag_downstream_stall.py \
        --t-pm 24000 --seed 1002 --n-filament-suppliers 5 --max-ticks 35000
"""
import argparse
import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from AgroDroneLine import AgroDroneLine, SimulationComplete  # noqa: E402
from EnumsLine import NodeState  # noqa: E402

DT = 100.0

ALL_TYPES = [f"Type{i}" for i in range(0, 23)] + ["TypePL"]


def snapshot(line: AgroDroneLine, elapsed: float):
    print(f"\n{'='*100}\nЗНІМОК СТАНУ на t={elapsed:.0f}с (drones_made={line.number_drones_made})\n{'='*100}")

    print(f"\n--- Ресурси (склад / вироблено / квота) ---")
    print(f"{'Тип':>8} {'склад':>10} {'вироблено':>10} {'квота':>10} {'заблоковано?':>13}  виробники (id: статус[/op])")
    limit_drones = line.planner.limit_drones
    for t in ALL_TYPES:
        stock = line.res_manager.resources[t].number() if t in line.res_manager.resources else None
        produced = line.get_produced(t)
        required = line.planner.resource_limits.get(t, 0) * limit_drones
        blocked = "ТАК" if (t not in line.planner.UNBOUNDED_RESOURCES and produced >= required and required > 0) else ""
        producers = []
        for n in line.units:
            for op in n.operations:
                if op.name == t:
                    cur = f"/{n.current_op.name}:{n.current_op.state.name}" if n.current_op else ""
                    producers.append(f"{n.id}:{n.status.name}{cur}")
        stock_s = f"{stock:.1f}" if stock is not None else "—"
        print(f"{t:>8} {stock_s:>10} {produced:>10} {required:>10} {blocked:>13}  {producers}")

    print(f"\n--- Вузли (усі, статус != WORKING/IDLE виділено) ---")
    for n in sorted(line.units, key=lambda u: u.id):
        cur_op = n.current_op.name if n.current_op else "-"
        cur_state = n.current_op.state.name if n.current_op else "-"
        marker = " <<<" if n.status in (NodeState.WAITING_FOR_RESOURCE, NodeState.REPAIR, NodeState.FAILURE) else ""
        print(f"  id={n.id:>5} статус={n.status.name:<22} поточна_оп={cur_op:<8}({cur_state:<10}) "
              f"reserved={dict(n.reserved)} produced={dict(n.produced)}{marker}")

    print(f"\n--- Pending запити в ResourceManager (усі) ---")
    reqs = sorted(line.res_manager.requests, key=lambda r: -r.wait_ticks)
    if not reqs:
        print("  (пусто)")
    for r in reqs:
        print(f"  вузол={r.requester_node_id:>5} просить={r.requester_name:<8} "
              f"потрібно={r.input_resources} чекає_тіків={r.wait_ticks}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t-pm", type=float, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n-filament-suppliers", type=int, default=1)
    ap.add_argument("--max-ticks", type=int, default=35000)
    ap.add_argument("--snapshot-every", type=int, default=0,
                     help="якщо >0 — робити знімок кожні N тіків (крім фінального)")
    args = ap.parse_args()

    line = AgroDroneLine(seed=args.seed, lim_drones_made=10, T_pm_print_park=args.t_pm,
                          verbose=False, n_filament_suppliers=args.n_filament_suppliers)
    elapsed = 0.0
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            for step in range(1, args.max_ticks + 1):
                elapsed += DT
                line.tick(elapsed)
                if args.snapshot_every and step % args.snapshot_every == 0:
                    with contextlib.redirect_stdout(sys.__stdout__):
                        snapshot(line, elapsed)
    except SimulationComplete as sc:
        print(f"\n✅ SimulationComplete: elapsed={sc.elapsed_time:.0f}с, дронів={sc.number_drones_made}")
        return

    snapshot(line, elapsed)


if __name__ == "__main__":
    main()
