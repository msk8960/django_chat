from django.shortcuts import render, redirect
from .models import User

from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

########### register here #####################################
# views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User
from .models import Message


def get_all_users():
    print("*******")
    return User.objects.all()


def get_all_online_users():
    print("*******")
    return User.objects.filter(is_online=True)


def create_user(user):
    user = User.objects.create(user=user, is_online=True)
    user.save()

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        
        print("***", get_all_users()) 
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            create_user(user)
            print("redirecting")
            form = login(response, user)
            return redirect("/api/online-users")
        else:
            print(form.errors.as_data())
    else:
        form = RegisterForm()

    return render(response, "chat/register.html", {"form":form})

################ login forms###################################################
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import auth

from datetime import datetime

def user_login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            
            logged_user = User.objects.get(user=user)
            logged_user.is_online=True
            logged_user.save()
            return redirect('/api/online-users/')
        else:
            messages.info(request, f'account does not exit please sign in')
    form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form':form, 'title':'log in'})


def get_online_users(request):
    if not request.user.is_authenticated:
        return redirect("login-user")

    if request.method == 'GET':
        online_users=get_all_online_users()
        return render(request, 'chat/online.html', {'users':online_users})


def chat_start(request):
    if not request.user.is_authenticated:
        return redirect("login-user")

    #messages.info(request, f'let us chat with x')

    if not "username" in request.POST:
        messages.error(request, f'please select user to start message')
        return redirect("online-users")

    username = request.POST['username']
    print("start user is ", username)
    user1=auth.models.User.objects.get(username=username)
    user = User.objects.get(user=user1)
    try:
        all_messages = Message.objects.filter(sender=user1.id)
    except Message.DoesNotExist:
        all_messages = []
    return render(request, 'chat/chat.html', {'user':user, 'all_messages':all_messages})


def chat_send(request):
    if not request.user.is_authenticated:
        return redirect("login-user")

    #messages.info(request, f'Message is being sent')
    print("userid = ", request.user.id)

    if not "username" in request.POST:
        messages.error(request, f'please select user to send message')
        return redirect("online-users")

    username = request.POST['username']
    print("user is ", username)
    user1=auth.models.User.objects.get(username=username)
    receiver = User.objects.get(user=user1)

    #Message.objects.all().delete()
    content_message = request.POST['content']
    message = Message.objects.create(sender=request.user.user, receiver=receiver, content=content_message, timestamp=datetime.now())
    message.save()
    all_messages = Message.objects.filter(sender=request.user.user).filter(receiver=receiver)|Message.objects.filter(receiver=request.user.user).filter(sender=receiver)
    return render(request, 'chat/chat.html', {'user':receiver, 'all_messages':all_messages})
