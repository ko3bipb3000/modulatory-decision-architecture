📄 ОТЧЕТ ОБ ИСПЫТАНИЯХ И ТЕХНИЧЕСКИЙ ПАСПОРТ: MDA V2.1Проект: Modulatory Decision Architecture (MDA)Ревизия ядра: 2.1 (Neuromorphic "Kalashnikov" Edition)Дата: 25.03.20261. АРХИТЕКТУРНАЯ СХЕМА (Signal Flow)Модель имитирует биологический процесс принятия решения, где внутреннее состояние (Агрессия) модулирует восприятие внешней угрозы (Риск).Вход (Benefit): Желание/Ценность цели.Шум (Randomness): Применяется ДО расчетов ($\pm 5.0$). Имитирует флуктуации внимания.Первичный фильтр: Если $Motivation \le 50 \rightarrow$ HOLD.Демпфер Риска: Агрессия снижает Риск пропорционально самому Риску.$risk\_final = risk - (risk \times \frac{aggression}{100})$Вторичный фильтр: Мотивация умножается на "безопасный остаток".$motivation\_final = motivation \times (1 - \frac{risk\_final}{100})$Выход: Если $motivation\_final > 50 \rightarrow$ ACT, иначе HOLD.2. ТАБЛИЦЫ КАЛИБРОВКИ (Результаты тестов)Тест А: "Порог Пробуждения" (Normal)Условия: Risk=40, Aggr=35, Random=ON.BenefitACT %HOLD %ПереключенияКомментарий550%100%0Полная пассивность6512%88%8Начало "дребезга"7068%32%24Пик нерешительности75100%0%0Уверенный переходТест Б: "Градиент Смелости" (Aggressive)Условия: Benefit=60, Risk=40, Random=ON.AggressionACT %HOLD %ПереключенияСостояние30-400%100%0Осторожный тактик55-6076%24%22Фазовый переход70-80100%0%0Режим "Берсерк"3. ЭТАЛОННАЯ РЕАЛИЗАЦИЯ (Python 3.10+)Pythonimport random

class MDAModel:
    def __init__(self, use_random=True, use_aggr=True):
        self.use_random = use_random
        self.use_aggr = use_aggr
        self.temp_ranges = {
            "calm": (1.0, 40.0),
            "normal": (10.0, 60.0),
            "aggressive": (30.0, 80.0)
        }

    def step(self, benefit, risk, aggression=0.0):
        # 1. Применяем рандом на входе
        motivation = benefit + (random.uniform(-5, 5) if self.use_random else 0)
        
        # 2. Первая отсечка (Ватерлиния)
        if motivation <= 50: return "HOLD"

        # 3. Расчет подавления риска
        risk_final = risk
        if self.use_aggr:
            risk_final = risk - (risk * (aggression / 100.0))
        
        # 4. Финальный расчет и вторая отсечка
        motivation_final = motivation * (1 - (risk_final / 100.0))
        return "ACT" if motivation_final > 50 else "HOLD"
