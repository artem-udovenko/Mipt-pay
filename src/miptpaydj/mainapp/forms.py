from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Name')
    surname = forms.CharField(max_length=100, help_text='Surname')
    address = forms.CharField(max_length=150, help_text='Address')
    passport = forms.IntegerField(help_text='Passport')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'surname', 'address', 'passport')


class PutForm(forms.Form):
    bank_id = forms.CharField(max_length=100, help_text='Bank ID')
    account_id = forms.CharField(max_length=100, help_text='Account ID')
    amount = forms.CharField(max_length=150, help_text='Amount')


class TransferForm(forms.Form):
    departure_bank = forms.CharField(max_length=100, help_text='Bank ID1')
    departure_account = forms.CharField(max_length=100, help_text='Account ID1')
    destination_bank = forms.CharField(max_length=100, help_text='Bank ID2')
    destination_account = forms.CharField(max_length=100, help_text='Account ID2')
    amount = forms.CharField(max_length=150, help_text='Amount')
