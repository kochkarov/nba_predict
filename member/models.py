from django.db import models
from django.contrib.auth.models import User
from services.bot import XgbBot, BaseBot, Bot


class Human(User):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('User name', max_length=64, default='')
    is_bot = models.IntegerField(verbose_name='Bot signature', default=1)
    human = models.ForeignKey('Human', related_name='+', on_delete=models.CASCADE,
                              verbose_name='Human user', default=None, null=True)
    param = models.JSONField(null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = None

    def __str__(self):
        if self.is_bot:
            return f"Bot {self.name} {self.param['class_name']}"
        return f'{self.name}'

    def restore_bot(self):
        if self.is_bot:
            cls = globals()[self.param['class_name']]
            self.bot = cls(self.param)

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'
