import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from main.models import Game_Info

class Web_Scraping:
    def __init__(self,day,month,year):

        self.day = day
        self.month = month
        self.year = year

        if len(str(self.day)) == 1:
            self.day = "0" + str(self.day)
        if len(str(self.month)) == 1:
            self.month = "0" + str(self.month)

        self.url = "https://www.ncaa.com/scoreboard/softball/d1/"+str(self.year)+"/"+str(self.month)+"/"+str(self.day)+"/all-conf"
        print("going to url: "+self.url)

        self.page = requests.get(self.url, headers=self.get_random_user_agent())
        self.html = BeautifulSoup(self.page.text,'lxml')
        self.games = self.html.findAll("div",{"class":"gamePod gamePod-type-game status-final"})

        self.game_list = []
        for i in self.games:
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
            self.game_list.append(game_dict)

    def get_game_list(self):
        return self.game_list

    def get_random_user_agent(self):
        ua = UserAgent()
        return {'User-agent': ua.random}
