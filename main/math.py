from . import dbgame
from . import dbRating

class RPI_Calculation:
    def __init__(self,team):
        self.team = team
        self.test1 = dbgame.DB_Game_Interface()
        self.test2 = dbRating.DB_RPI_Interface()
        self.wp = self.win_percentage()
        print("WP: ",self.wp)
        self.owp = self.opp_win_percentage()
        print("OWP: ",self.owp)
        self.oowp = self.opp_opp_win_percentage()
        print("OOWP: ",self.oowp)
        self.bonus = 0
        self.test2.create_single_rating_info(self.team,self.wp,self.owp,self.oowp,self.bonus,((self.wp * .25) + (self.owp * .5) + (self.oowp *.25)))
        self.cal_bonus()
        temp = self.test2.get_by_team(self.team)[0]
        print("we upading with :",self.bonus)
        temp.bonus = self.bonus
        temp.save()


    def cal_bonus(self):
        top25 = self.test2.get_top(25)
        intop25 = False
        for i in top25:
            if (i.team_name == self.team):
                intop25 = True
                break
        if (not intop25):
            dbquarry = self.test1.get_by_team(self.team)
            for i in dbquarry:
                winner = self.get_winner(i)
                for j in top25:
                    if (j.team_name == winner):
                        print('we adding!!!')
                        self.bonus = self.bonus + 1
        #------------------------------------------------
        bottom75 = self.test2.get_bottom(75)
        inbottom75 = False
        for i in bottom75:
            if (i.team_name == self.team):
                inbottom75 = True
                break
        if (not inbottom75):
            dbquarry = self.test1.get_by_team(self.team)
            for i in dbquarry:
                winner = self.get_winner(i)
                for j in top25:
                    if (j.team_name == winner):
                        self.bonus = self.bonus - 1
                        print('we subtracting!!!')

    def get_winner(self,game):
        if (game.points < game.opp_points):
            return game.opp_team
        elif (game.points > game.opp_points):
            return game.team
        else:
            return None

    def win_percentage(self):
          dbquarry = self.test1.get_by_team(self.team)
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
          dbquarry = self.test1.get_by_team(self.team)
          totalGames = len(dbquarry)
          #Subtract one from totalGames every time we find that team
          #When calcuating the oppon
          total = 0
          for i in dbquarry:
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

          dbquarry = self.test1.get_by_team(self.team)
          totalGames = len(dbquarry)
          #Subtract one from totalGames every time we find that team
          #When calcuating the oppon
          total = 0
          for i in dbquarry:
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
        dbquarry = self.test1.get_by_team(self.team)
        totalGames = len(dbquarry)
        #Subtract one from totalGames every time we find that team
        #When calcuating the oppon
        total = 0
        for i in dbquarry:
            if (self.team == i.team):
                total = total + self.opp_win_percentage_mod(i.opp_team)
            elif (self.team == i.opp_team):
                total = total + self.opp_win_percentage_mod(i.team)
        return (total/totalGames)
