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
from django.http import HttpResponse
from django.http import HttpResponseForbidden

from .models import notification_data
from .models import Job,SaveJob,Application


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



# def signup_register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         superkey = request.POST.get('superkey')


#         if password1 == password2: 
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username is already taken')
#                 return redirect('signup_view') 
#             else:
#                 signupdata = User.objects.create_user(username=username, password=password1)
#                 signupdata.save()

#                 if superkey == 'iamadmin':
#                     supersignupdata = User.objects.create_superuser(username=username, password=password1)
#                     supersignupdata.save()

#                 messages.success(request, 'Welcome')
#                 return redirect('login_view')  
#         else:
#             messages.error(request, 'Passwords do not match')
#             return redirect('signup_view') 

#     return render(request, 'registration/signup.html')



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
def delete_home_data(request, job_id):
    jobdata = Job.objects.get(id=job_id)
    jobdata.delete()
    return redirect('home')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def addjobs(request):
    if request.method == 'POST':
        

        ndata = Application.objects.all().order_by('-id')  



        # Extract form data from the request
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        photo = request.FILES.get('photo')
        # Create a new Job instance and save it to the database
        new_job = Job(job_title=job_title, job_description=job_description, photo=photo)
        new_job.save()
        # Redirect to a success page or wherever you want
        # return redirect('success_page') 
        return render(request, 'admin/addjobs.html', {'application': ndata})
    
    else:
        ndata = Application.objects.all().order_by('-id')  
        return render(request, 'admin/addjobs.html', {'application': ndata})
        # return render(request, 'admin/addjobs.html')


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
def savehome_submit(request, job_id):
    if request.user.is_authenticated:
        user = request.user
        job = get_object_or_404(Job, id=job_id)
        
        if not SaveJob.objects.filter(user=user, job=job).exists():
            save_job = SaveJob(user = request.user,job=job)
            save_job.save() 
        return redirect('home') 
    else:
        return redirect('home')
    

 

@login_required
def save_home_data(request):
        if request.user.is_authenticated:
            saveddata = SaveJob.objects.filter(user=request.user).order_by('-id')
            return render(request, 'base/save.html', {'saveddata': saveddata})
            # return redirect('home')
        else:
            return redirect('login')




@login_required
def saved_delete_home_data(request, savedjob_id):   
    saved_job = get_object_or_404(SaveJob, id=savedjob_id)
    saved_job.delete()
    
    return redirect('save_home_data')




@login_required
def manage_profile(request):
        if request.user.is_authenticated:
            return render(request, 'base/manageprofile.html')
        else:
            return render(request, 'base/manageprofile.html')



def changesignupdata(request):
    if request.method == 'POST':
        current_user = request.user
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:     
                current_user.set_password(password1)
                current_user.save()
                messages.success(request, 'Password Changed')
                return redirect('manage_profile') 
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('manage_profile')

    return redirect('manage_profile')




@login_required
def apply_home_data(request):
    if request.user.is_authenticated:
        saveddata = Application.objects.filter(user=request.user).order_by('-id')
        data = Job.objects.all().order_by('-id')  
        context = {
            'applieddata': saveddata,
            'datas': data
        }
        return render(request, 'base/applied.html', context)
    else:
        return render(request, 'base/applied.html')
        



def applyportal_home_data(request, job_id): 
    saveddata = Job.objects.filter(id=job_id)  # Assuming job_id is a field in the Job model

    context = {'data': saveddata}  # Corrected context dictionary

    return render(request, 'base/applyjobtemp.html', context)




def applydata_submit(request, job_id):
    if request.method == 'POST':
        user = request.user
        job = Job.objects.get(id=job_id)

        # Check if the user has already applied for the job
        if Application.objects.filter(job=job, user=user).exists():
            return HttpResponseForbidden("You have already applied for this job.")
        else:

            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            experience = request.POST.get('experience')
            resume = request.FILES['resume']
            
            # Create and save the application
            application = Application.objects.create(
                job=job, user=user, fullname=fullname, email=email, phone=phone, 
                experience=experience, resume=resume
            )
            application.save()
            
            # return redirect('success_page')  # Redirect to a success page or any other page
            return render(request,'base/applysuccess.html')
    else:
        pass
    # else:
    #     job = Job.objects.get(id=job_id)
    #     return render(request, 'apply_job.html', {'job': job})






def search_data(request):
    if request.method == 'POST':
        text = request.POST.get('text')  
        if text:  # Check if text is not empty
            results = Job.objects.filter(job_title__icontains=text) | Job.objects.filter(job_description__icontains=text)
            return render(request, 'base/searchedresult.html', {'results': results, 'query': text})
        else:
            return redirect('home')
    else:
        return redirect('home')















def signup_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        superkey = request.POST.get('superkey')

        # Check if passwords match
        if password1 == password2:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('signup_view')  # Redirect to signup page with error message
            else:
                # Create a new user
                signupdata = User.objects.create_user(username=username, password=password1)
                signupdata.save()

                # Check if superkey is provided
                if superkey == 'iamadmin':
                    # Create a superuser
                    supersignupdata = User.objects.create_superuser(username=username, password=password1, superkey = superkey)
                    supersignupdata.save()

                messages.success(request, 'Account created successfully')
                return redirect('login_view')  # Redirect to login page after successful signup
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup_view')  # Redirect to signup page with error message

    return render(request, 'registration/signup.html')





































