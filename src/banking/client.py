from inspect import currentframe as cf
from typing import Optional
import src

class Client:
    """ Personal account of the banking's client.
    One user can have many of them (one per banking). """

    __id: int # PK
    __name: str
    __surname: str
    __address: str
    __passport: str
    __precarious: bool

    def __init__(self, ident: int = None, name: str = None, surname: str = None, address: str = None, passport: str = None, precarious: bool = None, bank: int = None, person: int = None):
        self.__name = name
        self.__surname = surname
        if ident is not None:
            self.__id = ident
            self.__passport = passport
            self.__address = address
            self.__precarious = precarious
        else:
            self.__address = address if address != "NO_VALUE" else None
            self.__passport = passport if passport != "NO_VALUE" else None
            if passport == "NO_VALUE" or address == "NO_VALUE":
                self.__precarious = True
            self.__id = src.SingleDO.DO().put(self, False, bank, person)

    @property
    def precarious(self):
        src.available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__precarious

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def surname(self):
        return self.__surname

    @property
    def address(self):
        src.available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__address

    @property
    def passport(self):
        src.available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__passport

    @address.setter
    def address(self, address: str):
        src.available_from(cf(), "Bank", "ClientBuilder")
        self.__address = address

    @passport.setter
    def passport(self, passport: str):
        src.available_from(cf(), "Bank", "ClientBuilder")
        self.__passport = passport

    def update(self, address: str, passport: str):
        src.available_from(cf(), "Bank", "ClientBuilder")
        # print("Actually updating")
        self.__address = address
        self.__passport = passport
        self.validate()

    def validate(self):
        if self.passport is None or self.address is None:
            self.__precarious = True
        else:
            self.__precarious = False

