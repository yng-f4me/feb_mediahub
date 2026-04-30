'''
# render : will load a html page 
# redirect : will redirect user to specific html pages based on
completed activity 
'''
from django.shortcuts import render,redirect 
'''django inbuilt auth functions that return true or false based 
on the process
login = returns True if user is currently logged in 
logout = returns True if the user successfully logs out 
authenticate = returns True if the user provides correct credentials
for a login process 
'''
from django.contrib.auth import login, logout, authenticate
'''return true or false if the user is logged in or not and 
allow execution of a function based on that result'''
from django.contrib.auth.decorators import login_required
'''message alerts : notifications'''
from django.contrib import messages
'''require the configured form views for the password reset process'''
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
'''only load views when required: reverse_lazy '''
from django.urls import reverse_lazy
'''import form files from your apps forms.py'''
from .forms import UserRegistrationForm,UserLoginForm,UserProfileForm
# Create your views here.
## registration process / sign-ups 
def register_view(request):
    # check if user is already logged 
    # django always maintains our user object 
    if request.user.is_authenticated:
        # if user is already authenticated take them to dashboard
        return redirect('media_assets:dashboard')
    
    # check the type of request method 
    # when submitting the form the request is POST 
    # when viewing the form the request is default GET
    if request.method  == 'POST':
        # create the form reference for registration frm forms.py
        form = UserRegistrationForm(request.POST)
        # if all form inputs are filled we save details to the db 
        # form.is_valid checks if all forms fields are filled 
        # correctly
        if form.is_valid():
            user = form.save() ## save() submits details to our db 
            login(request,user) ## saving our login state for the user
            messages.success(request, 
            f'welcome {user.username} Your account has been created'
            )
            # redirect user to our dashboard 
            return redirect('media_assets:dashboard')
    else:
        form = UserRegistrationForm() # default get process5

    return render(request, 'accounts/register.html', 
    {'form' : form})
# Login process 
def login_view(request):
    # check if user is already logged in 
    if request.user.is_authenticated:
        return redirect('media_assets:dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        # check if fields are filled 
        if form.is_valid():
            # pick up username and password entries 
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # use django method authenticate from django 
            # to login user 
            user = authenticate(request, username=username,
            password=password) # query db for the user 
            if user is not None:
                login(request,user) # login user
                messages.success(request, 
                f'Welcome back {user.username}') 
                return redirect('media_assets:dashboard')   
    else:
        form = UserLoginForm(request) 
    return render(request, 'accounts/login.html',{'form' : form})

## logout 
## ensure the user is logged in by use of the decorator method 
## @login_required 
@login_required # the function defined below will work if only this 
# decorators returns true i.e. only if user is logged in 
def logout_view(request):
    # use django inbuilt log out method 
    logout(request)
    messages.info(request, f'You have logged out!!')
    return redirect('accounts:login')

# profile update
@login_required
def profile_view(request):
    if request.method == 'POST':
        # request.POST - will pick text data 
        # request.FILES - will pick media data 
        # instance - will tag current logged in user 
        form = UserProfileForm(request.POST,request.FILES,
        instance=request.user)
        # check if all fields filled 
        if form.is_valid():
            form.save() # update the user profile 
            messages.success(request, f"Profile saved!!")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request,'accounts:profile.html', {'form':form})

# views for our password reset 
# django inbuilt configs for process 
class CustomPasswordResetView(PasswordResetView):
    # interface change 
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    # reverse lazy will ensure view is added when needed 
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # interface change 
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

