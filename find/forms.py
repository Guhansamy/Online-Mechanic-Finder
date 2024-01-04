from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class Register_user(UserCreationForm):
    email=forms.EmailField(label='E-Mail')
    firstname=forms.CharField(label='Firstname')
    lastname=forms.CharField(label='Lastname')
    class Meta:
        model=User
        fields=('username','firstname','lastname','email')
    def save(self, commit=True):
        user=super(Register_user,self).save(commit=False)
        user.first_name=self.cleaned_data['firstname']
        user.last_name=self.cleaned_data['lastname']
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user