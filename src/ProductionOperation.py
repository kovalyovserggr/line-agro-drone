
from Resource import  ManufacturedResource
from EnumsLine import OperationState
from Efficiency import Efficiency

class ProductionOperation:
    """Базовий клас виробничих операцій, що враховує час виконання."""
    def __init__(self, name, description, input_resources,  duration, duration_letup, efficiency, res_manager):
        self.name = name                        # Назва ресурсу, що виготовляється операцією збігаєтьсяз назвою операції 
        self.description = description          # Опис операції
        self.input_resources = input_resources  # Вхідні ресурси (словник {назва: кількість})
        self.duration = duration                # Час виконання операції (у секундах)
        self.progress = 0.0                     # Прогрес виконання операції (у секундах) 
        self.duration_letup = duration_letup    # Час відпочинку поміж операціями (у секундах)
        self.efficiency : Efficiency = efficiency            # Модель ефективності (екземпляр класу Efficiency)
        self.state = OperationState.IDLE        # початковий стан
        self.resourses = []                     # обєкти ресурси (словник {назва: кількість})
        self.time_work = 0.0                    # Загальний час роботи операції після обслуговування
        self.res_manager = res_manager
        self.countProduct = 0.0 
        self.memory: list = []
    
    def create_resource(self, node_id):
        """Створює виготовлений ресурс на основі операції."""
        if  self.name == "Type0":
            self.res_manager.add_resource(self.name,  1000.0)
            self.countProduct += 1000.0
        else:
            self.res_manager.add_resource(self.name, ManufacturedResource(self.name, self.resourses, node_id))
            self.countProduct += 1.0
        self.resourses = []
    
    def callback(self, resources):
        """Функція зворотного виклику при отриманні ресурсів."""
        self.resourses = resources
        self.state = OperationState.EXECUTING
  