from django.db import models


class Snippet(models.Model):
    LANGS_CHOICES = (
                    ('py', 'Python'),
                    ('js', 'JavaScript'),
                    ('html', 'HTML'),
                    ('css', 'CSS')
                    )

    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=100, 
                            choices=LANGS_CHOICES, default='python')
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
