from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information.
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating profile information.
    """
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'github_url', 'website', 'specialization']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о себе и своем опыте'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'specialization': forms.TextInput(attrs={'placeholder': 'Например: Frontend разработчик, Python разработчик'})
        } 