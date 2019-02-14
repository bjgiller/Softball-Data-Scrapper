import datetime
from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=30)

    def __str__(self):
        return self.team_name

class Team_RPI(models.Model):
    #team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30)
    rpi = models.IntegerField(default=(-1))

    def __str__(self):
        return self.team_name

class Game_Info(models.Model):
    team = models.CharField(max_length=30)
    opp_team = models.CharField(max_length=30)
    points = models.IntegerField(default=(-1))
    opp_points = models.IntegerField(default=(-1))
    date_start_time = models.DateTimeField(default=datetime.datetime.now())
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return (self.team + " | " + self.opp_team)

# Create your models here.


# Hashtag
