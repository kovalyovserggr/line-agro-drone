import threading
import time

class TimeManager:
        #:param production_line: об'єкт виробничої лінії
        #:param acceleration_factor: коефіцієнт прискорення
        #:param tick_rate_hz: кількість тік/сек (10 Гц = кожні 100 мс)
    def __init__(self, acceleration_factor=1.0, tick_rate_hz=10):
        self.acceleration_factor = acceleration_factor
        self.tick_interval = 1.0 / tick_rate_hz
        self.base_tick = self.tick_interval  # базовий часовий крок
        self.current_time = 0.0
        self._running = False
        self._thread = None

    def start(self):
        """Запускає таймер у окремому потоці."""
        self._running = True
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.start()

    def stop(self):
        """Зупиняє таймер."""
        self._running = False
        if self._thread:
            self._thread.join()

    def _run_loop(self):
        """Циклічно викликає tick() кожен інтервал."""
        while self._running:
            self.tick()
            time.sleep(self.tick_interval)

    def tick(self):
        """Обробляє тік і передає дельту часу у виробничу лінію."""
        delta_time = self.base_tick * self.acceleration_factor
        self.current_time += delta_time
        self.simulation.tick(self.current_time)