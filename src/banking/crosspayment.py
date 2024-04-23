from typing import Optional

import src


""" The module executing the singleton pattern for the class CrossPaymentSystem. """

def get_cpf():
    if src.system is None:
        src.system = src.CrossPaymentSystem()
    return src.system

class SingleSPF:
    """Singleton wrapper for TimeKeeper class"""
    __cpf: Optional[src.CrossPaymentSystem] = None

    def __init__(self):
        pass

    @classmethod
    def CPF(cls) -> src.CrossPaymentSystem:
        if SingleSPF.__cpf is None:
            SingleSPF.__cpf = src.CrossPaymentSystem()
        return SingleSPF.__cpf
