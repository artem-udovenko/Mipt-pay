from typing import Dict
import src


def input_int(left: int, right: int, message: str) -> int:
    while True:
        try:
            inp = int(input(message))
            if left != None:
                assert left <= inp
            if right != None:
                assert inp <= right
            break
        except:
            print("Некорректный ввод.")
    return inp


class UserInterface:  # TODO: Make singleton.
    """ A class that operates with a console interface. """

    __user: src.Person

    def login_and_register(self):
        print("""Вас приветствует MiptPay! Ваши действия:
                    1. Зарегестрироваться
                    2. Войти (в тестовом режиме эта функция недоступна)""")
        answer = input_int(1, 2, "Введите 1 или 2:")
        if answer == 1:
            login = str(input("Придумайте логин:"))
            password = str(input("Придумайте пароль:"))
            name = str(input("Введите ваше имя:"))
            surname = str(input("Введите вашу фамилию:"))
            address = str(input("Введите ваш адрес (enter для пропуска):"))
            if len(address) < 1:
                print("Пропущен ввод адреса. Данные можно будет дополнить позднее.")
                address = None
            passport = str(input("Введите ваш номер паспорта (формат: 00 00 000000) (enter для пропуска):"))
            if len(passport) < 1:
                print("Пропущен ввод паспорта. Данные можно будет дополнить позднее.")
                passport = None
            self.__user = src.Person(login, password, name, surname, address, passport)
            self.main_menu()
        elif answer == 2:
            login = str(input("Введите ваш логин:"))
            password = str(input("Введите ваш пароль:"))
            self.__user.log_in(login, password)
            self.main_menu()

    def open_plan(self):
        print("""Это меню открытия счёта пожалуйста введите банк в котором вы хотите открыть счёт: """)
        bank_name = str(input())
        if src.DataOperator().get_bank_by_name(bank_name) is None:
            print("Введённые банк не поддерживается нашей системой")
            self.open_plan()
        else:
            bank = src.DataOperator().get_bank_by_name(bank_name)
        print("Выберите счёт из предлагаемых данным банком:")
        plans: Dict[int, src.Plan] = {}
        counter = 1
        for ident in bank.plans:
            plan = src.DataOperator().get_cpf(ident, "Plan")
            plan_type = ""
            if isinstance(plan, src.DebitPlan):
                plan_type = "Дебетовый тариф"
            elif isinstance(plan, src.DepositPlan):
                plan_type = "Депозитный тариф"
            elif isinstance(plan, src.CreditPlan):
                plan_type = "Кредитный тариф"
            plans[counter] = plan
            properties = plan.get_properties()
            print(counter, ") ", plan_type, ":")
            for p in properties:
                print(p.info())
            counter += 1
        ans = input_int(0, counter - 1, "Введите номер:")
        plan = plans[ans]
        client_id = self.__user.banks[bank_name]
        new_account = bank.open_account(client_id, plan.id)
        if new_account is None:
            print("Такой счёт уже зарегистрирован")
            self.main_menu()
        self.__user.accounts[bank_name] = new_account
        self.__user.plans[new_account] = plan.id
        print("Новый счёт успешно открыт. Номер васшего счёта: ", new_account)
        self.main_menu()

    def profile(self):
        print("""Это страница вашего профиля
                     Ваши данные:""")
        print("Ваше имя: ", self.__user.name)
        print("Ваша фамилия: ", self.__user.surname)
        print("Ваш адрес: ", self.__user.address)
        print("Ваш паспорт: ", self.__user.passport)
        print("Открытые счета: ")
        for account_id, plan_id in self.__user.plans.items():
            plan = src.DataOperator().get_cpf(plan_id, "Plan")
            properties = plan.get_properties()
            print("Номер счёта: ", account_id)
            for p in properties:
                print(p.info())
        print("1. Вернуться в главное меню")
        answer = input_int(1, 1, "Введите 1:")
        if answer == 1:
            self.main_menu()

    def transaction(self, account_id: int, bank: src.Bank):
        print("Это страница перевода между счетами:"
              "1. В одном банке"
              "2. Между банками"
              "3. Назад")
        ans = input_int(1, 3, "Введите число от 1 до 3:")
        if ans == 1:
            second_account_id = input_int(None, None, "Введите номер счёта получателя:")
            s = input_int(None, None, "Введите сумму перевода:")
            bank.transfer(account_id, second_account_id, s)
            print("Ваши деньги успешно переведены")
        elif ans == 2:
            second_bank_name = str(input("Введите банк получателя:"))
            if src.DataOperator().get_bank_by_name(second_bank_name) is None:
                print("Введённые банк не поддерживается нашей системой")
                self.transaction(account_id, bank)
            else:
                second_bank = src.DataOperator().get_bank_by_name(second_bank_name)
            second_account_id = input_int(None, None, "Введите номер счёта получателя:")
            s = input_int(None, None, "Введите сумму перевода:")
            acc = self.__user.banks[bank.name]
            src.bank.crosspayment.get_cpf().transfer(bank.id, account_id, second_bank.id, second_account_id, acc, s)
            print("Ваши деньги успешно переведены")
        elif ans == 3:
            self.operations()
        else:
            print("Такого варианта нет:")
            self.transaction(account_id, bank)

    def operations(self):
        print("Это страница операций")
        print("Ваши счета:")
        for account_id, plan_id in self.__user.plans.items():
            plan = src.DataOperator().get_cpf(plan_id, "Plan")
            plan_type = ""
            if isinstance(plan, src.DebitPlan):
                plan_type = "Дебетовый тариф"
            elif isinstance(plan, src.DepositPlan):
                plan_type = "Депозитный тариф"
            elif isinstance(plan, src.CreditPlan):
                plan_type = "Кредитный тариф"
            properties = plan.get_properties()
            print("Номер счёта: ", account_id, "Тип: ", plan_type)
            for p in properties:
                print(p.info())
        account_id = input_int(None, None, "Введите номер счёта с которым вы хотите совершить операцию:")
        global_bank_name = ""
        for bank_name, ident in self.__user.banks.items():
            if ident == account_id:
                global_bank_name = bank_name
        bank = src.DataOperator().get_bank_by_name(global_bank_name)
        print("""Возможные дествия со счетами:
                     1. Полжить деньги
                     2. Снять деньги
                     3. Перевести со счёта на счёт
                     4. Закрыть счёт
                     5. Главное меню""")
        answer = input_int(1, 5, "Введите число от 1 до 5:")
        if answer == 1:
            s = input_int(None, None, "Введите сумму для зачисления:")
            bank.put(account_id, s)
            print("Ваши деньги успешно зачислены")
        elif answer == 2:
            s = input_int(None, None, "Введите сумму для снятия:")
            bank.put(account_id, s)
            print("Ваши деньги успешно сняты")
        elif answer == 3:
            self.transaction(account_id, bank)
        elif answer == 4:
            print("Данная операция ещё не реализована")
            self.operations()
        elif answer == 5:
            self.main_menu()
        else:
            print("Такого варианта нет")
            self.operations()
        self.main_menu()

    def registration(self):
        print("Введите название банка в котором вы хотите зарегистрироваться:")
        bank_name = str(input())
        if src.DataOperator().get_bank_by_name(bank_name) is None:
            print("Введённые банк не поддерживается нашей системой")
            self.main_menu()
        else:
            bank = src.DataOperator().get_bank_by_name(bank_name)
            new_id = bank.register(self.__user.name, self.__user.surname, self.__user.address,
                                   str(self.__user.passport))
            if new_id is None:
                print("Данные указаны в неверном формате")
                self.registration()
            self.__user.banks[bank.name] = new_id
            print("Вы успешно зарегистрировались")
            self.main_menu()

    def update_data(self):
        if self.__user.banks:
            print("Введите название банка в котором вы хотите заменить данные:")
            bank_name = str(input())
            if src.DataOperator().get_bank_by_name(bank_name) is None:
                print("Введённые банк не поддерживается нашей системой")
                self.update_data()
            else:
                bank = src.DataOperator().get_bank_by_name(bank_name)
            address = self.__user.address
            passport = str(self.__user.passport)
            print("Хотите поменять адрес: (Y/N)")
            ans = str(input())
            if ans == "Y":
                print("Введите адресс:")
                address = str(input())
            print("Хотите поменять паспорт: (Y/N)")
            ans = str(input())
            if ans == "Y":
                print("Введите паспорт:")
                passport = str(input())
            if bank.update(self.__user.banks[bank.name], address, passport):
                print("Данные успешно изменены")
            else:
                print("Вы не зарегистрированы в этом банке")
            self.main_menu()
        else:
            print("Вы не зарегистрированы ни в одном банке")
            self.main_menu()

    def main_menu(self):
        print("""Это главное меню приложения вы можете сделать следующее:
                        1. Зарегистрироваться в банке
                        2. Открыть счёт
                        3. Дополнить данные
                        4. Профиль
                        5. Операции со счётом
                        6. Перейти к следующему дню
                        7. Выход""")
        answer = input_int(1, 7, "Введите число от 1 до 7:")
        if answer == 1:
            self.registration()
        elif answer == 2:
            self.open_plan()
        elif answer == 3:
            self.update_data()
        elif answer == 4:
            self.profile()
        elif answer == 5:
            self.operations()
        elif answer == 6:
            src.SingleTK.timekeeper().increase()
            print(src.DataOperator().account_info())
        elif answer == 7:
            exit(0)
        else:
            print("Введено неверное число")
            self.main_menu()

    def bank_create(self):
        sberbank = src.Bank("Sberbank")
        sber_debit = sberbank.add_plan(src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4)))
        sber_credit = sberbank.add_plan(
            src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2)))
        sber_deposit = sberbank.add_plan(
            src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2)))

        tinkoff = src.Bank("Tinkoff")
        tink_debit = tinkoff.add_plan(src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4)))
        tink_credit = tinkoff.add_plan(
            src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2)))
        tink_deposit = tinkoff.add_plan(
            src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2)))