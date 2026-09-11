# SIMULATION_MODEL_SPEC.md

Технічна специфікація моделі в `src/` — довідник по класах і параметрах, на
який спирається Розділ 3.4 статті 1 (Рис. 3 — UML-схема класів, Таблиця 4 —
параметри вузлів). Для *рішень і компромісів* див. `docs/DECISIONS.md`; тут —
лише опис того, що є, без історії "чому саме так".

## Огляд архітектури

Дискретно-подієва (тік-циклова) симуляція лінії з 26 вузлів. Кожен тік
(`AgroDroneLine.tick(elapsed_time)`) послідовно оновлює: ресурси
(`ResourceManager`), стан кожного вузла (`ProductionNode.tick()` →
`update_status()`), стан його поточної операції (`ProductionOperation`).

```
AgroDroneLine
 ├─ ResourceManager  — склад ресурсів/деталей, резервування (RequestRes)
 ├─ ProductionPlanner — черга завдань, зв'язок вузол → наступна операція
 └─ units: list[ProductionNode]   (26 вузлів, id 1..26)
     ├─ reliability: Reliability  — контейнер розподілів надійності вузла
     │   ├─ reliability          — TimeDependentExponential (λ безвідмовності,
     │   │                          старіння), джерело порогу REPAIR (D2)
     │   ├─ failure_frequency    — TimeDependentExponential, діагностичне
     │   │                          поле, на FSM не впливає (D2)
     │   └─ maintenance_interval — TimeDependentLogNormal, джерело порогу
     │                              MAINTENANCE, якщо T_pm не задано (D3)
     ├─ operations: list[ProductionOperation]
     │   └─ efficiency: Efficiency — розподіли тривалості/якості операції
     ├─ status: NodeState  (IDLE | WAITING_FOR_RESOURCE | WORKING |
     │                       MAINTENANCE | REPAIR | FAILURE)
     └─ T_pm: float | None  — фіксований період ТО для параметричного
                              дослідження 4.2 (вузли 2-16, парк 3D-друку);
                              None для решти вузлів (природний розподіл)
```

## Вузли (`ProductionNode`)

Ідентифікатори `id` 1..26. Вузол 1 — постачання філаменту (Type0), вузли
2-16 — парк 3D-друку (15 однотипних принтерів, беруть участь у
параметричному дослідженні T_pm), вузли 17-21 — складання/пост-обробка,
22-26 — фінальні операції/пакування (точні призначення — `AgroDroneLine.py`,
`node_paramsN`/`efficiency_paramsN`/`reliability_paramsN`, N=1..26).

FSM вузла (`EnumsLine.NodeState`): `IDLE → WORKING → (REPAIR | IDLE-цикл із
MAINTENANCE на межі операцій) → IDLE`. Детально — `docs/DECISIONS.md` D2/D3.

## Операції (`ProductionOperation`)

Стан `OperationState`: `IDLE | WAITING_FOR_RESOURCE | EXECUTING | LETUP |
BLOCKED_BY_AGENT`. Тривалість/успішність семплюється з `Efficiency`
(`NormalDistribution`, `UniformDistribution`, `IncreasingParameter`,
`DecreasingParameter`, `ConstantParameter` — див. `Efficiency.py`).

## Точки інтеграції DQN (стаття 3)

`NodeAgent` / `ResourceAgent` — порожні класи-стаби. Призначені для
DQN-агента, що керуватиме параметрами надійності/ефективності в статті 3
(окремий репозиторій, форк цього коду; тут навмисно не реалізовано —
див. `/areas/article-3-dqn.md` у нотатках проєкту та обговорення
розмежування статей 1/3).

## Джерело параметрів

Числові значення `node_paramsN`/`efficiency_paramsN`/`reliability_paramsN`
(λ, μ, σ, тривалості) — плейсхолдер у поточній версії; фізичне обґрунтування
(паспортні характеристики обладнання / експертні оцінки / довідники
надійності) не закрито — див. `docs/DECISIONS.md` D7 і
`validation/validation_reliability_params.md`.
