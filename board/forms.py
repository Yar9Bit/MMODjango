from django import forms
from .models import Ad, Resp


class AdForm(forms.ModelForm):
    """Добавление публикаций на сайт"""

    class Meta:
        model = Ad
        fields = ('title', 'text', 'category', 'attach')
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form_control'}
            ),
            'text': forms.Textarea(
                attrs={'class': 'form_control'}
            ),
            'category': forms.Select(
                attrs={'class': 'form_control'}
            ),
            'attach': forms.FileInput(
                attrs={'class': 'form_control'}
            ),
        }


class RespForm(forms.ModelForm):
    """Отклик на объявление"""
    class Meta:
        model = Resp
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
