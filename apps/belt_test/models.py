from __future__ import unicode_literals
from django.db import models

# class User(models.Model):
#     name = models.CharField(max_length = 255)
#     alias = models.CharField(max_length = 255)
#     email = models.CharField(max_length = 255)
#     password = models.CharField(max_length = 255)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)

# class Author(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)

# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     author = models.ForeignKey(Author, related_name="books")
#     reviewed_users = models.ManyToManyField(User, related_name = "reviewed_books")

# class Review(models.Model):
#     written_review = models.TextField()
#     rating = models.IntegerField(default=3)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     reviewer = models.ForeignKey(User, related_name="user_reviews")
#     reviewed_book = models.ForeignKey(Book, related_name="book_reviews")

