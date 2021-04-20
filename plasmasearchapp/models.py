from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField
# Create your models here.

class Userinfo(models.Model):

    user= models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null = True
    )
    type = (
        ('donor', 'donor'),
        ('recipient', 'recipient'),
    )
    genderchoices = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    quartypes = (
        ('hospitalized', 'Hospitalized'),
        ('homequar', 'Home Quarantined'),
    )
    bgtypes = (
        ('A+ve', 'A+ve'),
        ('A-ve', 'A-ve'),
        ('B+ve', 'B+ve'),
        ('B-ve', 'B-ve'),
        ('AB+ve', 'AB+ve'),
        ('AB-ve', 'AB-ve'),
        ('O+ve', 'O+ve'),
        ('O-ve', 'O-ve'),      
    )    
    type = models.CharField(max_length=30,choices=type,default='recipient')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profilepic = models.ImageField()
    phoneno = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=30,choices=genderchoices)
    desctext =models.CharField(max_length=30)
    covidnegcert = models.ImageField(null=True)
    covidnegdate = models.DateField()
    quartype = models.CharField(max_length=30,choices=quartypes)
    govtid = models.ImageField()
    bloodgroup = models.CharField(max_length=30,choices=bgtypes)
    lat = models.CharField(max_length=30 , null = True)
    long = models.CharField(max_length=30, null = True)
    sentotp = models.CharField(max_length=30, null = True)
    phoneverified = models.BooleanField(default=False)
    isapproved = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class requestplasma(models.Model):

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = True,
        related_name='user1'
    )
    donee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = True,
        related_name='user2'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = BooleanField(default=False)
    

    def __str__(self):
        return self.donor.username



