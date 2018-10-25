from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        emailToCheck = postData['email']
        matchingEmail = User.objects.filter(email=emailToCheck) 
        errors = {}
        
        if len(postData['first_name']) < 1:
            errors["first_name"] = "First Name cannot be blank"
        elif len(postData['first_name']) < 3:
            errors["first_name"] = 'First Name has to be atleast 3 characters'
        elif not re.match("^[A-Za-z]*$", postData['first_name']):
            errors["first_name"] = 'First Name can only contain letters. No numbers allowed!'


        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last Name cannot be blank"
        elif len(postData['last_name']) < 3:
            errors["last_name"] = 'Last Name has to be atleast 3 characters'
        elif not re.match("^[A-Za-z]*$", postData['last_name']):
            errors["last_name"] = 'Last Name can only contain letters. No numbers allowed!'
        
        if len(postData['email']) < 1:
            errors['email'] = 'Email is required. Cannot be empty'
        elif len(matchingEmail) != 0:
            errors['email'] = 'Email already exists.'
        
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be atleast 8 characters'
        elif postData['password'] != postData['password_confirm']:
            errors["password"] = 'Must match password confirmation field'
        
        return errors
    
    def login_validator(self, postData):
        emailToCheck = postData['email']
        matchingEmail = User.objects.filter(email=emailToCheck) 
        errors = {}
        
        if len(postData['email']) < 1:
            errors['email'] = 'Enter your email to login'
        elif len(matchingEmail) == 0:
            errors['email'] = 'Email not recognized. Please register.'
        if len(postData['password']) < 1:
            errors['password'] = 'Please enter your password'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}

        if len(postData['destination']) < 1:
            errors['destination'] = "Must provide a destination"
        # elif not re.match("^[A-Za-z]+,*$", postData['destination']):
        #     errors['destination'] = 'Location can only contain letters. No numbers allowed!'
        
        if len(postData['start']) < 1:
            errors['start'] = 'Must enter a start date'

        else:
            start = datetime.strptime(postData['start'], "%Y-%m-%d")
            end = datetime.strptime(postData['end'], "%Y-%m-%d")
            if start < datetime.now():
                errors['start'] = 'Start date must be in the future'
            if end < start:
                errors['end'] = 'End date must be after start date'

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=200)
    start = models.DateField()
    end = models.DateField()
    plan = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, related_name="uploader")
    join = models.ManyToManyField(User, related_name="joined")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()