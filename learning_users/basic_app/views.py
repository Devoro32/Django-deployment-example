from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render (request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, NICE!!")

#by using @login_required, then the view (user_logout) needs to be first login
@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse ('index'))



def register(request):

    registered=False

    if request.method =="POST":
        user_form =UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid ():
            #if it is a valid post request, then it take the user information from the form and applies it to user
            user =user_form.save()
            #save the password as an hash
            user.set_password(user.password)
            user.save()

            #dont want to commit to the database yet as might get error in tryting to override the information
            profile = profile_form.save(commit=False)

            #this sets up the one to one relationship with the user  from the MODEL user=models.OneToOneField(User)
            profile.user =user

            if 'profile_pic' in request.FILES:
                profile.profile_pic= request.FILES['profile_pic']


            profile.save()

            registered =True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form =UserProfileInfoForm()

    #passing information to the template- registration.html that is in {%%}
    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})


def user_login(request):
    if request.method == 'POST':
        #getting the username and password from the login.html file with the same name
        v_username=request.POST.get('username')
        v_password =request.POST.get ( 'password')

        user =authenticate(username=v_username,password=v_password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed ")
            print ("Username:{} and password {}".format(v_username,v_password))
            return HttpResponse("invalid login details supplied")

    else:
        return render (request, 'basic_app/login.html',{})
