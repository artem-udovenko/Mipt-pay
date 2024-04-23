from typing import List, Optional
import re
from inspect import currentframe as cf
import src


class Bank:
    """ The banking has plans, accounts and clients linked to it.
    At the middle level, the interaction takes place through it. """

    __id: int # PK
    __name: str
    __clients: List[int]
    __accounts: List[int]
    __plans: List[int]
    __registrator: src.ClientBuilder

    # def __init__(self, name: str):
    #     self.__clients = []
    #     self.__accounts = []
    #     self.__plans = []
    #     self.__name = name
    #     self.__registrator = src.ClientBuilder()
    #     self.__id = src.SingleDO.DO().put(self, False)
    #
    # def __init__(self, ident: int, name: str, clients: List[int], accounts: List[int], plans: List[int]):
    #     src.available_from(cf())  # not available for non-gods
    #     self.__id = ident
    #     self.__name = name
    #     self.__clients = clients
    #     self.__accounts = accounts
    #     self.__plans = plans
    #     self.__registrator = src.ClientBuilder()

    def __init__(self, ident: int = None, name: str = None, clients: List[int] = None, accounts: List[int] = None, plans: List[int] = None):
        self.__name = name
        self.__registrator = src.ClientBuilder()
        if ident is not None:
            self.__id = ident
            self.__clients = clients
            self.__accounts = accounts
            self.__plans = plans
        else:
            self.__clients = []
            self.__accounts = []
            self.__plans = []
            self.__id = src.SingleDO.DO().put(self, False)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def plans(self):
        return self.__plans

    @property
    def accounts(self):
        return self.__accounts

    @property
    def clients(self):
        return self.__clients

    def register(self, name: str, surname: str, address: str, passport: str, person: int) -> Optional[int]:
        # for id in self.__clients:
        #     client = src.SingleDO.DO().get(id, "Client")
        #     if client.name == name and client.surname == surname:
        #         return None
        pattern = re.compile("\d{10}")
        if passport != "NO_VALUE":
            passport = passport.replace(" ", "")
            if not pattern.match(passport):
                return None
        self.__registrator.bank(self.__id)
        self.__registrator.person(person)
        self.__registrator.reset(name, surname)
        if address != "NO_VALUE":
            self.__registrator.address(address)
        if passport != "NO_VALUE":
            self.__registrator.passport(passport)
        client = self.__registrator.get().id
        if client is None:
            return None
        self.__clients.append(client)
        src.SingleDO.DO().done_with(client, "Client")
        return client

    def register_from_person(self, user: int) -> Optional[int]:
        person = src.SingleDO.DO().get(user, "Person")
        if person is None:
            return None
        self.__registrator.reset(person.name, person.surname)
        if person.address is not None:
            self.__registrator.address(person.address)
        if person.passport is not None:
            self.__registrator.passport(person.passport)
        client = self.__registrator.get().id
        if client is None:
            return None
        self.__clients.append(client)
        src.SingleDO.DO().done_with(client, "Client")
        src.SingleDO.DO().done_with(user, "Person")
        return client

    def add_plan(self, plan: int) -> Optional[int]:
        # for id in self.__plans:
        #     if id == plan.id:
        #         return None
        self.__plans.append(plan)
        # src.SingleDO.DO().done_with(plan.id, "Plan")
        return plan

    def open_account(self, owner: int, plan: int) -> Optional[int]:
        if not owner in self.__clients or not plan in self.__plans:
            # print(owner, self.__clients, plan, self.__plans)
            return None
        plan_obj = src.SingleDO.DO().get(plan, "Plan")
        if plan_obj is None:
            return None
        acc = src.AccountFactory.create(owner, plan_obj, self.id).id
        self.__accounts.append(acc)
        # src.SingleDO.DO().done_with(acc, "Account")
        src.SingleDO.DO().done_with(plan, "Plan")
        return acc

    def transfer(self, departure: int, destination: int, amount: int) -> bool:
        if not departure in self.__accounts or not destination in self.__accounts:
            return False
        dep: src.Account = src.SingleDO.DO().get(departure, "Account")
        dest: src.Account = src.SingleDO.DO().get(destination, "Account")
        if dest is None or dep is None:
            return False
        trans = src.Transaction(None, departure, destination, amount, None)
        if dep.get_offer(amount) and dest.put_offer(amount):
            dep.get(amount)
            dest.put(amount)
            trans.prove()
            src.SingleDO.DO().done_with(dep.id, "Account")
            src.SingleDO.DO().done_with(dest.id, "Account")
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            return True
        trans.cancel()
        src.SingleDO.DO().done_with(dep.id, "Account")
        src.SingleDO.DO().done_with(dest.id, "Account")
        src.SingleDO.DO().done_with(trans.id, "Transaction")
        return False

    def do_get(self, account: int, amount: float):
        src.available_from(cf(), "CrossPaymentSystem")
        dep = src.SingleDO.DO().get(account, "Account")
        if dep is None:
            src.SingleDO.DO().done_with(account, "Account")
            return None
        dep.get(amount)
        src.SingleDO.DO().done_with(account, "Account")

    def do_put(self, account: int, amount: float):
        src.available_from(cf(), "CrossPaymentSystem")
        dep = src.SingleDO.DO().get(account, "Account")
        if dep is None:
            src.SingleDO.DO().done_with(account, "Account")
            return None
        print(dep.money)
        dep.put(amount)
        print(dep.money)
        src.SingleDO.DO().done_with(account, "Account")

    def get(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        dep = src.SingleDO.DO().get(account, "Account")
        if dep is None:
            return False
        trans = src.Transaction(None, 0, account, amount, None)
        if dep.get_offer(amount):
            self.do_get(account, amount)
            trans.prove()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep.id, "Account")
            return True
        else:
            trans.cancel()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep.id, "Account")
            return False

    def valid_get(self, client: int, account: int, amount: float) -> bool:
        if account not in self.__accounts:
            return False
        if client not in self.__clients:
            return False
        dep = src.SingleDO.DO().get(account, "Account")
        if dep is None:
            return False
        if dep.owner() != client:
            src.SingleDO.DO().done_with(dep.id, "Account")
            return False
        trans = src.Transaction(0, account, amount)
        if dep.get_offer(amount):
            self.do_get(account, amount)
            trans.prove()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep.id, "Account")
            return True
        else:
            trans.cancel()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep.id, "Account")
            return False

    def put(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        dest = src.SingleDO.DO().get(account, "Account")
        if dest is None:
            return False
        trans = src.Transaction(None, account, 0, amount, None)
        if dest.put_offer(amount):
            self.do_put(account, amount)
            trans.prove()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dest.id, "Account")
            return True
        else:
            trans.cancel()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dest.id, "Account")
            return False

    def update(self, owner: int, address: str, passport: str) -> bool:
        pattern = re.compile("\d{10}")
        if passport is not None:
            passport = passport.replace(" ", "")
            if not pattern.match(passport):
                print(f"Passport {passport} does not match pattern")
                return False
        if owner not in self.__clients:
            return False
        else:
            client_obj = src.SingleDO.DO().get(owner, "Client")
            if client_obj is None:
                src.SingleDO.DO().done_with(owner, "Client")
                return False
            client_obj.update(address, passport)
            src.SingleDO.DO().done_with(owner, "Client")

    def valid_client(self, account: int, client: int) -> bool:
        if client not in self.__clients:
            return False
        account_obj = src.SingleDO.DO().get(account, "Account")
        ret = False
        if account_obj is not None:
            ret = account_obj.owner == client
        src.SingleDO.DO().done_with(account, "Account")
        return ret

    def get_offer(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        account_obj = src.SingleDO.DO().get(account, "Account")
        ret = False
        if account_obj is not None:
            ret = account_obj.get_offer(amount)
        src.SingleDO.DO().done_with(account, "Account")
        return ret

    def put_offer(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        account_obj = src.SingleDO.DO().get(account, "Account")
        ret = False
        if account_obj is not None:
            ret = account_obj.put_offer(amount)
        src.SingleDO.DO().done_with(account, "Account")
        return ret


