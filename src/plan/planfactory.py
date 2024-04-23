import src


class PlanFactory:
    @staticmethod
    def create_debit_plan(transfer_limit: src.TransferLimit, bank: int):
        return src.DebitPlan(None, transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit, bank)

    @staticmethod
    def create_deposit_plan(transfer_limit: src.TransferLimit,
                            period: src.Period, commission: src.Commission, bank: int):
        return src.DepositPlan(None, period.period, period.decreased_period,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit, bank)

    @staticmethod
    def create_credit_plan(transfer_limit: src.TransferLimit,
                            lower_limit: src.LowerLimit, commission: src.Commission, bank: int):
        return src.CreditPlan(None, lower_limit.lower_limit, lower_limit.decreased_lower_limit,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit, bank)
