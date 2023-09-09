from django.db import models
from django.contrib.auth.models import User

class Mailing(models.Model):
    user = models.OneToOneField(User, verbose_name='mailing', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(verbose_name='active', default=True)

    def __str__(self) -> str:
        return f'{self.user} is {self.active}'
