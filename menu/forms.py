from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django import forms

from .models import Category, FoodItem
from accounts.validators import allow_only_images_validator


class CategoryForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),
                            validators=[allow_only_images_validator])

    class Meta:
        model = Category
        fields = ['category_name', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'upload-btn foodbakery-dev-featured-upload-btn'})
            self.helper = FormHelper()
            self.helper.layout = Layout(
                'title',
                'description',
                'imagefile',
                HTML(
                    """{% if form.imagefile.value %}
                    <img class="upload-btn foodbakery-dev-featured-upload-btn w-100" src="{{ MEDIA_URL }}{{ form.imagefile.value }}">
                    {% endif %}""", ),
                'flag_featured',
            )


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),
                            validators=[allow_only_images_validator])

    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

    def __init__(self, *args, **kwargs):
        super(FoodItemForm, self).__init__(*args, **kwargs)

        for name, fiels in self.fields.items():
            self.fields[name].widget.attrs.update({'class': 'upload-btn foodbakery-dev-featured-upload-btn'})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            'imagefile',
            HTML(
                """{% if form.imagefile.value %}
                <img style="margin-top: 5px; font-size: 19px" class="upload-btn foodbakery-dev-featured-upload-btn w-50" src="{{ MEDIA_URL }}{{ form.imagefile.value }}">
                {% endif %}""", ),
            'flag_featured',
        )
