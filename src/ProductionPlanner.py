from typing import Callable
from ResourceManager import ResourceManager
from Resource import RequestRes
from EnumsLine import NodeState

class ProductionPlanner:
    # D12 (2026-09-11): сипучі/об'ємні ресурси (не дискретні деталі "рівно
    # по одній на дрон") — виробляються "на вимогу", БЕЗ верхньої BOM-квоти.
    # Жорсткий ліміт "рівно стільки, скільки треба на N дронів" коректний для
    # Type1..Type21 (дискретні деталі), але для Type0 (філамент) і TypePL
    # (базова сировина) він створює термінальний дефіцит: щойно сумарне
    # виробництво впирається в квоту, постачання зупиняється НАЗАВЖДИ, а
    # залишок на складі — випадкова сума, яка може бути замалою для будь-якої
    # з конкретних заявок парку, що ще чекають (762-1538 од. за раз). Див.
    # docs/DECISIONS.md D12.
    UNBOUNDED_RESOURCES = {"Type0", "TypePL"}

    def __init__(self):
        self.resource_limits : dict[ str ,int ] = {} # Скільки потрібно кожного ресурсу
        # 🔹 Делегати — ініціалізуються методами лінії
        self.get_state: Callable[[int], NodeState] = lambda id: NodeState.IDLE
        self.get_reserved: Callable[[str], int] = lambda res: 0  # замовлено (не декрементується — не для throttle, див. D11)
        self.get_produced: Callable[[str], int] = lambda res: 0  # D11: реально виготовлено — саме це звіряємо з квотою
        self.get_defects: Callable[[str], int] = lambda res: 0  # D15: списано в брак — розширює квоту на компенсацію
        self.get_bom_footprint: Callable[[str], dict] = lambda name: {name: 1}  # D18: наскрізний BOM-слід для нарахування браку
        self.limit_drones = 0

    def process_request(self, request: RequestRes, res_manager: ResourceManager) -> bool:
        id = request.requester_node_id
        name = request.requester_name

        if name not in self.UNBOUNDED_RESOURCES:
            # 🔹 Перевірка: чи ресурс ще потрібен (лише для дискретних деталей —
            # сипучі ресурси з UNBOUNDED_RESOURCES цю перевірку пропускають, D12)
            # D11 (2026-09-11): раніше тут стояло self.get_reserved(name) — рахунок
            # ЗАМОВЛЕНОГО (видано дозвіл на запит), який ніколи не декрементується.
            # Це блокувало НОВІ спроби назавжди, щойно замовлень назбиралось на
            # required, навіть якщо частина з них так і не була виконана (застрягла
            # в черзі на ResourceManager через дефіцит вхідних ресурсів) — вело до
            # безповоротного deadlock, що ставав ЧАСТІШИМ і РАНІШЕ саме при
            # ЗБІЛЬШЕННІ пропускної здатності (вузли встигали видати замовлення
            # швидше, ніж вони реально виконувались). Замінено на get_produced() —
            # рахунок РЕАЛЬНО завершеного виробництва.
            produced = self.get_produced(name)
            # D15 (2026-09-11): required розширюється на get_defects(name) — обсяг,
            # списаний у брак через REPAIR-переривання мід-флайт десь у лінії
            # (див. ProductionNode._interrupt_to()). Без цього доповнення жорсткий
            # ліміт "рівно BOM×N" не має запасу на жоден шлюб: щойно матеріал
            # згорає в перерваній операції, виробник вже вичерпав свою квоту й
            # ніколи не компенсує втрату — перманентний дедлок, що НЕ лікується
            # збільшенням --max-ticks (див. pilot_d14_extended.csv, DECISIONS.md D15).
            required = self.resource_limits.get(name, 0) * self.limit_drones + self.get_defects(name)

            if produced >= required:
                return False  # Вироблено достатньо (з урахуванням компенсації браку)

        if self.get_state(id) != NodeState.IDLE: # 🔹 Перевірка: чи вузол вільний
            return False  # Вузол зайнятий

        # 🔹 Дозволено запит
        res_manager.add_requests(request)
        return  True
    
