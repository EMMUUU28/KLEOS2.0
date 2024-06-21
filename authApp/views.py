from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required


# Create your views here.

# def login(request):
#     return render(request,'auth/login.html')

@login_required
def home(request):
    return render(request,'auth/home.html')

# def signup(request):
#     return render(request,'auth/signup.html')      




def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        print("got user register data ", username, password, email)
        # Check if the username is unique
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email) # Create a new user
            # gotuserData = MyserData.objects.create(
            #                                 user_name=username,
            #                                 email=email,
            #                                 password=password,

            #                                 intrest ='["Python", "Tailwind-CSS", "Django", "Data Science"]',
            #                                 skills  ='["JAVA", "Mongo DB", "Statistics"]',
            #                                 courses ='["Python", "DBMS", "Algorithms"]',
            #                                 dreamcompany = '["JP Morgan", "Media.net", "Google", "Microsoft"]',

            #                                 strength = "['Programming', 'Statistics', 'Machine Learning', 'Data Visualization', 'Problem Solving']",
            #                                 strengthvalues = "[4, 3, 5, 2, 4]",
            #                                 Description = 'Hi, I’m Alice, Decisions: If you can’t decide, the answer is no. If two equally difficult paths, choose the one more painful in the short term (pain avoidance is creating an illusion of equality).', 
            #                                 )

            return redirect('login')  # Redirect to your login view
        else:
            error_message = 'Username already exists'
    else:
        error_message = None

    return render(request, 'auth/signup.html', {'error_message': error_message})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # Redirect to your dashboard view
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = None

    return render(request, 'auth/login.html', {'error_message': error_message})


# def user_logout(request):
    # logout(request)
    # return redirect('user_login')  # Redirect to your login view