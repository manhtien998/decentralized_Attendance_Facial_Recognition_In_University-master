from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from django.db import transaction
from django.forms.utils import ValidationError
from attendance.models import User

class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}))
    password1 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    password2 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':' confirm password'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields= ['username','first_name','last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}))
    password1 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    password2 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':' confirm password'}))


    class Meta(UserCreationForm.Meta):
        model = User
        fields= ['username','first_name','last_name']
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        return user



class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    class Meta:
        model = User
        fields = ['email', 'first_name','last_name', 'password',]


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
    
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'
        self.fields['old_password'].label = ""
        
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ""
        self.fields['new_password1'].help_text = '<span class="form-text text-muted"><small><ul><li>Your password cant be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password cant be a commonly used password.</li><li>Your password cant be entirely numeric.</li></ul></small></span>'
        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ""
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
