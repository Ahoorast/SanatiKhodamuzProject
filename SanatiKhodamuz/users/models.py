from cgi import print_exception
from turtle import title
from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import User

class customUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isEmployer = models.BooleanField(default=0)
    def __str__(self):
        return self.user.username


class work(models.Model):
    employer = models.ForeignKey(customUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=100)
    timeEstimate = models.TimeField #  doesn't work 
    description = models.CharField(max_length=500, default='nothing')
    pub_date = models.DateTimeField('date published', default = timezone.now())
    estimate = models.IntegerField(default=60)
    def __str__(self):
        return self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def show_estimate(self):
        inminutes = self.estimate
        inhours = inminutes / 60
        days = inhours / 24
        minutes = inminutes % 60
        hours = inhours % 24
        timeEstimateForWork = ""
        va = False
        days = int(days)
        hours = int(hours)
        if days:
            timeEstimateForWork += str(days) + " " + "روز" + " "
            va = True
        if hours > 0:
            if va:
                timeEstimateForWork += " " + "و "
            timeEstimateForWork += str(hours) + " " + "ساعت" + " "
        return timeEstimateForWork