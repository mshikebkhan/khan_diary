from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.admin.widgets import AdminDateWidget
import datetime

from .models import Profile
from django_countries.fields import CountryField

# The following usernames can't be used as username (they are forbidden).
forbidden_users = ['admin', 'html', 'password' 'edit', 'css', 'js', 'authenticate', 'login', 'logout',
                   'administrator', 'root', 'email', 'user', 'join', 'sql', 'static', 'python', 'delete']


class SignupForm(UserCreationForm):
    """Sign Up form for new users."""
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "First Name", 'autofocus': '""'}), max_length=30, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Last Name"}), max_length=30, required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Username", 'autocapitalize': "none", 'autocomplete': "username"}), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Email"}), max_length=50, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Password", 'autocomplete': "new-password"}), max_length=30, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Confirm Password"}), max_length=30, required=False)

    class Meta: 
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean(self):

        # data from the form is fetched using super function
        super(SignupForm, self).clean()

        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        username_list = list(username)
        periods_list = ['/', '"', "'", '!', '#', '*', '%',
                        '$', '^', '&', '(', ')', '+', ',', '?', '\\']

        if username:

            # Conditions to be met for the username length.
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                    'Minimum 3 characters required'])

            if username in forbidden_users:
                self._errors['username'] = self.error_class([
                    'Invalid name for user, this is a reserverd word.'])

            for var in username:
                if var in periods_list:
                    self._errors['username'] = self.error_class([
                        'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])

        if first_name:
            if len(first_name) < 2:
                self._errors['first_name'] = self.error_class([
                    'Minimum 2 characters required.'])

        if email:
            if User.objects.filter(email=email).exists():
                self._errors['email'] = self.error_class([
                    'A user with this email already exists!'])

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password1', e)

        # return any errors if found.
        return self.cleaned_data




#Gender options
gender_choices = (
    ('Male','Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
    )
 


class ProfileUpdateForm(forms.ModelForm):
    """Form to update/edit profile."""
    gender = forms.ChoiceField(choices=gender_choices)
    birthday = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Ex- 01/01/2000"}, format='%d/%m/%Y'), input_formats=['%d/%m/%Y'], required=True)
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea is-medium is-rounded is-success', 'rows': "7",
               'placeholder': "Add something about you", 'autocomplete': 'off'})
    , max_length=150)

    country = CountryField()


    facebook = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Facebook account link"}), max_length=100, required=False)

    twitter = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Twitter account link"}), max_length=100, required=False)
    instagram = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Instagram account link"}), max_length=100, required=False)
    youtube = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "YouTube channel link"}), max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['gender', 'birthday' , 'bio', 'country', 'facebook', 'twitter', 'instagram', 'youtube']
        widgets = {
        'gender': forms.Select(choices=gender_choices),
        }

    def clean(self):

        # data from the form is fetched using super function.
        super(ProfileUpdateForm, self).clean()

        birthday = self.cleaned_data.get('birthday')

        # Sure for invalid birthdays.
        min_date = datetime.date(1900,1,1)
        max_date = datetime.date.today() - datetime.timedelta(days=365*12)
        if birthday:
            if birthday < min_date:
                self._errors['birthday'] = self.error_class([
                'Your age do not look real.'])
            if birthday > max_date:
                self._errors['birthday'] = self.error_class([
                'Your age must be at least 12.'])


        # return any errors if found
        return self.cleaned_data



class UserUpdateForm(forms.ModelForm):
    """Update user details."""
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "First Name"}), max_length=30, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Last Name"}), max_length=30, required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Username", 'autocapitalize': "none", 'autocomplete': "username"}), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'input is-rounded is-success', 'placeholder': "Email"}), max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username','first_name' , 'last_name', 'email']

    def clean(self):

        # data from the form is fetched using super function
        super(UserUpdateForm, self).clean()

        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        username_list = list(username)
        periods_list = ['/','"', "'", '!', '#', '*', '%', '$', '^', '&', '(', ')', '+', ',', '?', '\\' ]


        if username:

            # Conditions to be met for the username length.
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                    'Minimum 3 characters required'])

            if username in forbidden_users:
                self._errors['username'] = self.error_class([
                    'Invalid name for user, this is a reserverd word.'])

            for var in username:
                if var in periods_list:
                    self._errors['username'] = self.error_class([
                        'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])

        if first_name:
            if len(first_name) < 2:
                self._errors['first_name'] = self.error_class([
                'Minimum 2 characters required'])

        if email:
            if User.objects.filter(email=email).exists():
                user_obj = User.objects.get(email=email)
                if user_obj.username != username:
                    self._errors['email'] = self.error_class([
                    'A user with this email already exists!'])      

 
class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'input is-rounded is-success', 'placeholder': "Current Password", 'autocomplete': "old-password"}), max_length=30, required=True)

    new_password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'input is-rounded is-success', 'placeholder': "New Password", 'autocomplete': "new-password"}), max_length=30, required=True)

    confirm_password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'input is-rounded is-success', 'placeholder': "Confirm New Password", 'autocomplete': "confirm-password"}), max_length=30, required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)

        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password was incorrect.'])

        elif new_password != confirm_password:
            self._errors['new_password'] =self.error_class(['New passwords do not match.'])

        elif new_password:
            try:
                validate_password(new_password)
            except ValidationError as e:
                self.add_error('new_password', e)

        # return any errors if found
        return self.cleaned_data  

        return self.cleaned_data       


class AccountPrivacyForm(forms.ModelForm):
    """Form to update account privacy."""
    public = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ['public']

    def clean(self):

        # data from the form is fetched using super function.
        super(AccountPrivacyForm, self).clean()

        return self.cleaned_data
