from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Job(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    photo = models.ImageField(upload_to='job_photos/', null=True, blank=True)
    # text_notification = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class notification_data(models.Model):
    text_notification = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    
class savejob(models.Model):
    save_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Save the current user
    
    def __str__(self):
        return self.title
    