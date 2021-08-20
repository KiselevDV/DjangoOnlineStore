from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

from .models import Order


class LoginForm(forms.ModelForm):
    """Форма входа на сайт"""

    # Скрыть поле password переопределив виджет
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        """Переписать лейбл на русский"""
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

    def clean(self):
        """Валидация пользователя"""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # exists() - наличие данного объекта
        if not User.objects.filter(username=username).exists():
            raise ValidationError(
                f'Пользователь с логином {username} не найден в системе.')

        user = User.objects.get(username=username)
        if user:
            if not user.check_password(password):
                raise ValidationError('Неверный пароль!')

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(forms.ModelForm):
    """Регистрация пользователя"""

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Подтвердить пароль', widget=forms.PasswordInput)
    phone = forms.CharField(label='Номер телефона', required=False)
    address = forms.CharField(label='Адрес', required=False)
    email = forms.EmailField(label='E-mail', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean_email(self):
        """Вадидация почты"""
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['by', 'ru', 'ua', 'kz']:
            raise ValidationError(
                f'Регистрация для доменов "{domain}" невозможна')
        # Проверка уже зарегистрированого пользователя, с таким email
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                f'Данный почтовый адрес уже зарегистрирован в системе!')
        return email

    def clean_username(self):
        """Валидация логина"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                f'{username} - данный логин уже используется!')
        return username

    def clean(self):
        """Валидация пароля"""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError(f'Пароли не совпадают!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name',
                  'last_name', 'address', 'phone', 'email')


class OrderForm(forms.ModelForm):
    """Форма оформления заказа товаров"""

    order_date = forms.DateField(
        label='Дата получения заказа',
        widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'buying_type',
                  'order_date', 'comment')
