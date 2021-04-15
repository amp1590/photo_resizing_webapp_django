from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class UploadPhotoForm(forms.Form):
    title = forms.CharField(label="Title of the image")
    img = forms.ImageField(label="Image File")
    #recipient = forms.EmailField(label="Your email (results will be sent to this email)")

    