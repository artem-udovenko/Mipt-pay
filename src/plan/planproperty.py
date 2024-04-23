from typing import Optional


class PlanProperty:
    """ An object that stores a unit of information for a specific plan. """

    pass


class Commission(PlanProperty):
    commission: float
    increased_commission: float

    def __init__(self, commission: float, increased_commission: Optional[float] = None):
        self.commission = commission
        if increased_commission is not None:
            self.increased_commission = increased_commission
        else:
            self.increased_commission = commission

    def info(self) -> str:
        return f"""Комиссия, начисляемая или взимаемая банком: {self.commission}
        (Комиссия при ненадежном аккаунте: {self.increased_commission})"""

class Period(PlanProperty):
    period: int
    decreased_period: int

    def __init__(self, period: int, decreased_period: Optional[int] = None):
        self.period = period
        if decreased_period is not None:
            self.decreased_period = decreased_period
        else:
            self.decreased_period = period

    def info(self) -> str:
        return f"""Срок вклада: {self.period}
        (Срок при ненадежном аккаунте: {self.decreased_period})"""

class LowerLimit(PlanProperty):
    lower_limit: float
    decreased_lower_limit: float

    def __init__(self, lower_limit: float, decreased_lower_limit: Optional[float] = None):
        self.lower_limit = lower_limit
        if decreased_lower_limit is not None:
            self.decreased_lower_limit = decreased_lower_limit
        else:
            self.decreased_lower_limit = lower_limit

    def info(self) -> str:
        return f"""Минимальный остаток: {self.lower_limit}
        (Минимальный остаток при ненадежном аккаунте: {self.decreased_lower_limit})"""

class UpperLimit(PlanProperty):
    upper_limit: float
    decreased_upper_limit: float

    def __init__(self, upper_limit: float, decreased_upper_limit: Optional[float] = None):
        self.upper_limit = upper_limit
        if decreased_upper_limit is not None:
            self.decreased_upper_limit = decreased_upper_limit
        else:
            self.decreased_upper_limit = upper_limit

    def info(self) -> str:
        return f"""Максимальный балланс: {self.upper_limit}
        (Максимальный балланс при ненадежном аккаунте: {self.decreased_upper_limit})"""

class TransferLimit(PlanProperty):
    transfer_limit: float
    decreased_transfer_limit: float

    def __init__(self, transfer_limit: float, decreased_transfer_limit: Optional[float] = None):
        self.transfer_limit = transfer_limit
        if decreased_transfer_limit is not None:
            self.decreased_transfer_limit = decreased_transfer_limit
        else:
            self.decreased_transfer_limit = transfer_limit

    def info(self) -> str:
        return f"""Лимит на переводы: {self.transfer_limit}
        (Лимит на переводы при ненадежном аккаунте: {self.decreased_transfer_limit})"""
