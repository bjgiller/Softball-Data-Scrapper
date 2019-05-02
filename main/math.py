from . import dbgame
from . import dbRating
import datetime

class RPI_Calculation:
    def __init__(self,team):
        self.team = team
        self.dbRPIInt = dbRating.DB_RPI_Interface()
        self.dbGameInt = dbgame.DB_Game_Interface()

    def cal_rpi(self):
        #print(self.dbGameInt.get_by_date_start_time_team("UCLA", datetime.datetime(2019,3,9)))
        self.wp = self.win_percentage()
        print("WP: ",self.wp)
        self.owp = self.opp_win_percentage()
        print("OWP: ",self.owp)
        self.oowp = self.opp_opp_win_percentage()
        print("OOWP: ",self.oowp)
        self.bonus = 0
        self.dbRPIInt.create_single_rating_info(self.team,self.wp,self.owp,self.oowp,self.bonus,((self.wp * .25) + (self.owp * .5) + (self.oowp *.25)))

    def cal_bonus(self):
        top25 = self.dbRPIInt.get_top(25)
        #print(top25)
        top26to50 = self.dbRPIInt.get_top_by_range(26,50)
        top51to75 = self.dbRPIInt.get_top_by_range(51,75)

        bottom25 = self.dbRPIInt.get_bottom(25)
        bottom26to50 = self.dbRPIInt.get_bottom_by_range(26,50)
        bottom51to75 = self.dbRPIInt.get_bottom_by_range(51,75)

        b25 = b50 = b75 = p25 = p50 = p75 = 0.0

        dbquarry = self.dbGameInt.get_by_team(self.team)

        for i in dbquarry:
            temp = self.get_winner(i)
            if temp != None:
                winner = temp[0]
                loser = temp[1]
                #print(loser)
                if winner == self.team:
                    for j in top25:
                        if (loser == j.team_name):
                            b25 += 1
                    for j in top26to50:
                        if (loser == j.team_name):
                            b50 += 1
                    for j in top51to75:
                        if (loser == j.team_name):
                            b75 += 1

                if loser == self.team:
                    for j in bottom25:
                        if (winner == j.team_name):
                            p25 += 1
                    for j in bottom26to50:
                        if (winner == j.team_name):
                            p50 += 1
                    for j in bottom51to75:
                        if (winner == j.team_name):
                            p75 += 1

            temp = self.dbRPIInt.get_by_team(self.team)[0]
            #print("we upading with :",self.bonus)
            temp.bonus = (b25*0.0026)+(b50*0.002)+(b75*0.0013)
            temp.penalty = (p25*0.0026)+(p50*0.002)+(p75*0.0013)
            #temp.adj_rpi = (temp.rpi+temp.bonus+temp.penalty)
            temp.save()

            #print('b25: ',b25,'b50: ',b50,'b75: ',b75,'p25: ',p25,'p50: ',p50,'p75: ',p75)



    def get_winner(self,game):
        if (game.points < game.opp_points):
            return [game.opp_team,game.team]
        elif (game.points > game.opp_points):
            return [game.team,game.opp_team]
        else:
            return None

    def win_percentage(self):
          dbquarry = self.dbGameInt.get_by_team(self.team)
          totalGames = len(dbquarry)
          wins = 0
          for i in dbquarry:
              if (self.team == i.team):
                  if (i.points > i.opp_points):
                      wins = wins + 1
              elif (self.team == i.opp_team):
                  if (i.points < i.opp_points):
                      wins = wins + 1
          return (wins/totalGames)

    def win_percentage_mod(self,team,list):
          totalGames = len(list)
          if (totalGames != 0):
              wins = 0
              for i in list:
                  if (team == i.team):
                      if (i.points > i.opp_points):
                          wins = wins + 1
                  elif (team == i.opp_team):
                      if (i.points < i.opp_points):
                          wins = wins + 1
              return (wins/totalGames)
          else:
              return 0

    def opp_win_percentage(self):
          dbquarry = self.dbGameInt.get_by_team(self.team)
          totalGames = len(dbquarry)
          print("totalGames: ",totalGames)
          #Subtract one from totalGames every time we find that team
          #When calcuating the oppon
          total = 0
          for i in dbquarry:
              tempList = []
              if (self.team == i.team):
                  for j in self.dbGameInt.get_by_team(i.opp_team):
                      if (j.opp_team != self.team) and (j.team != self.team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.opp_team,tempList)
              elif (self.team == i.opp_team):
                  for j in self.dbGameInt.get_by_team(i.team):
                      if (j.opp_team != self.team) and (j.team != self.team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.team,tempList)
          return (total/totalGames)

    def opp_win_percentage_mod(self,team):

          dbquarry = self.dbGameInt.get_by_team(team)
          totalGames = len(dbquarry)
          #Subtract one from totalGames every time we find that team
          #When calcuating the oppon
          total = 0
          for i in dbquarry:
              tempList = []
              if (team == i.team):
                  for j in self.dbGameInt.get_by_team(i.opp_team):
                      if (j.opp_team != team) and (j.team != team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.opp_team,tempList)
              elif (team == i.opp_team):
                  for j in self.dbGameInt.get_by_team(i.team):
                      if (j.opp_team != team) and (j.team != team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.team,tempList)
          return (total/totalGames)

    def opp_opp_win_percentage(self):
        dbquarry = self.dbGameInt.get_by_team(self.team)
        totalGames = len(dbquarry)
        #Subtract one from totalGames every time we find that team
        #When calcuating the oppon
        total = 0
        for i in dbquarry:
            if (self.team == i.team):
                temp = self.opp_win_percentage_mod(i.opp_team)
                #print("temp: ",temp)
                total = total + temp
            elif (self.team == i.opp_team):
                temp = self.opp_win_percentage_mod(i.team)
                #print("temp: ",temp)
                total = total + temp
        print("total: ",total," | totalGames: ",totalGames)
        return (total/totalGames)
