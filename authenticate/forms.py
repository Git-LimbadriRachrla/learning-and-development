# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
# from django import forms
# from .models import UserProfile

# class EditProfileForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password')

#     def __init__(self, *args, **kwargs):
#         super(EditProfileForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['first_name'].widget.attrs['class'] = 'form-control'
#         self.fields['last_name'].widget.attrs['class'] = 'form-control'
#         self.fields['email'].widget.attrs['class'] = 'form-control'


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     role = forms.ChoiceField(choices=UserProfile.ROLES, widget=forms.Select(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')

#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['class'] = 'form-control'

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from .models import UserProfile


# Custom validator for names to allow only alphabetic characters
def validate_name(value):
    if not value.isalpha():
        raise ValidationError("Name should contain only alphabetic characters.")


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Enter a valid email address.'}
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_name]
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_name]
    )
    role = forms.ChoiceField(
        choices=UserProfile.ROLES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$',
                message="Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, and one number."
            )
        ]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].validators = [
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message="Username can only contain letters, numbers, and underscores."
            )
        ]
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
