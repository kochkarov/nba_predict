from django.contrib.auth.forms import UserCreationForm
from .models import Human


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Human
        fields = UserCreationForm.Meta.fields
