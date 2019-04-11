from . import dbgame
from . import dbRating

class RPI_Calculation:
    def __init__(self,team):
        self.team = team
        self.test1 = dbgame.DB_Game_Interface()
        self.test2 = dbRating.DB_RPI_Interface()
        self.wp = self.win_percentage()
        #print("WP: ",self.wp)
        self.owp = self.opp_win_percentage()
        print("OWP: ",self.owp)
        self.oowp = self.opp_opp_win_percentage()
        print("OOWP: ",self.oowp)
        self.test2.create_single_rating_info(self.team,((self.wp * .25) + (self.owp * .5) + (self.oowp *.25)))

    def win_percentage(self):
          totalGames = len(self.test1.get_by_team(self.team))
          wins = 0
          for i in self.test1.get_by_team(self.team):
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
          totalGames = len(self.test1.get_by_team(self.team))
          #Subtract one from totalGames every time we find that team
          #When calcuating the oppon
          total = 0
          for i in self.test1.get_by_team(self.team):
              tempList = []
              if (self.team == i.team):
                  for j in self.test1.get_by_team(i.opp_team):
                      if (j.opp_team != self.team) and (j.team != self.team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.opp_team,tempList)
              elif (self.team == i.opp_team):
                  for j in self.test1.get_by_team(i.team):
                      if (j.opp_team != self.team) and (j.team != self.team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.team,tempList)
          return (total/totalGames)

    def opp_win_percentage_mod(self,team):
          totalGames = len(self.test1.get_by_team(team))
          #Subtract one from totalGames every time we find that team
          #When calcuating the oppon
          total = 0
          for i in self.test1.get_by_team(team):
              tempList = []
              if (team == i.team):
                  for j in self.test1.get_by_team(i.opp_team):
                      if (j.opp_team != team) and (j.team != team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.opp_team,tempList)
              elif (team == i.opp_team):
                  for j in self.test1.get_by_team(i.team):
                      if (j.opp_team != team) and (j.team != team):
                          tempList.append(j)
                  total = total + self.win_percentage_mod(i.team,tempList)
          return (total/totalGames)

    def opp_opp_win_percentage(self):
        totalGames = len(self.test1.get_by_team(self.team))
        #Subtract one from totalGames every time we find that team
        #When calcuating the oppon
        total = 0
        for i in self.test1.get_by_team(self.team):
            if (self.team == i.team):
                total = total + self.opp_win_percentage_mod(i.opp_team)
            elif (self.team == i.opp_team):
                total = total + self.opp_win_percentage_mod(i.team)
        return (total/totalGames)
