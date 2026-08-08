from typing import Callable
from ResourceManager import ResourceManager
from Resource import RequestRes
from EnumsLine import NodeState

class ProductionPlanner:
    def __init__(self):
        self.resource_limits : dict[ str ,int ] = {} # Скільки потрібно кожного ресурсу
        # 🔹 Делегати — ініціалізуються методами лінії
        self.get_state: Callable[[int], NodeState] = lambda id: NodeState.IDLE
        self.get_reserved: Callable[[str], int] = lambda res: 0
        self.limit_drones = 0

    def process_request(self, request: RequestRes, res_manager: ResourceManager) -> bool:
        id = request.requester_node_id
        name = request.requester_name

        # 🔹 Перевірка: чи ресурс ще потрібен
        produced = self.get_reserved(name) 
        required = self.resource_limits.get(name, 0) * self.limit_drones 
      
        if produced >= required:
            return False  # Вироблено достатньо

        if self.get_state(id) != NodeState.IDLE: # 🔹 Перевірка: чи вузол вільний
            return False  # Вузол зайнятий

        # 🔹 Дозволено запит
        res_manager.add_requests(request)
        return  True
    
