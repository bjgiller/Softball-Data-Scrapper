from django.utils import timezone
from django.db.models import Q
from main.models import Team_RPI

class DB_RPI_Interface:
    def __init__(self):
        self.g = None

    def get_by_team(self,team):
        return Team_RPI.objects.filter(team_name=team)

    def get_top(self,numb):
        return Team_RPI.objects.all().order_by('-rpi')[:numb]

    def get_bottom(self,numb):
        return Team_RPI.objects.all().order_by('rpi')[:numb]

    def create_single_rating_info(self,team,wp,owp,oowp,bonus,rpi):
        self._add_to_db(team,wp,owp,oowp,bonus,rpi,True)

    def _add_to_db(self,team,wp,owp,oowp,bonus,rpi,override):
        exists = Team_RPI.objects.filter(team_name=team).exists()

        #overriding
        if override and exists:
                self.g = Team_RPI.objects.get(team_name=team)
                self.g.wp = wp
                self.g.owp = owp
                self.g.oowp = oowp
                self.g.bonus = bonus
                self.g.rpi = rpi
                self.g.save()
        #adding
        else:
            self.g = Team_RPI(team_name=team,wp=wp,owp=owp,oowp=oowp,bonus=bonus,rpi=rpi)
            self.g.save()

    def clear_table(self):
        for i in Team_RPI.objects.all():
            i.delete()

    '''

    def get_by_date_start_time(self,date_start_time):
        return Game_Info.objects.filter(date_start_time=date_start_time)

    def get_by_team(self,team):
        return Game_Info.objects.filter(Q(team=team) | Q(opp_team=team))

    def get_by_date_range(self,date_start_time,date_end_time):
        return Game_Info.objects.filter(date_start_time=date_start_time)

    def get_all_teams(self):
        allGames = Game_Info.objects.all()
        setAllTeams = {""}
        setAllTeams.clear()
        for i in range(len(allGames)):
            setAllTeams.update({allGames[i].team})
            setAllTeams.update({allGames[i].opp_team})

        return setAllTeams


    def create_single_game_info(self,team,opp_team,points,opp_points,date_start_time):
        self._add_to_bd(team,opp_team,points,opp_points,date_start_time,False)

    def create_games_from_list(self,game_list):
        #will follow the structure of [game{"team name":score,"team_name",score},game{"team name":score,"team_name",score}]
        for i in range(len(game_list)):
            dict = game_list[i]
            team1 = list(dict.keys())[0]
            team2 = list(dict.keys())[1]
            score1 = dict.get(team1)
            score2 = dict.get(team2)
            date_start_time = dict.get("date_start_time")

            print(team1 + "|" + score1 + "|" + team2 + "|" + score2)

            self._add_to_db(team1,team2,score1,score2,date_start_time,False)

    def _add_to_db(self,team,opp_team,points,opp_points,date_start_time,override):
        if not override:
            if not Game_Info.objects.filter(team=team,opp_team=opp_team,points=points,opp_points=opp_points,date_start_time=date_start_time).exists():
                self.g = Game_Info(team=team,opp_team=opp_team,points=points,opp_points=opp_points,date_start_time=date_start_time,pub_date=timezone.now())
                self.g.save()
        else:
            self.g = Game_Info(team=team,opp_team=opp_team,points=points,opp_points=opp_points,date_start_time=date_start_time,pub_date=timezone.now())
            self.g.save()

    def clear_table(self):
        for i in Game_Info.objects.all():
            i.delete()

    '''
