from django import forms
from .models import Plat

class PlatForm(forms.ModelForm):
    class Meta:
        model = Plat
        fields = ['nom', 'description', 'prix', 'stock', 'categorie', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }
