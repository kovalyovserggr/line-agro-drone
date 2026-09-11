from enum import Enum, auto

class OperationState(Enum):
    # Стани операцій
    WAITING_FOR_RESOURCE = auto()           # Очікує ресурс, запит на ресурс надіслано на склад
    EXECUTING = auto()                      # Виконується
    BLOCKED_BY_AGENT = auto()               # Заблокована агентом
    IDLE = auto()                           # Простоювання операції, запит на ресурс не відправлявся і операція не активізовувалась
    LETUP = auto()                          # відпочинок поміж операціями

# Клас для відстеження стану вузла
class NodeState(Enum):
    # Стани вузла
    WAITING_FOR_RESOURCE = auto()           # Очікує ресурс
    MAINTENANCE = auto()                    # Профілактика вузла
    REPAIR = auto()                         # Ремонт вузла
    FAILURE = auto()                        # Аварія вузла
    IDLE = auto()                           # Простоювання вузла
    WORKING = auto()                        # Виконання операції
    
# Клас для відстеження стану вузла
class NodeEfficiencyState(Enum):
    # Стани вузла
    OPTIMAL = auto()           # Оптимальна ефективність
    RISKY = auto()             # Ризикована ефективність
    CRITICAL = auto()          # Критична ефективність
    FAILED = auto()            # Вузол не працює
    
class NodeReliabilityState(Enum):
    # Стани надійності вузла
    HIGH = auto()           # Висока надійність
    MEDIUM = auto()         # Середня надійність
    LOW = auto()            # Низька надійність
    BROKEN = auto()         # Вузол не працює