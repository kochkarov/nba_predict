from django.db import models
from django.contrib.auth.models import User
from services.bot import XgbBot, Bot
import json


class Human(User):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Member(models.Model):
    is_bot = models.IntegerField(verbose_name='Bot signature', default=0)
    human = models.ForeignKey('Human', related_name='+', on_delete=models.CASCADE,
                              verbose_name='Home team', default=None, null=True)
    param_json = models.TextField(default=None)

    def __init__(self):
        self.bot = None

    def restore_bot(self):
        param = json.loads(self.param_json)
        cls = globals()[param['class_name']]
        return cls(param)
