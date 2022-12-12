from django.db import models


class UserModel(models.Model):
    username = models.CharField(verbose_name='Usuário', max_length=100)
    password = models.CharField(verbose_name="Senha", max_length=100)

    def __str__(self):
        return self.username
