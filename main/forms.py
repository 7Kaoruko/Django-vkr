# Импорты
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile


# Форма регистрации
class RegisterForm(UserCreationForm):
    # Добавляем поле email (по умолчанию его нет в UserCreationForm)
    email = forms.EmailField(required=True)

    class Meta:
        # Указываем модель пользователя
        model = User

        # Поля, которые будут отображаться в форме
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        # Инициализация родительского класса
        super().__init__(*args, **kwargs)


        # Русские подписи полей

        self.fields["username"].label = "Логин"
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повтор пароля"


        # Убираем стандартные подсказки Django

        for f in ("username", "email", "password1", "password2"):
            self.fields[f].help_text = ""

        # Настройка внешнего вида (CSS + placeholder)

        # Логин
        self.fields["username"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Введите логин",
            "autocomplete": "username",
        })

        # Email
        self.fields["email"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Введите email",
            "autocomplete": "email",
        })

        # Пароль
        self.fields["password1"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Введите пароль",
            "autocomplete": "new-password",
        })

        # Повтор пароля
        self.fields["password2"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Повторите пароль",
            "autocomplete": "new-password",
        })

# Форма входа
class LoginForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        # Инициализация родительского класса
        super().__init__(request=request, *args, **kwargs)

        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"

        # Настройка внешнего вида

        self.fields["username"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Введите логин",
            "autocomplete": "username",
        })

        self.fields["password"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Введите пароль",
            "autocomplete": "current-password",
        })

# Форма загрузки аватарки
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        widgets = {
            "avatar": forms.FileInput(attrs={
                "class": "avatar-input",
                "accept": "image/*"
            })
        }