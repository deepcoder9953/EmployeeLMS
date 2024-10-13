from django.db import models
from django.contrib.auth.models import User

class Empform(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=20)
    address = models.TextField(max_length=30)
    position = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.username
    
class LeaveApplication(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50, choices=[('Sick', 'Sick'), ('Emergency', 'Emergency'), ('Maternity', 'Maternity')])
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)  
    is_rejected = models.BooleanField(default=False)  
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.username}-{self.leave_type}'
    
    def duration(self):
        return(self.end_date - self.start_date).days +1


class UserProfile(models.Model):
    photo = models.ImageField(upload_to= 'images', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.full_name