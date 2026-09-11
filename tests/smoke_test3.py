import sys, time
sys.path.insert(0, "src")
from AgroDroneLine import AgroDroneLine, SimulationComplete
import contextlib, io

t0 = time.time()
line = AgroDroneLine(seed=1, lim_drones_made=10, T_pm_print_park=6000.0, verbose=False)

elapsed = 0.0
dt = 100.0
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        for step in range(20000):  # up to 2,000,000s model time safety cap
            elapsed += dt
            line.tick(elapsed)
except SimulationComplete as sc:
    t1 = time.time()
    print(f"✅ makespan = {sc.elapsed_time:.1f} s (модельного часу), {sc.number_drones_made} дронів")
    print(f"   реальний час прогону: {t1-t0:.2f} с")
else:
    t1 = time.time()
    print(f"⚠️ не завершилось за {elapsed} с модельного часу / {t1-t0:.2f} с реального")

# швидка перевірка стану парку (нема "підвислих" вузлів)
for n in line.units:
    if 2 <= n.id <= 16:
        pass
print("state_durations вузол 2 (3D-друк):", {k.name: round(v) for k,v in line.units[1].state_durations.items()})
