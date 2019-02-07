import datetime
from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=30)
    year = models.IntegerField(('year'), default=datetime.date.today().year)
    pub_date = models.DateTimeField('date published')
    prev_year_rank = models.IntegerField(default=(-1))
    cur_year_rank = models.IntegerField(default=(-1))

    def __str__(self):
        return self.team_name

class Score(models.Model):
    team = models.ForeignKey(Team, related_name = 'team', on_delete=models.CASCADE)
    opp_team = models.ForeignKey(Team, related_name = 'opp_team', on_delete=models.CASCADE)
    venue = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    date_start_time = models.DateTimeField(default=datetime.datetime.now())
    points = models.IntegerField(default=(-1))

    def __str__(self):
        return self.team

# Create your models here.


# Hashtag