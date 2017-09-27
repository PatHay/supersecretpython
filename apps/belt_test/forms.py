from django import forms
from models import User, Book, Review, Author
from django.core import validators
from django.forms import CharField
import re, bcrypt

PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d') #searches for a upper case followed by a number and the |(or operator) looks for a number then a upper case
# NAME_REGEX = re.compile(r'\W.*[A-Za-z ]|[ A-Za-z]\.*\W|\d.*[A-Za-z ]|[ A-Za-z].*\d')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')


class Register(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    alias = forms.CharField(label='Alias', max_length=255)
    email = forms.CharField(label='Email', validators=[validators.validate_email], max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Pw', max_length=255)

    def clean(self):
        cleaned_data = super(Register, self).clean()
        name = cleaned_data.get("name")
        alias = cleaned_data.get("alias")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_pw = cleaned_data.get("confirm_password")
        if not NAME_REGEX.search(name):
            msg = "Invalid name!"
            self.add_error('name', msg)
        if User.objects.filter(alias = alias):
            msg = "This alias has already been taken.  Please pick another!"
            self.add_error('alias', msg)
        if User.objects.filter(email = email):
            msg = "This email address has already been registered!"
            self.add_error('email', msg)
        if password != confirm_pw:
            msg = "Your password and confirm password do not match!"
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)



class Login(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)
    email = forms.CharField(label='Email', max_length=255)

    def clean(self):
        cleaned_data = super(Login, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if not User.objects.filter(email = email):
            msg = "Email not registered in database"
            self.add_error('email', msg)
            return True #ty chuck and rodrigo
        if bcrypt.checkpw(password.encode('utf8'), User.objects.get(email=email).password.encode('utf8')) != True:
            msg = "Incorrect password!"
            self.add_error('password', msg)

# def author_list():
#     a_list = []
#     for author in Author.objects.all():
#         a_list.append((author.id, author.name))
#     return a_list  #ty chris

# class Add_Book(forms.Form):
#     title = forms.CharField(label="Book Title", max_length=255)
#     author = forms.ChoiceField(label="Choose from the List", choices=author_list) #no () on author list so it is called each time/refreshes the list
#     # (author.id,author.name) for author in Author.objects.all()
#     new_author = forms.CharField(required=False, label="Or add a new author", max_length=255)
#     review = forms.CharField(label="Review", widget=forms.Textarea)
#     rating = forms.ChoiceField(label="Rating", choices=[(x, x) for x in range (1, 6)])
    
#     def clean(self):
#         cleaned_data = super(Add_Book, self).clean()
#         title = cleaned_data.get("title")
#         author = cleaned_data.get("author")
#         new_author = cleaned_data.get("new_author")
#         review = cleaned_data.get("review")
#         rating = cleaned_data.get("rating")
#         if Author.objects.filter(name=new_author):
#             msg = "This author is already in the database.  Please see the author dropdown"
#             self.add_error('new_author', msg)
#         if Book.objects.filter(title=title):
#             msg = "This book is already in the database.  Please check the main books page to navigate to this book and leave a review"
#             self.add_error('title', msg)

# class Add_Review(forms.Form):
#     review = forms.CharField(label="Review", widget=forms.Textarea)
#     rating = forms.ChoiceField(label="Rating", choices=[(x, x) for x in range (1, 6)])
    
#     def clean(self):
#         cleaned_data = super(Add_Review, self).clean()
#         review = cleaned_data.get("review")
#         rating = cleaned_data.get("rating")