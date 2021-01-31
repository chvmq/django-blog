from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import News


class UserLoginFrom(AuthenticationForm):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={"class": 'form-control'}))

    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={"class": 'form-control'})
    )

    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={"class": 'form-control'})
    )

    password2 = forms.CharField(
        label='confirm password',
        widget=forms.PasswordInput(attrs={"class": 'form-control'})
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={"class": 'form-control'})
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'captcha'
        ]

        # widgets = {
        #     'username': forms.TextInput(attrs={"class": 'form-control'}),
        #     'email': forms.TextInput(attrs={"class": 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={"class": 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={"class": 'form-control'}),
        # }


#
# class NewsForm(forms.Form):
#     """Не связная форма с моделей"""
#     title = forms.CharField(max_length=50,
#                             label='Название',
#                             widget=forms.TextInput(attrs={"class": 'form-control'}))
#
#     content = forms.CharField(label='Текст ',
#                               required=False,
#                               widget=forms.Textarea(attrs={"class": 'form-control'}))
#
#     is_published = forms.BooleanField(label='Опубликовано? ',
#                                       initial=True)
#
#     category = forms.ModelChoiceField(queryset=Category.objects.all(),
#                                       label='Категория',
#                                       empty_label='Выберите категорию',
#                                       widget=forms.Select(attrs={"class": 'form-control'}))
#

class NewsForm(forms.ModelForm):
    """Связная форма с моделью"""

    class Meta:
        model = News
        # fields = '__all__'
        fields = [
            'title',
            'content',
            'is_published',
            'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={"class": 'form-control'}),
            'content': forms.Textarea(attrs={"class": 'form-control'}),
            'category': forms.Select(attrs={"class": 'form-control'}),
        }

    def clean_title(self):
        """Кастомный валидатор проверяет метод is_valid"""
        title = self.cleaned_data['title']
        if str(title)[0].isdigit():
            raise ValidationError('Строка не должна начинаца с цифры')
        return title

    def clean_is_published(self):
        """Кастомный валидатор"""
        status = self.cleaned_data['is_published']
        if status is False:
            raise ValidationError('Прочтите условия соглашения')
        return status
