from inspect import currentframe as cf
from typing import List
import src

class Plan:
    """ The invoice rate. Information about fees and restrictions. """

    __id: int # PK

    def __init__(self, ident: int = None, bank: int = None):
        if ident is not None:
            self.__id = ident
        else:
            pass

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, ident: int):
        self.__id = ident

    def get_properties(self) -> List[src.PlanProperty]:
        return []

class DebitPlan(Plan):
    """ Debit rate. """

    __transfer_limit: float
    __decreased_transfer_limit: float

    @property
    def transfer_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__transfer_limit

    @transfer_limit.setter
    def transfer_limit(self, transfer_limit: float):
        self.__transfer_limit = transfer_limit

    @property
    def decreased_transfer_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__decreased_transfer_limit

    @decreased_transfer_limit.setter
    def decreased_transfer_limit(self, decreased_transfer_limit: float):
        self.__decreased_transfer_limit = decreased_transfer_limit

    def __init__(self, ident: int = None, transfer_limit: float = None, decreased_transfer_limit: float = None, bank: int = None):
        super().__init__(ident, bank)
        self.transfer_limit = transfer_limit
        self.decreased_transfer_limit = decreased_transfer_limit
        if ident is None:
            from src.operators.dataoperator import DataOperator, SingleDO
            self.id = SingleDO.DO().put(self, False, bank)

            src.SingleDO.DO().done_with(self.id, "Plan")


    def get_properties(self) -> List[src.PlanProperty]:
        return [src.TransferLimit(self.__transfer_limit, self.__decreased_transfer_limit)]


class DepositPlan(Plan):
    """ Deposit rate. """

    __period: int
    __decreased_period: int
    __commission: float
    __increased_commission: float
    __transfer_limit: float
    __decreased_transfer_limit: float

    @property
    def transfer_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__transfer_limit

    @transfer_limit.setter
    def transfer_limit(self, transfer_limit: float):
        self.__transfer_limit = transfer_limit

    @property
    def decreased_transfer_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__decreased_transfer_limit

    @decreased_transfer_limit.setter
    def decreased_transfer_limit(self, decreased_transfer_limit: float):
        self.__decreased_transfer_limit = decreased_transfer_limit

    @property
    def period(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__period

    @period.setter
    def period(self, period: int):
        self.__period = period

    @property
    def decreased_period(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__decreased_period

    @decreased_period.setter
    def decreased_period(self, decreased_period: float):
        self.__decreased_period = decreased_period

    @property
    def commission(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__commission

    @commission.setter
    def commission(self, commission: float):
        self.__commission = commission

    @property
    def increased_commission(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__increased_commission

    @increased_commission.setter
    def increased_commission(self, increased_commission: float):
        self.__increased_commission = increased_commission

    def __init__(self, ident: int = None, period: int = None, decreased_period: int = None,
                 commission: float = None, increased_commission: float = None,
                 transfer_limit: float = None, decreased_transfer_limit: float = None, bank: int = None):
        super().__init__(ident, bank)
        self.__period = period
        self.__decreased_period = decreased_period
        self.__commission = commission
        self.__increased_commission = increased_commission
        self.__transfer_limit = transfer_limit
        self.__decreased_transfer_limit = decreased_transfer_limit
        if ident is None:
            from src.operators.dataoperator import DataOperator, SingleDO
            self.id = SingleDO.DO().put(self, False, bank)

            src.SingleDO.DO().done_with(self.id, "Plan")

    def get_properties(self) -> List[src.PlanProperty]:
        return [src.TransferLimit(self.__transfer_limit, self.__decreased_transfer_limit),
                src.Period(self.__period, self.__decreased_period),
                src.Commission(self.__commission, self.__increased_commission)]



class CreditPlan(Plan):
    """ Credit rate. """

    __lower_limit: float
    __decreased_lower_limit: float
    __commission: float
    __increased_commission: float
    __transfer_limit: float
    __decreased_transfer_limit: float

    @property
    def transfer_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__transfer_limit

    @transfer_limit.setter
    def transfer_limit(self, transfer_limit: float):
        self.__transfer_limit = transfer_limit

    @property
    def decreased_transfer_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__decreased_transfer_limit

    @decreased_transfer_limit.setter
    def decreased_transfer_limit(self, decreased_transfer_limit: float):
        self.__decreased_transfer_limit = decreased_transfer_limit

    @property
    def lower_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__lower_limit

    @lower_limit.setter
    def lower_limit(self, lower_limit: float):
        self.__lower_limit = lower_limit

    @property
    def decreased_lower_limit(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__decreased_lower_limit

    @decreased_lower_limit.setter
    def decreased_lower_limit(self, decreased_lower_limit: float):
        self.__decreased_lower_limit = decreased_lower_limit

    @property
    def commission(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__commission

    @commission.setter
    def commission(self, commission: float):
        self.__commission = commission

    @property
    def increased_commission(self):
        src.available_from(cf(), "Bank", "Account")
        return self.__increased_commission

    @increased_commission.setter
    def increased_commission(self, increased_commission: float):
        self.__increased_commission = increased_commission

    def __init__(self, ident: int = None, lower_limit: float = None, decreased_lower_limit: float = None,
                 commission: float = None, increased_commission: float = None,
                 transfer_limit: float = None, decreased_transfer_limit: float = None, bank: int = None):
        super().__init__(ident, bank)
        self.__lower_limit = lower_limit
        self.__decreased_lower_limit = decreased_lower_limit
        self.__commission = commission
        self.__increased_commission = increased_commission
        self.__transfer_limit = transfer_limit
        self.__decreased_transfer_limit = decreased_transfer_limit
        if ident is None:
            from src.operators.dataoperator import DataOperator, SingleDO
            self.id = SingleDO.DO().put(self, False, bank)

            src.SingleDO.DO().done_with(self.id, "Plan")

    def get_properties(self) -> List[src.PlanProperty]:
        return [src.TransferLimit(self.__transfer_limit, self.__decreased_transfer_limit),
                src.LowerLimit(self.__lower_limit, self.__decreased_lower_limit),
                src.Commission(self.__commission, self.__increased_commission)]
