import requests,datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from main.models import Game_Info, Completed

class Web_Scraping:
    def __init__(self,day,month,year,dtime=None):

        self.website_naming = {
            "NCAA":{
                "url":[
                    "https://www.ncaa.com/scoreboard/softball/d1/",
                    "/all-conf"
                ],
                'everythingelse':[
                    "gamePod gamePod-type-game status-final",
                    "gamePod-game-team-name",
                    "gamePod-game-team-score"
                ]
            },
        }

        '''
            "ESPN":{
                "url":[
                    "http://cdn.espn.com/college-sports/scoreboard?date="20190222&sport=current"
                ]
            }
        '''
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

        if len(str(self.day)) == 1:
            self.day = "0" + str(self.day)
        if len(str(self.month)) == 1:
            self.month = "0" + str(self.month)
        self.url = "https://www.ncaa.com/scoreboard/softball/d1/"+str(self.year)+"/"+str(self.month)+"/"+str(self.day)+"/all-conf"
        print("going to url: "+self.url)

        self.page = requests.get(self.url, headers=self.get_random_user_agent())
        # print("got to url: "+self.page.url)
        # print("got satus_code: "+ str(self.page.status_code))
        self.html = BeautifulSoup(self.page.text,'lxml')

        self.games = self.html.findAll("div",{"class":"gamePod gamePod-type-game status-final"})
        self.pre_games = self.html.findAll("div",{"class":"gamePod gamePod-type-game status-pre"})
        self.nostart = self.html.findAll("div",{"class":"gamePod gamePod-type-game status-nostart"})
        self.pre_games = self.pre_games + self.nostart
        #print(self.pre_games)


        self.game_list = []
        temp_list_check_false = []
        temp_list_check_true = []
        temp_list = []
        for i in self.games:
            check = False
            discript = i.findAll("span",{"class","game-round"})
            if (len(discript) > 0):
                check = True
            teams = i.findAll("span",{"class":"gamePod-game-team-name"})
            scores = i.findAll("span",{"class":"gamePod-game-team-score"})
            for j in range(len(teams)):
                teams[j] = teams[j].getText()
            for j in range(len(scores)):
                scores[j] = scores[j].getText()
            if len(teams) == len(scores):
                game_dict = {}
                for k in range(len(teams)):
                    game_dict.update({teams[k]:scores[k]})
                game_dict.update({"date_start_time":self.date_start_time})
            if (check == False):
                temp_list_check_false.append(game_dict)
            if (check == True):
                temp_list_check_true.append(game_dict)

        temp_list = temp_list_check_true.copy()

        for i in temp_list_check_false:
            if i not in temp_list_check_true:
                temp_list.append(i)
        #print(temp_list)
        self.game_list = temp_list
        self.game_list_incomplete = []
        #print(self.pre_games)
        for i in self.pre_games:
            teams = i.findAll("span",{"class":"gamePod-game-team-name"})
            scores = i.findAll("span",{"class":"gamePod-game-team-score"})
            for j in range(len(teams)):
                teams[j] = teams[j].getText()
                #print(teams[j])
            for j in range(len(scores)):
                scores[j] = scores[j].getText()
                #print(scores[j])
            if len(teams) == len(scores):
                game_dict = {}
                for k in range(len(teams)):
                    game_dict.update({teams[k]:scores[k]})
                game_dict.update({"date_start_time":self.date_start_time})
            self.game_list_incomplete.append(game_dict)

        #print(self.game_list_incomplete)

    def get_game_list(self):
        return self.game_list

    def get_pre_game_list(self):
        return self.game_list_incomplete

    def get_random_user_agent(self):
        ua = UserAgent()
        return {'User-agent': ua.random}
