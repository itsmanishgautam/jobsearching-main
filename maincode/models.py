from django.db import models
from django.contrib.auth import get_user_model

User  = get_user_model()
    # Return the User model that is active in this project.



# Create your models here.


class Job(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    photo = models.ImageField(upload_to='job_photos/', null=True, blank=True)
    # text_notification = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.job_title

class notification_data(models.Model):
    text_notification = models.CharField(max_length=100)

    def __str__(self):
        return self.text_notification
    
class SaveJob(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
    # This means that a user cannot save the same job multiple times.

    def __str__(self):
        return self.user
    

    

class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    experience = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')

