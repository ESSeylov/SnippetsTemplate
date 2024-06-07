from django.forms import ModelForm, TextInput, Textarea, BooleanField
from MainApp.models import Snippet

from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput
from django.core.exceptions import ValidationError


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ['name', 'lang', 'code', 'public']
        labels = {'name': '', 'lang': '', 'code': '', 'public': 'Публичный сниппет'}
        widgets = {
                   'name': TextInput(attrs={'placeholder': 'Имя сниппета'}),
                   'code': Textarea(attrs={'placeholder': 'Пример кода сниппета'}),
                   }


class UserReistrationForm(ModelForm):
    password1 = CharField(widget=PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = CharField(widget=PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
                   'username': TextInput(attrs={'placeholder': 'Имя пользователя'}),
                   'email': TextInput(attrs={'placeholder': 'Электронная почта'}),
                   }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        if len(username) < 3:
            raise ValidationError('Имя пользователя слишком короткое')
        return username

    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if (password1 and password2 and (password1 == password2)):
            return password2
        raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super(UserReistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
