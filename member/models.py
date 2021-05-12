from django.db import models
from django.contrib.auth.models import User
from services.bot import XgbBot, Bot
import json


class Human(User):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Member(models.Model):
    name = models.CharField('User name', max_length=64, default='')
    is_bot = models.IntegerField(verbose_name='Bot signature', default=1)
    human = models.ForeignKey('Human', related_name='+', on_delete=models.CASCADE,
                              verbose_name='Human user', default=None, null=True)
    param_json = models.TextField(default=None, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = self.restore_bot()

    def __str__(self):
        return f'{self.name}'

    def restore_bot(self):
        if self.is_bot:
            param = json.loads(self.param_json)
            cls = globals()[param['class_name']]
            return cls(param)
        return None

    def restore_name(self):
        pass

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
