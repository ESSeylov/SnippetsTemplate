from django.forms import ModelForm, TextInput, Textarea
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ['name', 'lang', 'code']
        labels = {'name': '', 'lang': '', 'code': ''}
        widgets = {
                   'name': TextInput(attrs={'placeholder': 'Название'}),
                   'code': Textarea(attrs={'placeholder': 'Код'})
                   }
