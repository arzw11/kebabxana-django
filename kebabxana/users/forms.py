from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField
import datetime

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин или E-mail', widget=forms.TextInput(attrs={'placeholder': 'Логин или почта'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={ 'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}), region='RU')
    class Meta: 
        model = get_user_model()
        fields = ['username', 'phone_number','email','password1','password2']
        
        labels = {
            'email': 'E-mail'
        }

        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'E-mail'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone_number']
        
        if get_user_model().objects.filter(phone_number=phone):
            raise forms.ValidationError('Такой номер телефона уже зарегистрирован')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if get_user_model().objects.filter(email=email):
            raise forms.ValidationError('Такой почтовый адрес уже зарегистрирован')
        return email

class PasswordResetFormUser(PasswordResetForm):
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'placeholder': 'Введите ваш E-mail'}))

class PasswordResetFormUserConfirm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label='Новый пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}), label='Повторите пароль')


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True,label='Логин', widget=forms.TextInput(attrs={'class': 'text-input'}))
    email = forms.CharField(disabled=True, required= False, label='E-mail', widget=forms.TextInput(attrs={'class': 'text-input'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'text-input'}), label='Номер телефона')
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))
    
    class Meta:
        model = get_user_model()
        fields = ['username','phone_number', 'email', 'date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Старый пароль'}), label='Старый пароль')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label='Новый пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}), label='Повторите пароль')
