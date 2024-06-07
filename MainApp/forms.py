from django.forms import ModelForm, TextInput, Textarea, BooleanField
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ['name', 'lang', 'code', 'public']
        labels = {'name': '', 'lang': '', 'code': '', 'public': 'Публичный сниппет'}
        widgets = {
                   'name': TextInput(attrs={'placeholder': 'Имя сниппета'}),
                   'code': Textarea(attrs={'placeholder': 'Пример кода сниппета'}),
                   }
