from AgroDroneLine import AgroDroneLine
from TimeManager import TimeManager

class SimulationLine:
    def __init__(self, timer):
        self.line = AgroDroneLine()
        self.timer = timer
        self.timer.simulation = self

    def tick(self, elapsed_time):
        self.line.tick(elapsed_time)

if __name__ == "__main__":
    # Реальночасовий інтерактивний режим (з sleep між тіками). Для швидкого
    # батч-експерименту (сітка T_pm × N реплікацій) використовується
    # experiments/run_parametric_study.py, який керує AgroDroneLine напряму,
    # без TimeManager/sleep — інакше кожна репліка займала б ~30-60с реального часу.
    a = SimulationLine(TimeManager(acceleration_factor=10000.0, tick_rate_hz=100))
    print("🚀 Запуск симуляції виробничої лінії...")
    a.timer.start()



