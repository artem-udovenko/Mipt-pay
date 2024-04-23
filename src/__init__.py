import os
import django
import toml

import miptpay.tests.sampledata

TIME: str
with open("pyproject.toml", "r") as f:
    data = toml.load(f)
    print(data)
    TIME = data["constant"]["time"]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.miptpaydj.miptpaydj.settings')

if miptpay.tests.sampledata.SETUP_MODE:
    django.setup()

from src.miptpaydj.mainapp.models import BankModel, PersonModel, ClientModel, PlanCategoryModel, PlanModel, AccountModel, TransactionModel, DiaryModel

from src.miptpaydj.mainapp import apps

from src.miptpaydj.mainapp import views

from src.tools.accesstools import available_from

from src.plan.planproperty import PlanProperty, Commission, Period, LowerLimit, UpperLimit, TransferLimit
from src.plan.plan import Plan, DebitPlan, DepositPlan, CreditPlan
from src.plan.planfactory import PlanFactory

from src.banking.client import Client
from src.banking.clientbuilder import ClientBuilder

from src.account.account import Account, DebitAccount, DepositAccount, CreditAccount
from src.account.accountfactory import AccountFactory

from src.transaction.transaction import Transaction

from src.banking.bank import Bank
from src.banking.crosspaymentsystem import CrossPaymentSystem, system
from src.banking.crosspayment import SingleSPF

from src.users.person import Person
from src.admin.admin import Admin, SingleAdmin

from src.operators.timekeeper import TimeKeeper, SingleTK
from src.operators.dataoperator import DataOperator, SingleDO
from src.operators.adaptors import Adaptor, SingleAdaptor


from django.contrib.auth.models import User

__all__ = ['available_from',
           'PlanProperty', 'Commission', 'Period', 'LowerLimit', 'UpperLimit', 'TransferLimit',
           'Plan', 'DebitPlan', 'DepositPlan', 'CreditPlan',
           'PlanFactory',
           'Client', 'ClientBuilder',
           'Account', 'DepositAccount', 'DebitAccount', 'CreditAccount',
           'AccountFactory',
           'Transaction',
           'Bank',
           'CrossPaymentSystem', 'system',
           'get_cpf',
           'TimeKeeper', 'SingleTK',
           'DataOperator', 'SingleDO',
           'Adaptor', 'SingleAdaptor',
           'Person',
           'Admin', 'SingleAdmin',
           'BankModel', 'PersonModel', 'ClientModel', 'PlanCategoryModel', 'PlanModel', 'AccountModel', 'TransactionModel', 'DiaryModel',
           'User',
           'apps',
           'views',
           ]
