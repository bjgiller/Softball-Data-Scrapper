import requests,datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from main.models import Game_Info

class Web_Team_Scraping:
    d1 = "https://www.ncaa.com/rankings/softball/d1/ncaa-womens-softball-rpi"
    d2 = "https://www.ncaa.com/rankings/softball/d2/regional-rankings"
    d3 = "https://www.ncaa.com/rankings/softball/d3/regional-rankings"

    all_teams = {}


    def __init__(self):
        self.page = requests.get(self.d1, headers=self.get_random_user_agent())
        print("got to url: "+self.page.url)
        print("got satus_code: "+ str(self.page.status_code))
        self.html = BeautifulSoup(self.page.text,'lxml')

        self.table = self.html.findAll("article",{"class":"rankings-content overflowable-table-region layout--content-left"})
        #print(self.table)
        #rows = self.table[0].findAll("tr",{"role":"row"})
        dict = {}
        for i in self.table[0].findAll("tr"):
            if (not i.findAll("th")):
                set = i.findAll("td")
                temp_team = temp_conf = ""
                for j in range(len(set)):
                    if (j==1):
                        temp_team = set[j].getText()
                    elif (j==2):
                        temp_conf = set[j].getText()
                dict.update({temp_team:temp_conf})
        self.all_teams.update({"d1":dict})

        #---------------------------------------------------

        self.page = requests.get(self.d2, headers=self.get_random_user_agent())
        print("got to url: "+self.page.url)
        print("got satus_code: "+ str(self.page.status_code))
        self.html = BeautifulSoup(self.page.text,'lxml')

        self.table = self.html.findAll("article",{"class":"rankings-content overflowable-table-region layout--content-left"})
        #print(self.table)
        #rows = self.table[0].findAll("tr",{"role":"row"})
        dict = {}
        cur_conf = ""
        for i in self.table[0].findAll("tr"):
            if (not i.findAll("th")):
                set = i.findAll("td")
                temp_team = ""
                if (set[0].getText() == "" and set[1].getText() != ""):
                    cur_conf = set[1].getText()
                elif (set[0].getText() != "" and set[1].getText() != ""):
                    for j in range(len(set)):
                        if (j == 1):
                            temp_team = set[j].getText()
                    dict.update({temp_team:cur_conf})
        self.all_teams.update({"d2":dict})

        #---------------------------------------------------

        self.page = requests.get(self.d3, headers=self.get_random_user_agent())
        print("got to url: "+self.page.url)
        print("got satus_code: "+ str(self.page.status_code))
        self.html = BeautifulSoup(self.page.text,'lxml')

        self.table = self.html.findAll("article",{"class":"rankings-content overflowable-table-region layout--content-left"})
        #print(self.table)
        #rows = self.table[0].findAll("tr",{"role":"row"})
        dict = {}
        cur_conf = ""
        for i in self.table[0].findAll("tr"):
            if (not i.findAll("th")):
                set = i.findAll("td")
                temp_team = ""
                if (set[1].getText() == "" and set[0].getText() != ""):
                    cur_conf = set[0].getText()
                elif (set[0].getText() != "" and set[1].getText() != ""):
                    for j in range(len(set)):
                        if (j == 1):
                            temp_team = set[j].getText()
                    dict.update({temp_team:cur_conf})
        self.all_teams.update({"d3":dict})

    def get_team_info(self):
        return self.all_teams

    def get_random_user_agent(self):
        ua = UserAgent()
        return {'User-agent': ua.random}
