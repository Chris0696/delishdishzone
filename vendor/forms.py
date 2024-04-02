from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django import forms
from accounts.validators import allow_only_images_validator
from .models import Vendor, OpeningHour


class VendorForm(forms.ModelForm):
    restaurant_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
                                         validators=[allow_only_images_validator])

    class Meta:
        model = Vendor
        fields = ['restaurant_name', 'restaurant_phone', 'restaurant_license']

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'upload-btn foodbakery-dev-featured-upload-btn'})


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


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']




