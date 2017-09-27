from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Travel_Plan(models.Model):
    destination = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date = models.DateField()
    joined_users = models.ManyToManyField(User, related_name = "joint_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    planned_by = models.ForeignKey(User, related_name="my_trips", on_delete=models.CASCADE)