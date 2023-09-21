from django.shortcuts import render, redirect
from .models import User

def get_all_users():
    print("*******")
    return User.objects.all()


def get_all_online_users():
    print("*******")
    return User.objects.filter(is_online=True)

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    all_users = get_all_users()
    print(all_users)
    return render(request, 'chat/chat.html', {'users': all_users})


from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

########### register here #####################################
# views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User
from .models import Message

def create_user(user):
    user = User.objects.create(user=user, is_online=True)
    user.save()

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
 
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            create_user(user)
        else:
            print(form.errors.as_data())
        
        print(form.is_valid())
        #user=form.save()
        #create_user(user)

        print("***", get_all_users())    
        return redirect("/api")
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
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            user1=auth.models.User.objects.get(username=username)
            user = User.objects.get(user=user1)
            user.is_online=True
            user.save()
            return redirect('/api/online-users/')
        else:
            messages.info(request, f'account does not exit please sign in')
    form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form':form, 'title':'log in'})


def get_online_users(request):
    if request.method == 'GET':
        online_users=get_all_online_users()
        return render(request, 'chat/online.html', {'users':online_users})

def chat_start(request):
    #messages.info(request, f'let us chat with x')
    username = request.POST['username']
    print("user is ", username)
    user1=auth.models.User.objects.get(username=username)
    user = User.objects.get(user=user1)
    try:
        all_messages = Message.objects.get(sender=user1.id)
    except Message.DoesNotExist:
        all_messages = []
    return render(request, 'chat/chat.html', {'user':user, 'messages':all_messages})

def chat_send(request):
    #messages.info(request, f'Message is being sent')
    print("userid = ", request.user.id)
    #Message.objects.all().delete()
    content = request.POST['content']
    message = Message.objects.create(sender=request.user.user, receiver=request.user.user, content=content, timestamp=datetime.now())
    message.save()
    all_messages = Message.objects.all()
    return render(request, 'chat/chat.html', {'user':"user1", 'all_messages':all_messages})
