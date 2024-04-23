SETUP_MODE = False


def main():
    global SETUP_MODE
    if SETUP_MODE:
        return
    SETUP_MODE = True
    import src
    from django.contrib.auth import authenticate

    src.User.objects.all().delete()
    src.DiaryModel.objects.all().delete()
    src.BankModel.objects.all().delete()
    src.PersonModel.objects.all().delete()
    src.ClientModel.objects.all().delete()
    src.PlanCategoryModel.objects.all().delete()
    src.PlanModel.objects.all().delete()
    src.AccountModel.objects.all().delete()
    src.TransactionModel.objects.all().delete()

    # Date

    src.SingleAdaptor.adaptor().set_date()

    # Plan categories

    debit = src.PlanCategoryModel(name="Debit", commission=False, period=False, lower_limit=False, upper_limit=False, transfer_limit=True)
    debit.save()
    deposit = src.PlanCategoryModel(name="Deposit", commission=True, period=True, lower_limit=False, upper_limit=False, transfer_limit=True)
    deposit.save()
    credit = src.PlanCategoryModel(name="Credit", commission=True, period=False, lower_limit=True, upper_limit=False, transfer_limit=True)
    credit.save()

    # Banks

    sber = src.Bank(None, "Sberbank")

    tink = src.Bank(None,"Tinkoff")

    # Plans

    sber_debit = src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4), sber.id)
    sber.add_plan(sber_debit.id)

    sber_deposit = src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2), sber.id)
    sber.add_plan(sber_deposit.id)

    sber_credit = src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2), sber.id)
    sber.add_plan(sber_credit.id)

    tink_debit = src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4), tink.id)
    tink.add_plan(tink_debit.id)

    tink_deposit = src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2), tink.id)
    tink.add_plan(tink_deposit.id)

    tink_credit = src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2), tink.id)
    tink.add_plan(tink_credit.id)

    # Persons and Users

    xygen = src.User.objects.create_user(username='xygen', password='strong_password')
    mikali = src.User.objects.create_user(username='mikali', password='ordinary_password')
    artudi = src.User.objects.create_user(username='artudi', password='weak_password')

    xygen.save()
    mikali.save()
    artudi.save()

    xygen.refresh_from_db()
    mikali.refresh_from_db()
    artudi.refresh_from_db()

    denis = src.Person(ident=xygen.personmodel.id, name="Denis", surname="Barilov", address="barilov.di@phystech.edu", passport="1234123456")
    src.SingleAdaptor.adaptor().fill_person(xygen.personmodel, denis)
    denis_model = xygen.personmodel

    misha = src.Person(ident=mikali.personmodel.id, name="Mikhail", surname="Kalinin", address="kalinin.mi@phystech.edu", passport="1000000000")
    src.SingleAdaptor.adaptor().fill_person(mikali.personmodel, misha)
    misha_model = mikali.personmodel

    artem = src.Person(ident=artudi.personmodel.id, name="Artem", surname="Udovenko", address="udovenko.ai@phystech.edu", passport="7777777777")
    src.SingleAdaptor.adaptor().fill_person(artudi.personmodel, artem)
    artem_model = artudi.personmodel

    xygen.save()
    mikali.save()
    artudi.save()

    xygen = authenticate(username=xygen.username, password=xygen.password)
    mikali = authenticate(username=mikali.username, password=mikali.password)
    artudi = authenticate(username=artudi.username, password=artudi.password)


    # Clients

    denis_sber_id = sber.register(denis.name, denis.surname, denis.address, denis.passport, denis.id)

    misha_sber_id = sber.register(misha.name, misha.surname, "NO_VALUE", "NO_VALUE", misha.id)

    artem_sber_id = sber.register(artem.name, artem.surname, "NO_VALUE", "NO_VALUE", artem.id)

    denis_tink_id = tink.register(denis.name, denis.surname, denis.address, denis.passport, denis.id)

    misha_tink_id = tink.register(misha.name, misha.surname, misha.address, misha.passport, misha.id)

    # Accounts

    denis_sber_debit_id = sber.open_account(denis_sber_id, sber_debit.id)

    denis_sber_deposit_id = sber.open_account(denis_sber_id, sber_deposit.id)

    denis_sber_credit_id = sber.open_account(denis_sber_id, sber_credit.id)

    denis_tink_debit_id = tink.open_account(denis_tink_id, tink_debit.id)

    denis_tink_deposit_id = tink.open_account(denis_tink_id, tink_deposit.id)

    denis_tink_credit_id = tink.open_account(denis_tink_id, tink_credit.id)


    misha_sber_debit_id = sber.open_account(misha_sber_id, sber_debit.id)

    misha_sber_deposit_id = sber.open_account(misha_sber_id, sber_deposit.id)

    misha_tink_debit_id = tink.open_account(misha_tink_id, tink_debit.id)


    misha_tink_credit_id = tink.open_account(misha_tink_id, tink_credit.id)


    artem_sber_debit_id = sber.open_account(artem_sber_id, sber_debit.id)

    artem_sber_deposit_id = sber.open_account(artem_sber_id, sber_deposit.id)

    artem_sber_credit_id = sber.open_account(artem_sber_id, sber_credit.id)

    # Fill money

    sber.put(denis_sber_debit_id, 8000)
    sber.put(denis_sber_deposit_id, 9500)
    sber.put(denis_sber_credit_id, 10000)

    sber.put(misha_sber_debit_id, 5000)
    sber.put(misha_sber_deposit_id, 6500)

    sber.put(artem_sber_debit_id, 7000)
    sber.put(artem_sber_deposit_id, 7500)
    sber.put(artem_sber_credit_id, 7000)

    tink.put(denis_tink_debit_id, 4000)
    tink.put(denis_tink_deposit_id, 3500)
    tink.put(denis_tink_credit_id, 5000)

    tink.put(misha_tink_debit_id, 5500)
    tink.put(misha_tink_credit_id, 6000)

    # Banks saving

    src.SingleDO.DO().done_with(sber.id, "Bank")
    src.SingleDO.DO().done_with(tink.id, "Bank")

    src.SingleDO.DO().print_online()




if __name__ == "__main__":
    main()
