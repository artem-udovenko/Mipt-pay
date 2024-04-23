from typing import Dict, List
import src


class Person:
    """ The personal account of a real users - the user of the application. """

    # TODO: logins, passwords, etc
    __id: int  # PK
    __login: str
    __password: str
    __name: str
    __surname: str
    __address: str
    __passport: str
    __clients: List[int]

    def __init__(self, ident: int = None, name: str = None, surname: str = None, address: str = None, passport: str = None, clients: List[int] = None):
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        if ident is not None:
            self.__id = ident
            self.__clients = clients
        else:
            print(f"It is deprecated to construct person with no id ({ident}).")
            self.__clients = []
            self.__id = src.DataOperator().put(self, True)

    def log_in(self, login: str, password: str):
        # TODO: Сделать систему проверки пользователя
        pass

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
        return self.__address

    @property
    def passport(self):
        return self.__passport

    def update(self, address: str, passport: str):
        self.__address = address
        self.__passport = passport


