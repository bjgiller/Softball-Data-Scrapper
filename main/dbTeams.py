from django.utils import timezone
from django.db.models import Q
from main.models import Team

class DB_Teams_Interface:
    def __init__(self):
        self.g = None

    def create_single_rating_info(self,team,conf,div):
        self._add_to_db(team,conf,div,False)

    def create_teams_from_dict(self,dict):
        for i in dict:
            div = i
            cur_div = dict.get(i)
            for j in cur_div:
                team = j
                conf = cur_div.get(j)
                self._add_to_db(team,conf,div,False)


    def _add_to_db(self,team,conf,div,override):
        if not override:
            if not Team.objects.filter(team_name=team,conference=conf,division=div).exists():
                self.g = Team(team_name=team,conference=conf,division=div)
                self.g.save()
        else:
            self.g = Team(team_name=team,conference=conf,division=div)
            self.g.save()

    def clear_table(self):
        for i in Team.objects.all():
            i.delete()
