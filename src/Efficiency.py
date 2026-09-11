from scipy import stats
from scipy.stats import norm, expon, uniform, lognorm

class IncreasingParameter:
    def __init__(self, initial_value: float, rate: float = 0.001):
        """
        :param initial_value: початкове значення
        :param rate: швидкість зростання (додаток за одиницю часу)
        """
        self.initial_value = initial_value
        self.rate = rate

    def sample(self, time_work: float) -> float:
        """Значення зростає лінійно з часом"""
        return self.initial_value + self.rate * time_work

class DecreasingParameter:
    def __init__(self, initial_value: float, rate: float = 0.001):
        """
        :param initial_value: початкове значення
        :param rate: швидкість спадання (віднімання за одиницю часу)
        """
        self.initial_value = initial_value
        self.rate = rate

    def sample(self, time_work: float) -> float:
        """Значення зменшується лінійно з часом, але не нижче нуля"""
        value = self.initial_value - self.rate * time_work
        return max(value, 0.0)
class ConstantParameter:
    def __init__(self, value: float):
        """
        :param value: постійне значення
        """
        self.value = value

    def sample(self, time_work: float) -> float:
        """Завжди повертає початкове значення"""
        return self.value
    
class TimeDependentNormal:
    """Нормальний розподіл, що змінюється з часом"""
    def __init__(self, mean, std_dev, rate_of_change):
        self.mean = mean  # Початкове середнє значення
        self.std_dev = std_dev  # Стандартне відхилення
        self.rate_of_change = rate_of_change  # Швидкість зміни параметра з часом

    def sample(self, time, precision = 2)-> float:
        """Генерує значення з урахуванням зниження або зростання параметра з часом"""
        dynamic_mean = max(0.01, self.mean - self.rate_of_change * time)
        return round(stats.norm.rvs(loc=dynamic_mean, scale=self.std_dev), precision)

class TimeDependentExponential:
    """Експоненціальний розподіл, що залежить від часу"""
    def __init__(self, rate, rate_of_change):
        self.rate = rate  # Початкова швидкість (λ)
        self.rate_of_change = rate_of_change  # Швидкість зміни параметра з часом

    def sample(self, time, precision = 5)-> float:
        """Генерує значення, що змінюється відповідно до експоненціального розподілу"""
        dynamic_rate = max(0.0001, self.rate * (1 + self.rate_of_change * time))  # З часом частота збоїв зростає
        return round(stats.expon.rvs(scale=1 / dynamic_rate), precision)

class TimeDependentUniform:
    """Рівномірний розподіл, що змінюється з часом"""
    def __init__(self, lower, upper, rate_of_change):
        self.lower = lower  # Початкова нижня межа
        self.upper = upper  # Початкова верхня межа
        self.rate_of_change = rate_of_change  # Зміна межі з часом

    def sample(self, time, precision = 2)-> float:
        """Генерує значення у межах рівномірного розподілу з врахуванням змін"""
        dynamic_lower = self.lower - self.rate_of_change * time
        dynamic_upper = max(dynamic_lower + 0.01, self.upper - self.rate_of_change * time)
        return round(stats.uniform.rvs(loc=dynamic_lower, scale=dynamic_upper - dynamic_lower), precision)

class TimeDependentLogNormal:
    """Логнормальний розподіл, що змінюється з часом"""
    def __init__(self, mu, sigma, rate_of_change):
        self.mu = mu  # Початкове значення
        self.sigma = sigma  # Відхилення
        self.rate_of_change = rate_of_change  # Як швидко змінюється параметр

    def sample(self, time, precision = 2)-> float:
        """Генерує значення з врахуванням зміни розподілу"""
        dynamic_mu = max(0.01, self.mu - self.rate_of_change * time)  # Чим більше часу пройшло, тим нижчий параметр
        return round(stats.lognorm.rvs(s=self.sigma / dynamic_mu, scale=dynamic_mu), precision)

class NormalDistribution:
    """Клас-обгортка для нормального розподілу"""
    def __init__(self, mean, std_dev):
        self.mean = mean
        self.std_dev = std_dev

    def sample(self, time, precision = 2) -> float:
        """Генерує значення згідно з нормальним розподілом"""
        return round(stats.norm.rvs(loc=self.mean, scale=self.std_dev), precision)

class ExponentialDistribution:
    """Клас-обгортка для експоненціального розподілу"""
    def __init__(self, rate):
        self.rate = rate

    def sample(self, time, precision = 5) -> float:
        """Генерує значення згідно з експоненціальним розподілом"""
        return round(stats.expon.rvs(scale=1 / self.rate), precision)

class UniformDistribution:
    """Клас-обгортка для рівномірного розподілу"""
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def sample(self, time, precision = 2) -> float:
        """Генерує значення згідно з рівномірним розподілом"""
        return round(stats.uniform.rvs(loc=self.lower, scale=self.upper - self.lower), precision)

class LogNormalDistribution:
    """Клас-обгортка для логнормального розподілу"""
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def sample(self, time, precision = 2)-> float:
        """Генерує значення згідно з логнормальним розподілом"""
        return round(stats.lognorm.rvs(s=self.sigma / self.mu, scale=self.mu), precision)
        
class Efficiency:
    
    def __init__(self,
                 productivity: float,
                 utilization_rate: float,
                 integration_capability: str,
                 scaling_potential: str,
                 schedule_accuracy: NormalDistribution,
                 defect_rate: NormalDistribution,
                 stability: UniformDistribution,
                 reconfiguration_speed: float,
                 power_usage: float,
                 maintenance_cost: float,
                 profitability: float,
                 certification_compliance: float,
                 waste_generation: float,
                 environmental_efficiency: float,       
                 ):
        
        # Конструктивні характеристики
        self.productivity = productivity                        # Продуктивність виробничого вузла
        self.utilization_rate = utilization_rate                # Використання виробничої потужності
        self.integration_capability = integration_capability     # Можливість інтеграції нових модулів
        self.scaling_potential  = scaling_potential              # Масштабованість виробничої потужності

        # Статистичні характеристики
        self.schedule_accuracy = schedule_accuracy # Точність виконання виробничого графіка
        self.defect_rate = defect_rate              # Відсоток дефектів продукції
        self.stability = stability                   # Стабільність технологічних параметрів
        
        # Вимірювані характеристики
        self.reconfiguration_speed = reconfiguration_speed    # Швидкість переналаштування між процесами
        self.power_usage = power_usage              # Енергетична ефективність
        self.maintenance_cost = maintenance_cost    # Витрати на експлуатацію та обслуговування
        self.profitability = profitability           # Рентабельність вузла
        self.certification_compliance = certification_compliance # Відповідність продукції сертифікаційним вимогам
        self.waste_generation  = waste_generation       # Обсяг відходів та викидів
        self.environmental_efficiency  = environmental_efficiency # Рівень використання екологічних технологій
        
    def get(self, time_work: float) -> dict:
        """Оновлює вимірювані характеристики ефективності на основі розподілів"""
        
        def fmt(value, precision=4):
            # якщо є метод sample() → викликаємо його
            if hasattr(value, "sample"):
                value = value.sample(time_work)
            return round(float(value), 5)
            
        x = {
        "productivity": fmt(self.productivity),
        "utilization_rate": fmt(self.utilization_rate),
        "integration_capability": str(self.integration_capability),
        "scaling_potential": str(self.scaling_potential),

        "schedule_accuracy": fmt(self.schedule_accuracy),
        "defect_rate": fmt(self.defect_rate),
        "stability": fmt(self.stability),

        "reconfiguration_speed": fmt(self.reconfiguration_speed),
        "power_usage": fmt(self.power_usage),
        "maintenance_cost": fmt(self.maintenance_cost),
        "profitability": fmt(self.profitability),
        "certification_compliance": fmt(self.certification_compliance),
        "waste_generation": fmt(self.waste_generation),
        "environmental_efficiency": fmt(self.environmental_efficiency),
        }
        return x
        
class Reliability:
  
    def __init__(self, 
                repairability: str, 
                preservation: float, 
                longevity: float,
                failure_frequency: TimeDependentExponential,  # Частота технічних збоїв
                maintenance_interval: TimeDependentLogNormal, # Інтервал міжремонтного обслуговування
                reliability: TimeDependentExponential,        # Безвідмовність вузла
                emergency_response: float                     # Швидкість реагування на аварійні ситуації
                ):

        # Конструктивні характеристики
        self.repairability = repairability    # Ремонтопридатність
        self.preservation = preservation      # Збережуваність
        self.longevity = longevity            # Довговічність

        # Статистичні характеристики
        self.failure_frequency: TimeDependentExponential = failure_frequency # Частота технічних збоїв
        self.maintenance_interval : TimeDependentLogNormal = maintenance_interval # Інтервал міжремонтного обслуговування
        self.reliability : TimeDependentExponential = reliability # Безвідмовність вузла.

        #вимірювані характеристики
        self.emergency_response: float = emergency_response     # Швидкість реагування на аварійні ситуації
           
    def get(self, time_work: float) -> dict:
        def fmt(value, precision=4, *args):
            # універсальний форматер: семплить якщо є .sample(), і округлює
            if hasattr(value, "sample"):
                value = value.sample(time_work, *args)
            return float(value)
        
        x = { 
            "repairability": str(self.repairability),
            "preservation": fmt(self.preservation),
            "longevity": fmt(self.longevity),
            
            "failure_frequency": fmt(self.failure_frequency, 5),
            "maintenance_interval": fmt(self.maintenance_interval, 5),
            "reliability": fmt(self.reliability, 5),
            
            "emergency_response": fmt(self.emergency_response)}
        return x


