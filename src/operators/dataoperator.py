from typing import Dict, Union, List, Optional
import src


clients: Dict[int, List[Union[src.Client, int]]] = {}
clients_counter = 0

accounts: Dict[int, List[Union[src.Account, int]]] = {}
accounts_counter = 0

banks: Dict[int, List[Union[src.Bank, int]]] = {}
banks_counter = 0

plans: Dict[int, List[Union[src.Plan, int]]] = {}
plans_counter = 0

transactions: Dict[int, List[Union[src.Transaction, int]]] = {}
transactions_counter = 0

persons: Dict[int, List[Union[src.Person, int]]] = {}
persons_counter = 0


class DataOperator:
    """ The class of interaction of logic with the database.
    Stores (reserves) objects that are currently being used by the system. """

    def get(self, id: int, type: str) -> Union[src.Client, src.Bank, src.Account, src.Plan, src.Transaction, src.Person, None]:
        type_to_container = {
            "Client": clients,
            "Bank": banks,
            "Account": accounts,
            "Plan": plans,
            "Transaction": transactions,
            "Person": persons
        }
        container = type_to_container.get(type)
        if id not in container.keys() or container[id][1] == 0:
            print("Need to load", id)
            if id not in container.keys():
                container[id] = [None, 0]
            container[id][1] = 1
            adapter = __import__("src.operators.adaptors").SingleAdaptor.adaptor()
            container[id][0] = adapter.multy_get(id, type)
            return container[id][0]
        else:
            print("Already have", id)
            container[id][1] += 1
            return container[id][0]

    def put(self, obj, done: bool, *args) -> int:
        global clients, clients_counter
        global accounts, accounts_counter
        global banks, banks_counter
        global plans, plans_counter
        global transactions, transactions_counter
        global persons, persons_counter
        amount_in_use = 0 if done else 1
        print("Putting", type(obj), f"(available - {amount_in_use})", end='')
        adapter = __import__("src.operators.adaptors").SingleAdaptor.adaptor()
        if isinstance(obj, src.Client):
            bank = src.BankModel.objects.get(id=args[0])
            person = src.PersonModel.objects.get(id=args[1])
            model = adapter.create_client(obj, bank, person)
            clients[model.id] = [obj, amount_in_use]
            print(f" (set id = {model.id})")
            return model.id
        if isinstance(obj, src.Bank):
            model = adapter.create_bank(obj)
            banks[model.id] = [obj, amount_in_use]
            print(f" (set id = {model.id})")
            return model.id
        if isinstance(obj, src.Account):
            bank = src.BankModel.objects.get(id=args[0])
            client = src.ClientModel.objects.get(id=obj.owner)
            plan = src.PlanModel.objects.get(id=obj.plan)
            model = adapter.create_account(obj, bank, client, plan)
            accounts[model.id] = [obj, amount_in_use]
            print(f" (set id = {model.id})")
            return model.id
        if isinstance(obj, src.Plan):
            bank = src.BankModel.objects.get(id=args[0])
            model = adapter.create_plan(obj, bank)
            plans[model.id] = [obj, amount_in_use]
            print(f" (set id = {model.id})")
            return model.id
        if isinstance(obj, src.Transaction):
            model = adapter.create_transaction(obj)
            transactions[model.id] = [obj, amount_in_use]
            print(f" (set id = {model.id})")
            return model.id
        if isinstance(obj, src.Person):
            raise MemoryError("Putting Person is deprecated")

    def get_bank_by_name(self, name: str):
        for ident, bank in banks.items():
            if bank[0].name == name:
                return bank
        return None

    def get_client_by_name(self, name: str):
        for ident, client in clients.items():
            if client[0].name == name:
                return client


    def account_info(self) -> str:
        st = ""
        for id, account in accounts.items():
            st += account[0].info() + '\n'
        return st

    def banks(self):
        return banks

    def plans(self):
        return plans

    def clients(self):
        return clients

    def accounts(self):
        return accounts

    def transactions(self):
        return transactions

    def done_with(self, id: int, type: str) -> bool:
        print("Done with", id, f"({type})")
        type_to_container = {
            "Client": clients,
            "Bank": banks,
            "Account": accounts,
            "Plan": plans,
            "Transaction": transactions,
            "Person": persons
        }
        container = type_to_container.get(type, {})
        models = __import__("src.miptpaydj.mainapp.models")
        if id not in container.keys():
            return False
        else:
            container[id][1] -= 1
            if container[id][1] == 0:
                print("Saving", type, id)
                if type == "Client":
                    model = models.ClientModel.objects.get(id=id)
                    model.name = container[id][0].name
                    model.surname = container[id][0].surname
                    model.address = container[id][0].address if container[id][0].address is not None else "NO_VALUE"
                    model.passport = -1 if (container[id][0].passport is None or container[id][0].passport == "NO_VALUE") else int(container[id][0].passport)
                    model.precarious = container[id][0].precarious
                    model.save()
                elif type == "Bank":
                    model = models.BankModel.objects.get(id=id)
                    model.name = container[id][0].name
                    model.save()
                elif type == "Account":
                    model = models.AccountModel.objects.get(id=id)
                    model.opened = container[id][0].opened
                    model.money = container[id][0].money
                    model.transfer = container[id][0].transfer
                    if isinstance(container[id][0], src.DepositAccount):
                        model.freeze_date = container[id][0].freeze_date
                    model.save()
                elif type == "Plan":
                    model = models.PlanModel.objects.get(id=id)
                    if isinstance(container[id][0], src.DebitPlan):
                        model.transfer_limit = container[id][0].transfer_limit
                        model.decreased_transfer_limit = container[id][0].decreased_transfer_limit
                    elif isinstance(container[id][0], src.DepositPlan):
                        model.transfer_limit = container[id][0].transfer_limit
                        model.decreased_transfer_limit = container[id][0].decreased_transfer_limit
                        model.commission = container[id][0].commission
                        model.increased_commission = container[id][0].increased_commission
                        model.period = container[id][0].period
                        model.decreased_period = container[id][0].decreased_period
                    elif isinstance(container[id][0], src.CreditPlan):
                        model.transfer_limit = container[id][0].transfer_limit
                        model.decreased_transfer_limit = container[id][0].decreased_transfer_limit
                        model.commission = container[id][0].commission
                        model.increased_commission = container[id][0].increased_commission
                        model.lower_limit = container[id][0].lower_limit
                        model.decreased_lower_limit = container[id][0].decreased_lower_limit
                    model.save()
                elif type == "Transaction":
                    model = models.TransactionModel.objects.get(id=id)
                    model.amount = container[id][0].amount
                    model.status = container[id][0].status
                    model.save()
                elif type == "Person":
                    model = models.PersonModel.objects.get(id=id)
                    model.name = container[id][0].name
                    model.surname = container[id][0].surname
                    model.address = container[id][0].address
                    model.passport = -1 if (container[id][0].name is None or container[id][0].name == "NO_VALUE") else int(container[id][0].name)
                    model.save()
            return True

    def print_online(self, undefined: bool = False):
        print("Online objects:\n")
        for ident, bank in banks.items():
            if bank[1] > 0:
                print('\t', "Bank", ident, bank[1], bank[0].name)
        for ident, plan in plans.items():
            if plan[1] > 0:
                print('\t', "Plan", ident, plan[1])
        for ident, client in clients.items():
            if client[1] > 0:
                print('\t', "Client", ident, client[1], client[0].name)
        for ident, account in accounts.items():
            if account[1] > 0:
                print('\t', "Account", ident, account[1])
        for ident, person in persons.items():
            if person[1] > 0:
                print('\t', "Person", ident, person[1], person[0].name)
        for ident, transaction in transactions.items():
            if transaction[1] > 0:
                print('\t', "Transaction", ident, transaction[1])
        print("\nOffline objects:\n")
        for ident, bank in banks.items():
            if bank[1] == 0:
                print('\t', "Bank", ident, bank[1], bank[0].name)
        for ident, plan in plans.items():
            if plan[1] == 0:
                print('\t', "Plan", ident, plan[1])
        for ident, client in clients.items():
            if client[1] == 0:
                print('\t', "Client", ident, client[1], client[0].name)
        for ident, account in accounts.items():
            if account[1] == 0:
                print('\t', "Account", ident, account[1])
        for ident, person in persons.items():
            if person[1] == 0:
                print('\t', "Person", ident, person[1], person[0].name)
        for ident, transaction in transactions.items():
            if transaction[1] == 0:
                print('\t', "Transaction", ident, transaction[1])
        if undefined:
            print("\nWTF objects:\n")
            for ident, bank in banks.items():
                if bank[1] < 0:
                    print('\t', "Bank", ident, bank[1], bank[0].name)
            for ident, plan in plans.items():
                if plan[1] < 0:
                    print('\t', "Plan", ident, plan[1])
            for ident, client in clients.items():
                if client[1] < 0:
                    print('\t', "Client", ident, client[1], client[0].name)
            for ident, account in accounts.items():
                if account[1] < 0:
                    print('\t', "Account", ident, account[1])
            for ident, person in persons.items():
                if person[1] < 0:
                    print('\t', "Person", ident, person[1], person[0].name)
            for ident, transaction in transactions.items():
                if transaction[1] < 0:
                    print('\t', "Transaction", ident, transaction[1])
            print("\n")


class SingleDO:
    """Singleton wrapper for DataOperator class"""
    __dataoperator: Optional[DataOperator] = None

    def __init__(self):
        pass

    @classmethod
    def DO(cls) -> DataOperator:
        if SingleDO.__dataoperator is None:
            SingleDO.__dataoperator = DataOperator()
        return SingleDO.__dataoperator
