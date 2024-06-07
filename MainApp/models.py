from django.db import models
from django.contrib.auth.models import User


class Snippet(models.Model):
    LANGS_CHOICES = (
                    ('Python', 'Python'),
                    ('JavaScript', 'JavaScript'),
                    ('HTML', 'HTML'),
                    ('CSS', 'CSS')
                    )

    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=100, 
                            choices=LANGS_CHOICES, default='python')
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    public = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.lang} - {self.name} - {self.creation_date} - {self.user}'
