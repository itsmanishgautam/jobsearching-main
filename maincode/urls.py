"""
URL configuration for jobsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from maincode import views
from django.views.generic import RedirectView
# from .views import custom_logout
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login_view'),

    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup/'),

    path('signup/', views.signup_view, name='signup_view'),

    path('signupdata/', views.signup_register, name='signupdata/'),
    path('addjobs/',views.addjobs, name='addjobs'),
    path('delete/<int:job_id>', views.delete_home_data, name='delete_home_data'),
    path('success/', views.success_page, name='success_page'),
    path('notification/',views.notificationpage,name='notificationpage'),
    path('noficationsubmit/',views.notification_submit,name='notification_submit'),
    path('notification/<int:notifications_id>', views.delete_notification, name='delete_notification'),
    path('manageprofile/',views.manage_profile,name='manage_profile'),
    path('savejobhome/<int:job_id>/',views.savehome_submit,name='savehome_submit'),
    path('savejobs/', views.save_home_data, name='save_home_data'),

    

    path('applied/', views.apply_home_data, name='apply_home_data'),
    path('applieddata/<int:job_id>', views.applydata_submit, name='applydata_submit'),





    path('savedelete/<int:savedjob_id>/',views.saved_delete_home_data,name='saved_delete_home_data'),
    path('applyjobhome/<int:job_id>/',views.applyportal_home_data,name='applyportal_home_data'),
    path('changesignupdata/',views.changesignupdata,name='changesignupdata'),
    










    path('applyjobs/', views.apply_home_data, name='apply_home_data'),










    #forproduction
    # path('<path:path>/', views.not_found_view),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
