from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login, logout
from posts.models import UserProfile
from .forms import CustomUserCreationForm
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def register(request):
    if request.user.is_authenticated:  #ensure that after registered it should not get back to register page again
        return redirect("posts:newpost")
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            # Create an empty UserProfile for the newly registered user
            UserProfile.objects.create(user=user)
            
            # Log in the user immediately after registration
            login(request, user)
            return redirect("posts:newpost")
        else:
            # If form is not valid, render the form again with errors
            return render(request, "register.html", {"form": form})
    else:
        form = CustomUserCreationForm()

        return render(request, "register.html", {"form": form})
    

@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect("posts:newpost")
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user()) #if you login on page it will also get logged in admin if username and password is same
            if 'next' in request.POST:
                return redirect(request.POST.get('next')) #it will get valur of next
            else:
                return redirect("about")                
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{"form":form})

@never_cache
def logout_page(request):
    if request.method == "POST":
        logout(request)
        return redirect("authme:login")
