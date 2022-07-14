from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import RegisterUser, Contact_US, Blog


# HTML Pages
def home(request):
    data = {}
    # for Home Page
    blogs = Blog.objects.all()

    #  Heandling Blog Search
    if request.method == "POST":
        searchBlog = str(request.POST.get('search'))
        print(len(searchBlog))
        if len(searchBlog) != 0:
            if searchBlog is not None:
                try:
                    searchData = Blog.objects.filter(blog_title=searchBlog)
                    data.update({"allBlogs": searchData})
                    return render(request, 'home.html', data)
                except Exception as e:
                    print(e)
                    data.update({"condition": True,
                                 "status": "[ERR] -> 404 Not Found"})
                    return render(request, 'home.html', data)
        else:
            data.update(
                {"condition": True, "status": "[ERR] -> 404 Not Found"})
            return render(request, 'home.html', data)

    data.update({"allBlogs": blogs})
    return render(request, 'home.html', data)


def contact(request):
    data = {}
    if request.method == "POST":
        Name = request.POST.get('FullName')
        Email = request.POST.get('email')
        phone_Number = request.POST.get('PhoneNumber')
        messages = request.POST.get('message')
        print(
            f'Name:{Name}\n email:{Email} \n Phone Number: {phone_Number}\n Message: {messages}')

        try:
            ContactUser = Contact_US(
                full_Name=Name, phone_Number=phone_Number, email=Email, message=messages)
            ContactUser.save()
            data.update(
                {"condition": True, "status": "The Message Has Been Sent Successfully.."})
            return render(request, 'contact.html', data)
        except Exception as e:
            print(e)
            data.update(
                {"condition": True, "status": "[INFO] => 503 : Service Unavailable"})
            return render(request, 'contact.html', data)

    return render(request, 'contact.html')


def addBlog(request):
    data = {}
    if request.method == "POST":
        blogTitle = request.POST.get('blogTitle')
        publishDate = request.POST.get('publishDate')
        autherName = request.POST.get('autherName')
        blogContent = request.POST.get('blogContent')
        # print(f"\nBlog Title: {blogTitle}\n Publish Date: {publishDate}\n Writer Name: {autherName}\n Blog Content: {blogContent}")
        try:
            Save_Blog = Blog(blog_title=blogTitle, publish_Date=publishDate,
                             auther_name=autherName, blog_content=blogContent)
            Save_Blog.save()
            data.update(
                {"condition": True, "status": "Blog Has Been Published"})
            return render(request, 'blog.html', data)
        except Exception as e:
            data.update(
                {"condition": True, "status": "[ERR: 500] -> inertnal Server Error"})

    return render(request, 'blog.html')

# Display All Details


def detailBlog(request, id):
    blog_Info = Blog.objects.get(id=id)
    data = {"BlogInfo": blog_Info}

    return render(request, 'detail.html', data)

# Autentication APIs


def loginPage(request):

    passcount = 3

    '''
    
    Login page handle here
    
    '''
    data = {}
    if request.method == 'POST':
        loginuserName = request.POST.get('loginuserName')
        loginpassword = request.POST.get('loginpassword')
        user = authenticate(username=loginuserName, password=loginpassword)
        # print(user)
        if user is not None:
            login(request, user)
            print("User Logeed In ")
            return HttpResponseRedirect("/")
        else:
            passcount = passcount + 1
            print(passcount)
            data.update({"condition": True,
                         "status": " invalid Credentials Please Try Again"})
            if passcount >= 4:
                data.update({"Cond": True, "stat": "Forgot Password"})
                return render(request, 'login.html', data)

            return render(request, 'login.html', data)

    return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return HttpResponseRedirect("/login/")


def registerUser(request):
    param = {}
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('LastName')
        userName = request.POST.get('UserName')
        email = request.POST.get('email')
        password = request.POST.get('Password')
        confirmPass = request.POST.get('ConfirmPassword')

        #  UserName Validation

        if len(userName) > 10:
            param.update({"status": "[Error] --> User Name too long..",
                          'condition': True, })
        if not userName.isalnum():
            param.update({"status": "[Error] --> User Name should only contain Letters and Numbers..",
                          'condition': True, })
        # Checking Email and username already exists or Not

        if RegisterUser.objects.filter(email=email).exists():
            param.update(
                {"status": "[Error] --> Email Already Exist..", 'condition': True, })

            return render(request, 'index.html', param)
        elif RegisterUser.objects.filter(username=userName).exists():
            param.update(
                {"status": "[Error] --> User Name Already Exist..",
                    'condition': True, }
            )
            return render(request, 'index.html', param)

        else:
            # Checking Passwords
            if password == confirmPass:
                user = RegisterUser(firstName=firstName, lastName=lastName,
                                    username=userName, email=email, password=password)
                user.save()
                param.update(
                    {"status": "User Successfully Register", 'condition': True})
                messages.success(request, 'Succfully Registered ')

                # Create User
                myUser = User.objects.create_user(userName, email, password)
                myUser.first_name = firstName
                myUser.last_name = lastName
                myUser.save()
                print("iCoder Account successfully created")
                return HttpResponseRedirect('/login/')
                print(userName, email, password, confirmPass)
            else:
                param.update(
                    {
                        "status": "Worng Password",
                        "condition": True,
                    }
                )
                return render(request, 'index.html', param)
    return render(request, 'index.html')
