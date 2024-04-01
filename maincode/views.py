# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,password_validation, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import HttpResponseNotFound
# from .forms import UserRegistrationForm
from django.core.exceptions import ValidationError

from .models import notification_data
from .models import Job,SaveJob


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')




def signup_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:  # Check if passwords match
            # Check if username is already taken
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('signup_view')  # Redirect to the signup page
            else:
                # Create the user if username is unique and passwords match
                signupdata = User.objects.create_user(username=username, password=password1)
                signupdata.save()
                messages.success(request, 'Welcome')
                return redirect('login_view')  # Redirect to the login page after successful signup
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup_view')  # Redirect to the signup page if passwords don't match

    return render(request, 'registration/signup.html')


def signup_view(request):
    return render(request, 'registration/signup.html')

def home(request):
    if request.user.is_authenticated:
        data = Job.objects.all().order_by('-id')  
        return render(request, 'base/home.html', {'data': data})
    else:
        return redirect('login')
    
@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_home_data(request, jobs_id):
    jobdata = Job.objects.get(id=jobs_id)
    jobdata.delete()
    return redirect('home')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def addjobs(request):
    if request.method == 'POST':
        # Extract form data from the request
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        photo = request.FILES.get('photo')
        # Create a new Job instance and save it to the database
        new_job = Job(job_title=job_title, job_description=job_description, photo=photo)
        new_job.save()
        # Redirect to a success page or wherever you want
        return redirect('success_page') 
    else:
        return render(request, 'admin/addjobs.html')


def success_page(request):
    return render(request, 'admin/successpage.html')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def notification_submit(request):
    if request.method == 'POST':
        text_notification = request.POST.get('text_notification') 
        notify_data = notification_data(text_notification=text_notification)
        notify_data.save()
        return redirect('success_page')  
    else:
        return render(request, 'admin/addjobs.html')


def notificationpage(request):
    if request.user.is_authenticated:
        ndata = notification_data.objects.all().order_by('-id')  
        return render(request, 'base/notifications.html', {'notifydata': ndata})
    else:
        return redirect('login')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_notification(request,notifications_id):
    if request.user.is_authenticated:
        notifydata = notification_data.objects.get(id=notifications_id)
        notifydata.delete()
        return redirect('notificationpage')
    else:
        return render(request, 'base/notifications.html', {'ndata': notifydata})


@login_required
def savehome_submit(request, jobs_id):
    if request.user.is_authenticated:
        user = request.user
        job_id = jobs_id
        job = get_object_or_404(Job, id=job_id)
        
        # Check if the job is already saved by the user
        if not SaveJob.objects.filter(user=user, job=job).exists():
            # If not saved yet, create and save the SaveJob object
            save_job = SaveJob(user = request.user,job=job)
            save_job.save()
        
        return render(request, 'base/home.html')
    else:
        return render(request, 'base/home.html')

 

@login_required
def save_home_data(request):
        if request.user.is_authenticated:
            saveddata = SaveJob.objects.filter(user=request.user).order_by('-id')
            return render(request, 'base/save.html', {'saveddata': saveddata})
        else:
            return redirect('login')




@login_required
def saved_delete_home_data(request, savedjob_id):   
    saved_job = get_object_or_404(SaveJob, id=savedjob_id)
    saved_job.delete()
    return redirect('home')






   










@login_required
def apply_home_data(request):
        if request.user.is_authenticated:
            return render(request, 'base/apply.html')
        else:
            return render(request, 'base/apply.html')



@login_required
def manage_profile(request):
        if request.user.is_authenticated:
            return render(request, 'base/manageprofile.html')
        else:
            return render(request, 'base/manageprofile.html')

















# @login_required
# def notification_view(request):
#     ndata = notification_data.objects.all() 
#     return render(request, 'base/notifications.html', {'notifydata': ndata})


# def signup_register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         form  = UserRegistrationForm(request.POST)
        
#         if form.is_valid():
#             if  username is not None and password is not None :
        
#              if not User.objects.filter(username__iexact=username).exists():
        
#                 if password:
#                     try:
#                         password_validation.validate_password(password, User)
#                     except ValidationError as error:
#                         print(error)
#                         messages.info(request,''.join(x for x in error))
                    
#                         return render(request,'signup.html')     
#                 user = User.objects.create(username=username)
#                 user.set_password(password)
#                 user.save()


#             else:
        
#                 messages.info(request,f'username {username} already taken')
            
#             messages.info(request,"User Registered")
#             return redirect('registration/login.html')
#         else:
#             messages.info(request,'Please correct errors!')

#     return render(request,'registration/signup.html')



















# def paginator_view(request):
#     queryset = Job.objects.all()
#     paginator = Paginator(queryset, 10)  # Change 10 to your desired page size
#     page_number = request.GET.get('page')
#     try:
#         page_obj = paginator.page(page_number)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)  # If page is not an integer, show first page
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)  # If page is out of range, show last page
#     return render(request, 'your_template.html', {'page_obj': page_obj})



# def not_found_view(request, path):
#     return HttpResponseNotFound('<h1>Page not found</h1>')

