from typing import Optional
import src


class ClientBuilder:
    """ Builder class for creating Client instances. """

    __brick: Optional[src.Client]
    __bank: int
    __person: int

    def bank(self, bank: int):
        self.__bank = bank

    def person(self, person: int):
        self.__person = person

    def reset(self, name: str, surname: str):
        self.__brick = src.Client(None, name, surname, "NO_VALUE", "NO_VALUE", None, self.__bank, self.__person)

    def address(self, address: str):
        self.__brick.address = address

    def passport(self, passport: str):
        self.__brick.passport = passport

    def get(self) -> src.Client:
        brick = self.__brick
        brick.validate()
        self.__brick = None
        return brick