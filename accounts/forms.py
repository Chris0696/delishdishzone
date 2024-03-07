from crispy_forms.helper import FormHelper
from django import forms
from django.urls import reverse_lazy

from .models import User, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password == confirm_password:
            if len(password) <= 8:
                raise forms.ValidationError(
                    "Passwords must be at least 8 characters."
                )
        else:
            raise forms.ValidationError(
                "Passwords does'nt match."
            )
