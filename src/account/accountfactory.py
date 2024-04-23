import src

class AccountFactory:
    """ Factory (Factory method) class for creating Account instances. """

    @staticmethod
    def create(owner: int, plan: src.Plan, bank: int) -> src.Account:
        if isinstance(plan, src.DepositPlan):
            return src.DepositAccount(None, owner, None, None, None, None, plan.id, bank)
        elif isinstance(plan, src.CreditPlan):
            return src.CreditAccount(None, owner, None, None, None, plan.id, bank)
        else:
            return src.DebitAccount(None, owner, None, None, None, plan.id, bank)