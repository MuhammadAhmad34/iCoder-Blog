from django.db import models

# Create your models here.
class Contact_US(models.Model):
    full_Name = models.CharField(max_length=100)
    phone_Number = models.CharField(max_length=12)
    email = models.CharField(max_length=100)
    message = models.TextField()


class RegisterUser(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    publish_Date = models.CharField(max_length=12)
    auther_name = models.CharField(max_length=20)
    blog_content = models.TextField()