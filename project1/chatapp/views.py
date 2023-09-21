from django.shortcuts import render, redirect
from .models import User

def get_all_users():
    print("*******")
    return User.objects.all()


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("login-user")
    
    all_users = get_all_users()
    print(all_users)
    return render(request, 'chat/chat.html', {'users': all_users})


from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="chat/register.html", context={"register_form":form})


########### register here #####################################
# views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User

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
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form, 'title':'log in'})



#from django.http import HttpResponse

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")