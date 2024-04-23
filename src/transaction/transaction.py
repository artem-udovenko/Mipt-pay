from inspect import currentframe as cf
import src


class Transaction:
    """ Any monetary transaction occurs with the creation of a transaction
    (so admins can track and/or cancel them). """

    __id: int
    __departure: int
    __destination: int
    __amount: float
    __status: int  # 0 - in progress, 1 - approved, -1 - cancelled, -2 - reverted

    def __init__(self, ident: int = None, departure: int = None, destination: int = None, amount: float = None, status: int = None):
        self.__departure = departure
        self.__destination = destination
        self.__amount = amount
        if ident is not None:
            self.__id = ident
            self.__status = status
        else:
            self.__status = 0
            self.__id = src.SingleDO.DO().put(self, False) # Transaction closes later


    @property
    def id(self):
        return self.__id

    @property
    def amount(self):
        return self.__amount

    @property
    def status(self):
        return self.__status

    @property
    def departure(self):
        return self.__departure

    @property
    def destination(self):
        return self.__destination

    def prove(self):
        self.__status = 1

    def cancel(self):
        self.__status = -1

    def revert(self):
        self.__status = -2
