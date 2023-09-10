from django import forms
from .models import ChartUserprofile

class MyForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    content = forms.CharField(max_length=200)
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = ChartUserprofile
        fields = ['name', 'email','content']