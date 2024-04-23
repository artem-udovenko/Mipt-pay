from typing import Optional
import src


class CrossPaymentSystem:
    """ Class providing an opportunity to conduct interbank transactions. """


    def valid_transfer(self, dep_bank: int, departure: int, dest_bank: int, destination: int, sender: int,
                 amount: float) -> bool:
        dep_bank_obj = src.SingleDO.DO().get(dep_bank, "Bank")
        dest_bank_obj = src.SingleDO.DO().get(dest_bank, "Bank")
        if not dep_bank_obj.valid_client(departure, sender):
            src.SingleDO.DO().done_with(dep_bank, "Bank")
            src.SingleDO.DO().done_with(dest_bank, "Bank")
            return False
        trans = src.Transaction(None, departure, destination, amount, None)
        if dep_bank_obj.put_offer(departure, amount) and dest_bank_obj.put_offer(destination, amount):
            dep_bank_obj.do_get(departure, amount)
            dest_bank_obj.do_put(destination, amount)
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep_bank, "Bank")
            src.SingleDO.DO().done_with(dest_bank, "Bank")
            trans.prove()
            return True
        else:
            trans.cancel()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep_bank, "Account")
            src.SingleDO.DO().done_with(dest_bank, "Account")
            return False


    def transfer(self, dep_bank: int, departure: int, dest_bank: int, destination: int, amount: float) -> bool:
        dep_bank_obj = src.SingleDO.DO().get(dep_bank, "Bank")
        dest_bank_obj = src.SingleDO.DO().get(dest_bank, "Bank")
        trans = src.Transaction(None, departure, destination, amount, None)
        if dep_bank_obj.put_offer(departure, amount) and dest_bank_obj.put_offer(destination, amount):
            dep_bank_obj.do_get(departure, amount)
            dest_bank_obj.do_put(destination, amount)
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep_bank, "Bank")
            src.SingleDO.DO().done_with(dest_bank, "Bank")
            trans.prove()
            return True
        else:
            trans.cancel()
            src.SingleDO.DO().done_with(trans.id, "Transaction")
            src.SingleDO.DO().done_with(dep_bank, "Account")
            src.SingleDO.DO().done_with(dest_bank, "Account")
            return False


system: Optional[CrossPaymentSystem] = None