# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_REGEX = re.compile(r'[a-zA-Z0-9.,-]*$')

class UserManager(models.Manager):
    def sign_up(self, data):
        errors = {}
        if ( not NAME_REGEX.match(data['name']) or  not len(data['name']) or not len(data['username']) or not NAME_REGEX.match(data['username']) ):
            errors['name'] = 'Enter a valid name'
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Enter a valid email'
        if self.filter(username=data['username']):
            errors['name_exist'] = 'This username is taken'
        if self.filter(email=data['email']):
            errors['email_exist'] = 'This email already exists'
        if len(data['password']) < 8:
            errors['password'] = 'Your password must be 8 characters or more'
        if data['confirm_password'] != data['password']:
            errors['confirm_password'] = 'Your password doesnt match'
        if len(errors):
            return errors
        else:
            hash_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            return self.create(name=data['name'], email=data['email'], password=hash_password, username=data['username'])

    def log_in(self, data):
        errors = {}
        if self.filter(email=data['email']):
            user = self.get(email=data['email'])
            password = data['password']
            hash_password = bcrypt.hashpw(password.encode(), user.password.encode())
            if (hash_password == user.password):
                return user
            else:
                errors['password'] = 'Wrong password'
        else:
            errors['email'] = 'Invalid Email'
        return errors

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
