#this class puts some of dbgame and webscraping together in a much more friendly way to uses
import datetime
from main.dbgame import DB_Game_Interface
from main.webscraping import Web_Scraping

class Past:
    def __init__(self,day,month,year,dtime=None):
        self.db = DB_Game_Interface()

        if ((day >= 1 and day <= 31) and (month >= 1 and month <= 12) and (year >= 2010)):
            self.day = day
            self.month = month
            self.year = year
            self.date_start_time = datetime.date(self.year,self.month,self.day)
        else:
            if (dtime != None):
                self.day = dtime.day
                self.month = dtime.month
                self.year = dtime.year
                self.date_start_time = datetime.date(self.year,self.month,self.day)
            else:
                print("Not valid Date time")

        '''ws = Web_Scraping(23,3,2019)

        exList = ws.get_game_list()

        db.create_games_from_list(exList)'''

        date = None

        while True:
            if (datetime.datetime.now().date() == date):
                break
            try:
                date = datetime.date(self.year,self.month,self.day)

                ws = Web_Scraping(self.day,self.month,self.year)
                exList = ws.get_game_list()
                self.db.create_games_from_list(exList)

                self.day = self.day + 1
            except ValueError:
                self.month = self.month + 1
                self.day = 1
