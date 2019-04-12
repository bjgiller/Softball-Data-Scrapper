from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from main.models import Game_Info,Team_RPI
from main.dbgame import DB_Game_Interface
from main.webscraping import Web_Scraping
from.forms import TeamSearch
from main.math import RPI_Calculation
from main.dbRating import DB_RPI_Interface
from main.webtargets import Past

# Create your views here.
# Ross made a really cool comment
def TeamStatistics(request):
    if request.method == 'POST':
        searched_team = request.POST['team']
        # print(searched_team)

        db = DB_Game_Interface()

        latest_team_list = db.get_by_team(searched_team)
        template = loader.get_template('TeamStatistics.html')
        context = {
            'team_name' : searched_team,
            'latest_team_list': latest_team_list,
            'form' : TeamSearch()
        }
        return HttpResponse(template.render(context, request))
    else:
        db = DB_Game_Interface()
        #ws = Web_Scraping(10,4,2019)
        #print(ws.get_pre_game_list())

        ws = Past(1,2,2019,None,10,2,2019)
        '''
        for i in db.get_all_teams():
            RPI_Calculation(i)'''
        latest_team_list = db.get_by_team("Arkansas")
        template = loader.get_template('TeamStatistics.html')
        context = {
            'team_name' : "Arkansas",
            'latest_team_list': latest_team_list,
            'form' : TeamSearch()
        }
        return HttpResponse(template.render(context, request))

def CurrentRanking(request):
    latest_team_list = Team_RPI.objects.all().order_by('-rpi')
    template = loader.get_template('CurrentRanking.html')
    context = {
        'latest_team_list': latest_team_list,
    }
    return HttpResponse(template.render(context, request))
