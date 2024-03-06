from django import forms

from .models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['restaurant_name', 'restaurant_license']

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'input'})

