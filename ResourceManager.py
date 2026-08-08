from collections import  deque
from Resource import RequestRes, ResourcePool 
from Resource import BaseResource

class ResourceManager:
    def __init__(self):
        # Ініціалізація типів ресурсів
        self.resources : dict[str, ResourcePool] = {} # словник де зберігаються ресурси (імя_ресурсу: [ресурси])
        self.requests = list()             # список запитів на ресурси      
        self.agent = None


    def add_resource(self, name: str, item: BaseResource):
        self.resources[name].add(item)

    def add_requests(self, item: RequestRes) -> bool:
        print(f"📜  операція - {item.requester_name} вузла {item.requester_node_id} успішний запит на ресурси")                 
        self.requests.append(item)

    def tick(self):
        self.requests.sort(key=lambda x: x.wait_ticks, reverse=True)  # сортування запитів за часом очікування
        list_requsets_for_remove = list()
        for item in self.requests:
            if self.agent is not None:
                return self.agent.get_resourse(item, self.resources, self.requests)
            else:

                count_res = 0; 
                # Перевірка наявності всіх потрібних ресурсів
                for res_name, qty_needed in item.input_resources.items():
                    if(self.resources[res_name] == None):
                        available_qty = 0
                    else:
                        available_qty = self.resources[res_name].number()
                    if available_qty >= qty_needed:
                        count_res += 1
               
               # вилучення ресурсів зі складу, якщо можливо виконати запит
                if count_res == len(item.input_resources):
                    used_resources = {}
                    for res_name, qty_needed in item.input_resources.items():
                        used_resources[res_name] = self.resources[res_name].get(qty_needed)
                    list_requsets_for_remove.append(item)
                    print(f"🍄  операція - {item.requester_name} вузла {item.requester_node_id} отримала ресурси")                 
                    item.callback(used_resources)
                else:
                    # Якщо не вдалося — збільшуємо лічильник очікування
                    item.increment_wait()
        for r in list_requsets_for_remove:
            self.requests.remove(r)

    def info(self) -> str:
        info_str = "Ресурси на складі:\n"
        for res_name, pool in self.resources.items():
            info_str += f" - {res_name}: {pool.number()} одиниць\n"

        for req in self.requests:
            info_str += f"Запит від вузла {req.requester_node_id} для виготовлення '{req.requester_name}' очікує вже {req.wait_ticks} тактів\n"
        return info_str


                       