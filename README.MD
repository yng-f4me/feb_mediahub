### CREATING A DJANGO APP WITH DB 
- Step 1 : set up the necessary configs for your project 
    For MediaHUB our configs are 
    a. Media files url 
    b. Templates directory 
    c. Redirect URLs 
    d. Cloudinary configs for media management 
    e. Custom auth model override 

- Step 2 : register our cloudinary credentials 
### Accounts app 
- Step 3 : set up our custom user model /schema - i.e. the table to be created on migration  
- Step 4 : install pillow for media file management i.e. the files that are not to be saved on cloudinary (pip install pillow)
- step 5 : run the migrations for the accounts app
 - python manage.py makemigrations
 - python manage.py migrate

 ## TEMPLATING (creation of user interfaces)
 - for our app our templates directory is set on the root folder.
 - we will have two app folders for each of our apps interfaces 
 - a base.html will provide links to stylesheets and other html meta-data information 
### For the form fields 
- IN each app for data collected specify the fields in a forms.py file 
- accounts : UserLoginForm , UserRegistrationForm, UserProfileForm
### Next work on the views methods for the request/response cycles
-views.py - register, login , profile , forgot password processes 
- the views will then be mapped to a url in the apps urls.py
### Next step will be to map our views as urls
## paths for the user to access the pages
- inside the apps urls.py 
### Next step is to set up our admin content management for the app
- inside the apps admin.py
### Next step is to configure our apps.py in the 
## apps folder to allow auto incrementation for our 
## ids 
- inside the apps apps.py 
## Next step is to register our apps urls to the 
## projects urls file 
- inside the project folder's urls.py 

### Test the project 
python manage.py runserver

### ADMIN CONFIGURATION 
- Set up administrative credentials 
python manage.py createsuperuser 
- give username,email and password combo 
- access admin by going to the route /admin
http://127.0.0.1:8000/admin

### MPESA INTEGRATION
- Daraja API sandbox: create an account here :
https://developer.safaricom.co.ke/
- Create an app in above portal - get development keys
- Django processes: sample media app
1. Create mediampesa app
2. Models, templates, admin, forms