from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Job(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #applicants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
    
# class Company(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE)
#     body = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.body[0:50]