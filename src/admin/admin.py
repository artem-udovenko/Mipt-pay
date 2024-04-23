import src
from typing import Optional


class Admin:
    """ Admin is an aggregator of the project's structural classes.
    Provides access to comprehensive information about the objects. """

    def account_info(self, account):
        account = src.SingleDO.DO().get(account, "Account")
        ret = f"""id: {account.id}
        owner: {account.owner}
        opened: {account.opened}
        money: {account.money}
        transfer: {account.transfer}
        plan: {account.plan}"""
        src.SingleDO.DO().done_with(account.id, "Account")
        return ret

    def bank_info(self, bank):
        bank = src.SingleDO.DO().get(bank, "Bank")
        ret = f"""id: {bank.id}
        name: {bank.name}
        clients: {bank.clients}
        accounts: {bank.accounts}
        plans: {bank.plans}"""
        src.SingleDO.DO().done_with(bank.id, "Bank")
        return ret

    def client_info(self, client):
        client = src.SingleDO.DO().get(client, "Client")
        ret = f"""id: {client.id}
        name: {client.name}
        surname: {client.surname}
        address: {client.address}
        passport: {client.passport}
        precarious: {client.precarious}"""
        src.SingleDO.DO().done_with(client.id, "Client")
        return ret

    def person_info(self, person):
        person = src.SingleDO.DO().get(person, "Person")
        ret = f"""id: {person.id}
        login: {person.log_in}
        password: {person.password}
        name: {person.name}
        surname: {person.surname}
        address: {person.address}
        passport: {person.passport}
        banks: {person.banks}
        accounts: {person.accounts}
        plans: {person.plans}"""
        src.SingleDO.DO().done_with(person.id, "Person")
        return ret

    def plan_info(self, plan):
        plan = src.SingleDO.DO().get(plan, "Plan")
        ret = f"""id: {plan.id}
        transfer_limit: {plan.transfer_limit}
        decreased_transfer_limit: {plan.decreased_transfer_limit}"""
        src.SingleDO.DO().done_with(plan.id, "Plan")
        return ret

    def transaction_info(self, transaction):
        transaction = src.SingleDO.DO().get(transaction, "Transaction")
        ret = f"""id: {transaction.id}
        departure: {transaction.departure}
        destination: {transaction.destination}
        amount: {transaction.amount}
        status: {transaction.status}"""
        src.SingleDO.DO().done_with(transaction.id, "Transaction")
        return ret

    def revert_transaction(self, trans: int) -> bool:
        transaction = src.SingleDO.DO().get(trans, "Transaction")
        if transaction is None:
            return False
        transaction.revert()
        flag = True
        if transaction.departure:
            departure = src.SingleDO.DO().get(transaction.departure, "Account")
            flag = flag and departure.put_offer(transaction.amount)
            departure.transfer -= transaction.amount
            departure.money += transaction.amount
            src.SingleDO.DO().done_with(transaction.departure, "Transaction")
        if transaction.destination:
            destination = src.SingleDO.DO().get(transaction.destination, "Account")
            flag = flag and destination.get_offer(transaction.amount)
            destination.transfer -= transaction.amount
            destination.money -= transaction.amount
            src.SingleDO.DO().done_with(transaction.destination, "Transaction")
        return flag


class SingleAdmin:
    """Singleton wrapper for Admin class"""
    __admin: Optional[Admin] = None

    def __init__(self):
        pass

    @classmethod
    def admin(cls) -> Admin:
        if SingleAdmin.__admin is None:
            SingleAdmin.__admin = Admin()
        return SingleAdmin.__admin


