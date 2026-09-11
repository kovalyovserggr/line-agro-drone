from Efficiency import Reliability
from EnumsLine import NodeState
from Resource import RequestRes
from ResourceManager import ResourceManager
from collections import deque
from ProductionOperation import  OperationState, ProductionOperation
from ProductionPlanner import ProductionPlanner
import sys

# Батьківський клас виробничого вузла
class ProductionNode: 
    Efficiency = {str: float}
    Reliability = {str: float}
    def __init__(
            self,
            id: float,
            description: str,
            reliability: Reliability,
            duration_maintenance,
            duration_repair,
            operations: list,
            res_manager: ResourceManager,
            planner : ProductionPlanner = None,
            T_pm: float | None = None
            ):
        self.id = id
        self.description = description
        self.reliability = reliability
        self.time_work = 0.0
        self.agentNode = None
        # --- Параметричне дослідження (стаття 1, 4.2): T_pm — фіксований період
        # проактивного ТО, що ЗАМІНЮЄ природний стохастичний maintenance_interval,
        # коли задано (не None). Для вузлів поза дослідженням лишається None —
        # ТО настає за природним розподілом self.reliability.maintenance_interval.
        self.T_pm = T_pm
        self.next_failure_threshold: float | None = None     # семпл з failure_frequency
        self.next_maintenance_threshold: float | None = None  # T_pm або семпл з maintenance_interval
        self.operations = operations if operations else []
        self.status = NodeState.IDLE
        self.progress = 0.0
        self.duration_maintenance = duration_maintenance
        self.duration_repair = duration_repair
        self.request_register = {}  # {resource_name: bool}
        self.active_operation = None
        self.last_time = 0.0
        self.current_op :ProductionOperation = None  # поточна операція що виконується
        self.res_manager = res_manager
        self.state_durations: dict[NodeState, float] = {
                NodeState.MAINTENANCE: 0.0,
                NodeState.REPAIR: 0.0,
                NodeState.FAILURE: 0.0,
                NodeState.IDLE: 0.0,
                NodeState.WAITING_FOR_RESOURCE: 0.0,
                NodeState.WORKING: 0.0 }
        
        self.produced: dict[str, int] = {} # {назва ресурсу: кількість виготовленого}
        self.defects: dict[str, int] = {} # {назва ресурсу: кількість браку}
        self.reserved: dict[str, int] = {} # {назва ресурсу: кількість зарезервованого}
        self.planner = planner             # посилання на планувальник
        self.made_dron = None              # callback на виготовлення дрона
        self.init_stat_dict()
        self.memory: list = []

        print(f"✅ Ініціалізовано вузол: {self.id}")
    
    def init_stat_dict(self):
        for op in self.operations:
            self.produced[op.name] = 0
            self.reserved[op.name] = 0

    def get_status(self) -> NodeState:
        return self.status

    def get_reserved(self, res_name: str) -> int:
        return self.reserved.get(res_name,0) 
    
    def get_produced(self, res_name: str) -> int:
        return self.producedget.get(res_name,0) 
     
    def update_status(self):
        """Перевіряє накопичене напрацювання (self.time_work) на предмет випадкової
        відмови. Діє лише поки вузол WORKING — у решті станів напрацювання не
        накопичується, перевіряти нема чого.

        Поріг self.next_failure_threshold семплюється з self.reliability.reliability
        ("λ безвідмовності", TimeDependentExponential, λ(t) зростає з напрацюванням —
        ефект старіння). НЕ self.reliability.failure_frequency: димовий тест
        2026-08-31 показав, що за λ₀ з node_paramsN (напр. 0.01 для вузла 1)
        failure_frequency дає MTBF ~100с — на два порядки коротше за тривалість однієї
        операції (1800с+), тобто вузол ніколи не встигає нічого виготовити. За
        узгодженням з автором (Serhii, 2026-08-31): REPAIR запускає саме reliability
        (λ~5·10⁻⁵ → MTBF~20000с, фізично правдоподібно), а failure_frequency лишається
        діагностичним полем — семплюється й пишеться в історію (self.memory), але на
        FSM не впливає, як і в оригінальному коді до цих правок.

        Відмова МОЖЕ перервати операцію мід-флайт — це відповідає природі непланової
        поломки. Планове ТО (T_pm / maintenance_interval) навмисно перевіряється в
        ІНШОМУ місці — на межі операцій (див. _maintenance_due(), викликається з IDLE
        у tick()), а не тут: другий димовий тест 2026-08-31 показав, що для частини
        вузлів середній природний maintenance_interval (напр. 1000с для вузла 1)
        коротший за тривалість однієї операції (1800с) — при неперервній перевірці
        мід-флайт вузол узагалі ніколи не завершував би жодного циклу. Це рішення я
        прийняв самостійно (без окремого підтвердження) як інженерно необхідне для
        працездатності лінії; варте фіксації в DECISIONS.md і перевірки, чи не
        суперечить задуму статті."""
        if self.status != NodeState.WORKING:
            return

        if self.next_failure_threshold is None:
            self.next_failure_threshold = self.reliability.reliability.sample(self.time_work)
        if self.time_work >= self.next_failure_threshold:
            self._interrupt_to(NodeState.REPAIR)

    def _maintenance_due(self) -> bool:
        """Перевіряється на межі операцій (з IDLE, перед вибором нової), не мід-флайт.
        Поріг: self.T_pm, якщо вузол бере участь у параметричному дослідженні 4.2,
        інакше природний розподіл self.reliability.maintenance_interval (LogNormal)."""
        if self.next_maintenance_threshold is None:
            self.next_maintenance_threshold = (
                self.T_pm if self.T_pm is not None
                else self.reliability.maintenance_interval.sample(self.time_work)
            )
        return self.time_work >= self.next_maintenance_threshold

    def _interrupt_to(self, new_status: NodeState):
        """Перериває поточну операцію (якщо є) і переводить вузол у REPAIR/MAINTENANCE.
        Перервана операція скидається в IDLE (а не лишається "підвислою" в EXECUTING),
        щоб вузол міг коректно повернутись до неї в наступному циклі IDLE.
        ВІДОМЕ СПРОЩЕННЯ: уже спожиті на перервану операцію ресурси (op.resourses)
        не повертаються на склад — це прийнятний, задокументований компроміс для
        цього дослідження (перерваних циклів відносно мало порівняно з тривалістю
        operations 3D-друку), але його варто явно зазначити в DECISIONS.md репозиторію."""
        if self.current_op is not None:
            self.current_op.progress = 0.0
            self.current_op.state = OperationState.IDLE
            self.current_op = None
        self.status = new_status
        self.progress = 0.0
        self.next_failure_threshold = None
        self.next_maintenance_threshold = None

    def tick(self, current_time: float, is_point : int):
               
        delta = current_time - self.last_time
        self.last_time = current_time
        self.state_durations[self.status] += delta
        
        # оновлюємо статуси
        self.update_status()
        
        # 🧠 Виклик агента для оцінки стану та керуванням вузлом
        if self.agentNode:
            self.agentNode.tick(self, current_time) 
        else:
            """Центральна FSM-логіка вузла та операцій"""
            if self.status == NodeState.MAINTENANCE:
                self.progress += delta
                if self.progress >= self.duration_maintenance:
                    self.status = NodeState.IDLE
                    self.time_work = 0.0
                    self.progress = 0.0

            elif self.status == NodeState.REPAIR:
                self.progress += delta
                if self.progress >= self.duration_repair:
                    self.status = NodeState.IDLE
                    self.time_work = 0.0
                    self.progress = 0.0

            elif self.status == NodeState.WORKING:
                if not self.current_op:
                    self.status = NodeState.IDLE
                    return
                
                op = self.current_op
                self.time_work += delta
                op.time_work += delta
                op.efficiency.get(op.time_work)
                self.reliability.get(self.time_work)

                if op.state == OperationState.EXECUTING:
                    op.progress += delta
                    if op.progress >= op.duration:
                        op.create_resource(self.id)
                        op.progress = 0.0
                        op.state = OperationState.LETUP

                        if op.name in self.produced:
                            self.produced[op.name] += 1000 if op.name == "Type0" else 1
                        else:
                            self.produced[op.name] = 1000 if op.name == "Type0" else 1

                        print(f"✅ Виготовлено - '{op.name}' на вузлі {self.id}, на складі: {op.res_manager.resources[op.name].number()}")
                                                   
                        if self.made_dron: 
                            print(f"🚜 виготовлено агродрон 📈")
                            self.made_dron(self.id)

                elif op.state == OperationState.LETUP:
                    op.progress += delta
                    if op.progress >= op.duration_letup:
                        op.progress = 0.0
                        op.state = OperationState.IDLE
                        self.current_op = None
                        self.status = NodeState.IDLE

            elif self.status == NodeState.WAITING_FOR_RESOURCE:
                # 🔹 Перевіряємо чи отримано ресурси для поточної операції
                if self.current_op and self.current_op.state == OperationState.EXECUTING:
                    self.current_op.progress = 0.0
                    self.status = NodeState.WORKING

            elif self.status == NodeState.IDLE:
                # 🔧 Планове ТО перевіряється саме тут — на межі операцій, до вибору
                # нової роботи (не мід-флайт, див. _maintenance_due()/update_status())
                if self._maintenance_due():
                    self.status = NodeState.MAINTENANCE
                    self.progress = 0.0
                    self.next_maintenance_threshold = None
                    self.next_failure_threshold = None
                    return
                # 🔹 Аналізуємо всі операції, які вузол може виконувати
                for op in self.operations:
                    if op.state == OperationState.IDLE: 
                        if self.planner.process_request(RequestRes(self.id, op.name, op.input_resources, op.callback), self.res_manager) :
                            self.current_op = op
                            self.status = NodeState.WAITING_FOR_RESOURCE  
                            # 🔹 Лічильник замовленої продукції
                            if op.name in self.reserved:
                                self.reserved[op.name] += 1000 if op.name == "Type0" else 1
                            else:
                                self.reserved[op.name] = 1000 if op.name == "Type0" else 1 
                            break  # запускаємо лише одну операцію за цикл
        if(is_point):       
            self.memory.append(self.reliability.get(self.time_work))
            for o in self.operations:
                o.memory.append(o.efficiency.get(self.time_work))

        


            
       
       