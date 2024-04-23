from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class BankModel(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return self.name


class PersonModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    passport = models.IntegerField(null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            PersonModel.objects.create(user=instance)
        instance.personmodel.save()


class ClientModel(models.Model):
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE)
    person = models.ForeignKey(PersonModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    passport = models.IntegerField()
    precarious = models.BooleanField()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return f'{self.name} {self.surname}'


class PlanCategoryModel(models.Model):
    name = models.CharField(max_length=50)
    commission = models.BooleanField()
    period = models.BooleanField()
    lower_limit = models.BooleanField()
    upper_limit = models.BooleanField()
    transfer_limit = models.BooleanField()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория плана'
        verbose_name_plural = 'Категории планов'

    def __str__(self):
        return self.name


class PlanModel(models.Model):
    name = models.CharField(max_length=50)
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE)
    category = models.ForeignKey(PlanCategoryModel, on_delete=models.CASCADE)
    commission = models.DecimalField(max_digits=8, decimal_places=6)
    increased_commission = models.DecimalField(max_digits=8, decimal_places=6)
    period = models.IntegerField()
    decreased_period = models.IntegerField()
    lower_limit = models.DecimalField(max_digits=14, decimal_places=2)
    decreased_lower_limit = models.DecimalField(max_digits=14, decimal_places=2)
    upper_limit = models.DecimalField(max_digits=14, decimal_places=2)
    decreased_upper_limit = models.DecimalField(max_digits=14, decimal_places=2)
    transfer_limit = models.DecimalField(max_digits=14, decimal_places=2)
    decreased_transfer_limit = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'

    def __str__(self):
        return self.name


class AccountModel(models.Model):
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    opened = models.BooleanField()
    money = models.DecimalField(max_digits=14, decimal_places=2)
    transfer = models.DecimalField(max_digits=14, decimal_places=2)
    plan = models.ForeignKey(PlanModel, on_delete=models.CASCADE)
    freeze_date = models.IntegerField()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        if self.id:
            return f"Счет {self.id}"
        else:
            return "Безымянный счет"



class TransactionModel(models.Model):
    departure = models.IntegerField()
    destination = models.IntegerField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.IntegerField()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return "Безымянная транзакция"


class DiaryModel(models.Model):
    parameter = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Страница параметров'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return self.parameter
