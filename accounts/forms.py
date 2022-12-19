from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    """ For Sign Up """
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("age", "email")


class CustomUserChangeForm(UserChangeForm):
    """ For Admin page """
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
