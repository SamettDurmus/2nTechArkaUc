from django import forms
from .models import AdminIzinAtama

class AdminIzinAtamaForm(forms.ModelForm):
    class Meta:
        model = AdminIzinAtama
        fields = ['personel', 'baslangic_tarihi', 'bitis_tarihi']