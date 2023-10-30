from django import forms
from django.forms import ModelForm
from .models import FaceRec

class ImageVideoForm(ModelForm):

    class Meta:
        model = FaceRec
        fields = ['image', 'video']



