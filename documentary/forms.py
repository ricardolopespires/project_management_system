from django import forms
from .models import Documentary





class DocumentaryForm(forms.ModelForm):

    class Meta:
        model = Documentary
        fields = ('__all__')
