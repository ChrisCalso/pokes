from __future__ import unicode_literals
import bcrypt
import re
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z\s]\w+')
class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for email
        if len(self.filter(username=post_data['username'])) > 0:
            # check this user's password
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Password Incorrect!')
        else:
            errors.append('Username not found!')
        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []

        #error handling for name fields
        if len(post_data['name']) < 2:
            errors.append("Names must be at least 3 characters!")

        if len(post_data['username']) < 2:
            errors.append("Username must be at least 3 characters!")

        #error handling for passwords
        if len(post_data['password']) < 8:
            errors.append("Passwords must be at least 8 characters!")

        # error handling for  letter characters
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Names must contain letter characters only!')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email_format'] = "Wrong email format"
        if User.objects.filter(email=post_data['email']).count() > 0:
            errors['email'] = "Email {} already exists".format(post_data['email'])

        #error handling for uniqueness of username
        if len(User.objects.filter(username=post_data['username'])) > 0:
            errors.append("This username is already in use!")

        #error handling for password matches
        if post_data['password'] != post_data['password_confirm']:
            errors.append("Passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw(
                (post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                email= post_data['email'],
                password=hashed,
            )
            return new_user
        return errors
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "<Users - user: {}, {}>".format(self.name, self.username)

class PokeManager(models.Manager):
    def createPoke(self, currentuser, user_id):
        self.create(
            poker=User.objects.get(id=currentuser),
            poked=User.objects.get(id=user_id)
        )

class Poke(models.Model):
    pokedate = models.DateTimeField(auto_now_add=True)
    poker = models.ForeignKey(User, related_name="whopoked")
    poked = models.ForeignKey(User, related_name="gotpoked")
    objects = PokeManager()
    def __repr__(self):
        return "<Pokes - poker: {}, poked: {}, pokedate: {}>".format(self.poker, self.poked, self.pokedate)
