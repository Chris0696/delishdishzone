from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django import forms
from django.urls import reverse_lazy
from .validators import allow_only_images_validator
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


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),  validators=[allow_only_images_validator])

    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'city', 'rue', 'country', 'departement', 'longitude',
                  'latitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'upload-btn foodbakery-dev-featured-upload-btn'})
            self.fields[name].label = False

        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'


'''
            self.helper = FormHelper()
            self.helper.layout = Layout(
                'title',
                'description',
                'imagefile',
                HTML(
                    """{% if form.imagefile.value %}<img class="upload-btn foodbakery-dev-featured-upload-btn" src="{{ MEDIA_URL }}{{ form.imagefile.value }}">{% endif %}""", ),
                'flag_featured',
            )
'''
