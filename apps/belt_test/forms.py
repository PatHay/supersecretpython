from django import forms
from models import User, Travel_Plan
from django.core import validators
from django.forms import CharField
from django.contrib.admin import widgets
import re, bcrypt, datetime

PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d') #searches for a upper case followed by a number and the |(or operator) looks for a number then a upper case
# NAME_REGEX = re.compile(r'\W.*[A-Za-z ]|[ A-Za-z]\.*\W|\d.*[A-Za-z ]|[ A-Za-z].*\d')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')


class Register(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    username = forms.CharField(label='Username', max_length=255)
    # email = forms.CharField(label='Email', validators=[validators.validate_email], max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Pw', max_length=255)

    def clean(self):
        cleaned_data = super(Register, self).clean()
        name = cleaned_data.get("name")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_pw = cleaned_data.get("confirm_password")
        if not NAME_REGEX.search(name):
            msg = "Invalid name!"
            self.add_error('name', msg)
        if len(name) < 3:
            msg = "Name needs to be at least 3 characters long!"
            self.add_error('name', msg)
        if len(username) < 3:
            msg = "Username needs to be at least 3 characters long!"
            self.add_error('username', msg)
        if User.objects.filter(username = username):
            msg = "This Username has already been taken.  Please pick another!"
            self.add_error('username', msg)
        if User.objects.filter(name = name):
            msg = "This Name has already been registered.  Please enter another!"
        self.add_error('name', msg)
        if len(password) < 8:
            msg = "Password needs to be at least 8 characters long"
            self.add_error('password',msg)
        if len(confirm_pw) < 8:
            msg = "Confirm Password needs to be at least 8 characters long"
            self.add_error('confirm_password',msg)
        if password != confirm_pw:
            msg = "Your password and confirm password do not match!"
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)



class Login(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)
    username = forms.CharField(label='Username', max_length=255)

    def clean(self):
        cleaned_data = super(Login, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not User.objects.filter(username = username):
            msg = "Username not registered in database"
            self.add_error('username', msg)
            return True #ty chuck and rodrigo
        if bcrypt.checkpw(password.encode('utf8'), User.objects.get(username=username).password.encode('utf8')) != True:
            msg = "Incorrect password!"
            self.add_error('password', msg)


class Trip(forms.Form):
    destination = forms.CharField(label="Destination", max_length = 255)
    desc = forms.CharField(label="Description", max_length = 255)
    travel_from = forms.DateField(label="Travel Date From")
    travel_to = forms.DateField(label="Travel Date To")

    def clean(self):
        cleaned_data = super(Trip, self).clean()
        destination = cleaned_data.get("destination")
        desc = cleaned_data.get("desc")
        travel_from = cleaned_data.get("travel_from")
        travel_to = cleaned_data.get("travel_to")
        if travel_from == travel_to:
            msg = "Your Travel From and Travel To dates cannot be the same!"
            self.add_error('travel_from', msg)
            self.add_error('travel_to', msg)
        if travel_from < datetime.date.today():
            msg = "Your Travel Date From cannot be before the current date!"
            self.add_error('travel_from', msg)
        if travel_to < datetime.date.today():
            msg = "Your Travel Date To cannot be before the current date!"
            self.add_error('travel_to', msg)