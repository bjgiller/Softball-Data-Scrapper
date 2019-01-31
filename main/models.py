import datetime
from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=30,primary_key=True)
    year = models.IntegerField(_('year'), default=datetime.date.today().year,primary_key=True)
    pub_date = models.DateTimeField('date published')
    prev_year_rank = models.IntegerField(default=(-1))
    cur_year_rank = models.IntegerField(default=(-1))

    def __str__(self):
        return self.team_name

class Score(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    opp_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    venue = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    date = models.DateField(default=datetime.datetime.today())
    start_time = models.TimeField(default=datetime.datetime.now().time())
    points = models.IntegerField(default=(-1))

    def __str__(self):
        return self.team

# Create your models here.
