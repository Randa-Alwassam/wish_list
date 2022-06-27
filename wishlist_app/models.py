from django.db import models
from tkinter import CASCADE
import re

class ItemManager(models.Manager):
    def basic_validat(self, postData):
        errors = {}
        if len(postData["item"]) < 0:
            errors["item"] = "no empty entries"
        elif len(postData["item"]) < 3:
            errors["item"] = "item name should be more than 3 characters"
        return errors


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["name"]) < 3:
            errors["name"] = "name cannot be less than 3 characters long"
        elif len(postData["username"]) < 3:
            errors["username"] = "username cannot be less than 3 characters long"
            try:
                User.objects.get(username=postData["username"])
                errors["username"] = "Username is already exists try another one"
            except:
                pass
        if len(postData["password"]) < 8:
            errors["password"] = "password cannot be less than 8 characters "
        elif postData["password"] != postData["confirm"]:
            errors["confirm"] = "password doesn't match "
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField()
    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='created_items',on_delete=models.CASCADE)
    fav_users = models.ManyToManyField(User, related_name='fav_items',blank=True)
    date_created = models.DateTimeField(auto_now=True)
    objects = ItemManager()
    
