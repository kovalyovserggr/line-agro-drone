import sys
sys.path.insert(0, "src")

from AgroDroneLine import AgroDroneLine, SimulationComplete

print("=== Smoke test 2: T_pm=6000, seed=1, lim_drones_made=10 ===")
line = AgroDroneLine(seed=1, lim_drones_made=10, T_pm_print_park=6000.0, verbose=False)

elapsed = 0.0
dt = 100.0
maintenance_events = 0
repair_events = 0
working_ticks = 0
prev_statuses = {n.id: n.status for n in line.units if 2 <= n.id <= 16}

try:
    for step in range(6000):
        elapsed += dt
        line.tick(elapsed)
        for n in line.units:
            if 2 <= n.id <= 16:
                if n.status.name == "WORKING":
                    working_ticks += 1
                if n.status.name == "MAINTENANCE" and prev_statuses[n.id] != n.status:
                    maintenance_events += 1
                if n.status.name == "REPAIR" and prev_statuses[n.id] != n.status:
                    repair_events += 1
                prev_statuses[n.id] = n.status
except SimulationComplete as sc:
    print(f"\n✅ SimulationComplete: elapsed_time={sc.elapsed_time}, number_drones_made={sc.number_drones_made}")
else:
    print(f"\n⚠️ Ліміт кроків вичерпано без SimulationComplete, elapsed={elapsed}")

print(f"MAINTENANCE events (nodes 2-16): {maintenance_events}")
print(f"REPAIR events (nodes 2-16): {repair_events}")
print(f"WORKING-тіків сумарно по парку: {working_ticks}")
print(f"state_durations вузла 2: { {k.name: v for k,v in line.units[1].state_durations.items()} }")
print(f"state_durations вузла 6: { {k.name: v for k,v in line.units[5].state_durations.items()} }")
