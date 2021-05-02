from django.contrib.auth.forms import UserCreationForm
from .models import Member


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = UserCreationForm.Meta.fields
