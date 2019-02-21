from django.utils import timezone
from main.models import Game_Info

class DB_Game_Interface:
    def __init__(self):
        self.g = None

    def create_single_game_info(self,team,opp_team,points,opp_points,date_start_time):
        self.g = Game_Info(team=team,opp_team=opp_team,points=points,opp_points=opp_points,date_start_time=date_start_time,pub_date=timezone.now())
        self.g.save()

    def create_games_from_list(self,game_list):
        #will follow the structure of [game{"team name":score,"team_name",score},game{"team name":score,"team_name",score}]
        for i in range(len(game_list)):
            dict = game_list[i]
            team1 = list(dict.keys())[0]
            team2 = list(dict.keys())[1]
            score1 = dict.get(team1)
            score2 = dict.get(team2)

            print(team1 + "|" + score1 + "|" + team2 + "|" + score2)

            self.g = Game_Info(team=team1,opp_team=team2,points=score1,opp_points=score2,date_start_time=timezone.now(),pub_date=timezone.now())
            self.g.save()
