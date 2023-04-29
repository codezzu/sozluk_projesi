from django import forms
from .models import Soru, Yorum

class SoruForm(forms.ModelForm):
    class Meta:
        model = Soru
        fields = ['baslik', 'icerik']

class YorumForm(forms.ModelForm):
    class Meta:
        model = Yorum
        fields = ['icerik']
