from AgroDroneLine import AgroDroneLine
from TimeManager import TimeManager

class SimulationLine:
    def __init__(self, timer):
        self.line = AgroDroneLine()
        self.timer = timer
        self.timer.simulation = self

    def tick(self, elapsed_time):
        self.line.tick(elapsed_time)

a = SimulationLine(TimeManager(acceleration_factor=10000.0, tick_rate_hz=100))
print("🚀 Запуск симуляції виробничої лінії...")
a.timer.start()



