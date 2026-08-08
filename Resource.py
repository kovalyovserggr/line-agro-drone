from typing import List, Optional
from datetime import date


class BaseResource:
    _id_counter = 1
    def __init__(self, name: str):
        self.name = name                                    # Унікальне ім'я ресурсу
        BaseResource._id_counter += 1
        self.id = BaseResource._id_counter                  # Унікальний ID ресурсу
        self.manufacture_date = date.today().strftime('%d.%m.%Y')  # Дата закупівлі
    
class PurchasedResource(BaseResource):
    def __init__(self, name: str):
        super().__init__(name)

class ManufacturedResource(BaseResource):

    def __init__(self, name: str, source_resources: Optional[List[BaseResource]] = None, node_id: Optional[int] = None  ):
        super().__init__(name)
        self.node_id = node_id                                     # ID вузла, що виготовив ресурс
        self.source_resources = source_resources or []            # Список ресурсів з яких складається виготовлений даний ресурс, напівфабрикат чи продукт

class RequestRes:

    def __init__(self, requester_node_id: float, requester_op_name: float,  input_resources: dict, callback=None):
        self.requester_name = requester_op_name      # Унікальний ID операції
        self.requester_node_id = requester_node_id   # Хто замовляє (ід вузла)
        self.input_resources = input_resources       # Вхідні ресурси (словник {назва: кількість})
        self.wait_ticks = 0                          # 🆕 Лічильник очікування
        self.callback = callback                     # Функція зворотного виклику при отриманні ресурсів

    def increment_wait(self):
        self.wait_ticks += 1
        return self.wait_ticks
    
    def __eq__(self, other):
        return (
            self.requester_name == other.requester_name and
            self.requester_node_id == other.requester_node_id
        )
    
class ResourcePool:
    def __init__(self,val_res):
        if isinstance(val_res, float):
            self.res = val_res
        else:
            self.res : List[BaseResource] = []
            
    def number(self):
        if isinstance(self.res, float):
            return self.res
        elif isinstance(self.res, list):
            return len(self.res)
        else:
            return 0; 

    def add(self, val):
        
        if isinstance(self.res, float) and isinstance(val, float):
            self.res += val
        elif isinstance(self.res, list) and isinstance(val, BaseResource):
            self.res.append(val)
        elif self.res == None and isinstance(val, BaseResource):
            self.res = []
            self.res.append(BaseResource(val.name))
        elif self.res == None and isinstance(val, list):
            self.res = []
            for obj in val:
                self.res.append(BaseResource(obj.name))

    def get(self,val):
        if isinstance(self.res, float):
            if(self.res >= val):
                self.res -= val
                return val
            else:
                return 0
        elif isinstance(self.res, list):
            if len(self.res) >= val:
                extracted = []
                for _ in range(min(val, len(self.res))):
                    extracted.append(self.res.pop(0))
                return extracted
            else:
                return []
        else:
            []
        
