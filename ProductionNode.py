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
            planner : ProductionPlanner = None
            ):
        self.id = id
        self.description = description
        self.reliability = reliability
        self.time_work = 0.0
        self.agentNode = None
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
        """Оновлює статус вузла та його операцій на основі параметрів ефективності та надійності"""

     
 

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

        


            
       
       