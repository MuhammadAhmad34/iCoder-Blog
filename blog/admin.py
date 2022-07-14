from django.contrib import admin
from .models import Contact_US, Blog, RegisterUser
# Register your models here.

class Contact_AdimView(admin.ModelAdmin):
    list_display = ('full_Name', 'phone_Number', 'email', 'message')

admin.site.register(Contact_US,Contact_AdimView)


class RegisterUser_AdminView(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'username', 'email', 'password')
admin.site.register(RegisterUser, RegisterUser_AdminView)

class BlogAdminView(admin.ModelAdmin):
    list_display = ("blog_title", "publish_Date", 'auther_name', 'blog_content')
admin.site.register(Blog, BlogAdminView)