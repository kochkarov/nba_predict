from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField
from services.predictor import XgbPredictor, Predictor
import json


class Member(User):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    is_bot = models.IntegerField('Is Bot?', default=0)
    param_json = models.TextField(default=None)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.predictor = None

    def restore_predictor(self):
        param = json.loads(self.param_json)
        cls = globals()[param['class_name']]
        return cls(param)
