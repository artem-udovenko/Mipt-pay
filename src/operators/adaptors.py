import src
from datetime import datetime
from typing import Optional


class Adaptor:
    def create_bank(self, bank: src.Bank):
        model = src.BankModel(name=bank.name)
        model.save()
        return model

    def create_person(self, person: src.Person, user):
        model = src.PersonModel(name=person.name, surname=person.surname, address=person.address, passport=int(person.passport.replace(" ", "")), user=user)
        model.save()
        return model

    def fill_person(self, model, person: src.Person):
        model.name = person.name
        model.surname = person.surname
        model.address = person.address
        model.passport = int(person.passport.replace(" ", ""))

    def create_client(self, client: src.Client, bank, person):
        # print(bank.name)
        model = src.ClientModel(bank=bank, person=person, name=client.name, surname=client.surname, address=(client.address if client.address is not None else ""), passport=(int(client.passport) if client.passport is not None else 0), precarious=client.precarious)
        model.save()
        return model

    def create_plan(self, plan: src.Plan, bank):
        name = bank.name
        model = src.PlanModel(name="TEMPORARY", bank=bank, commission=0, increased_commission=0, period=0, decreased_period=0, lower_limit=0, decreased_lower_limit=0, upper_limit=0, decreased_upper_limit=0, transfer_limit=0, decreased_transfer_limit=0)
        category: src.PlanCategoryModel
        if isinstance(plan, src.DebitPlan):
            category = src.PlanCategoryModel.objects.get(name='Debit')
            model.category = category
            name += f" debit "
        elif isinstance(plan, src.DepositPlan):
            category = src.PlanCategoryModel.objects.get(name='Deposit')
            model.category = category
            name += f" deposit "
        elif isinstance(plan, src.CreditPlan):
            category = src.PlanCategoryModel.objects.get(name='Credit')
            model.category = category
            name += f" credit "
        model.save()
        model.name = name + str(model.id)
        if category.commission:
            model.commission = plan.commission
            model.increased_commission = plan.increased_commission
        if category.period:
            model.period = plan.period
            model.decreased_period = plan.decreased_period
        if category.lower_limit:
            model.lower_limit = plan.lower_limit
            model.decreased_lower_limit = plan.decreased_lower_limit
        if category.upper_limit:
            model.upper_limit = plan.upper_limit
            model.decreased_lower_limit = plan.decreased_lower_limit
        if category.transfer_limit:
            model.transfer_limit = plan.transfer_limit
            model.decreased_transfer_limit = plan.decreased_transfer_limit
        model.save()
        return model

    def create_account(self, account: src.Account, bank, client, plan):
        model = src.AccountModel(bank=bank, owner=client, opened=account.opened, money=account.money, transfer=account.transfer, plan=plan)
        if isinstance(account, src.DepositAccount):
            model.freeze_date = account.freeze_date
        else:
            model.freeze_date = 0
        model.save()
        return model

    def create_transaction(self, transaction: src.Transaction):
        model = src.TransactionModel(departure=transaction.departure, destination=transaction.destination, amount=transaction.amount, status=transaction.status)
        model.save()
        return model

    def set_date(self):
        model, created = src.DiaryModel.objects.get_or_create(parameter="Date")
        model.value = str(datetime.now())
        model.save()
        return model

    def get_bank(self, ident: int) -> src.Bank:
        model = src.BankModel.objects.get(id=ident)
        clients = [it.id for it in src.ClientModel.objects.filter(bank=model)]
        accounts = [it.id for it in src.AccountModel.objects.filter(bank=model)]
        plans = [it.id for it in src.PlanModel.objects.filter(bank=model)]
        return src.Bank(model.id, model.name, clients, accounts, plans)

    def get_plan(self, ident: int) -> src.Plan:
        model = src.PlanModel.objects.get(id=ident)
        category = model.category
        if category.name == "Debit":
            return src.DebitPlan(ident, model.transfer_limit, model.decreased_transfer_limit, None)
        elif category.name == "Deposit":
            return src.DepositPlan(model.id, model.period, model.decreased_period, model.commission, model.increased_commission, model.transfer_limit, model.decreased_transfer_limit, None)
        elif category.name == "Credit":
            return src.CreditPlan(model.id, model.lower_limit, model.decreased_lower_limit, model.commission, model.increased_commission, model.transfer_limit, model.decreased_transfer_limit, None)

    def get_client(self, ident: int) -> src.Client:
        model = src.ClientModel.objects.get(id=ident)
        return src.Client(model.id, model.name, model.surname, model.address, str(model.passport), model.precarious)

    def get_account(self, ident: int) -> src.Account:
        model = src.AccountModel.objects.get(id=ident)
        print("When getting", model.money)
        if model.plan.category.name == "Debit":
            obj = src.DebitAccount(model.id, model.owner.id, model.opened, model.money, model.transfer, model.plan.id, None)
            print("In adapter", obj.money)
            return obj
        elif model.plan.category.name == "Deposit":
            return src.DepositAccount(model.id, model.owner.id, model.opened, model.money, model.transfer, model.freeze_date, model.plan.id, None)
        elif model.plan.category.name == "Credit":
            return src.CreditAccount(model.id, model.owner.id, model.opened, model.money, model.transfer, model.plan.id, None)

    def get_transaction(self, ident: int):
        model = src.TransactionModel.objects.get(id=ident)
        return src.Transaction(model.id, model.departure.id, model.destinations.id, model.amount, model.status)

    def get_person(self, ident: int):
        model = src.PersonModel.objects.get(id=ident)
        clients = [it.id for it in src.ClientModel.objects.filter(person=model)]
        return src.Person(model.id, model.name, model.surname, model.address, model.passport, clients)

    def multy_get(self, ident: int, cls: str):
        if cls == "Bank":
            return self.get_bank(ident)
        elif cls == "Plan":
            return self.get_plan(ident)
        elif cls == "Client":
            return self.get_client(ident)
        elif cls == "Account":
            return self.get_account(ident)
        elif cls == "Transaction":
            return self.get_transaction(ident)
        elif cls == "Person":
            return self.get_person(ident)
        else:
            print("error in multy_get")
            return None


class SingleAdaptor:
    """Singleton wrapper for Adopator class"""
    __adaptor: Optional[Adaptor] = None

    def __init__(self):
        pass

    @classmethod
    def adaptor(cls) -> Adaptor:
        if SingleAdaptor.__adaptor is None:
            SingleAdaptor.__adaptor = Adaptor()
        return SingleAdaptor.__adaptor
