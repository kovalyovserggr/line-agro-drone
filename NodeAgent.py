class NodeAgent:
    def __init__(self, node):
        self.node = node # це об'єкт ProductionNode, який містить стан вузла та операції.
        self.name = f"agentNode_{node.name}"
        self.last_time = 0.0

     #Метод керування вузлом у симуляції.
    def tick(self, current_time: float):# Логіка агента для керування вузлом
        pass
    
    def get_resourse(self, op):
        pass

    def init_operation(self, op):
        pass
    
    def complete_operation(self,  node, op):
        pass
        
    def evaluate(self, node, current_time):
        pass

