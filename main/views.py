from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from main.models import Game_Info,Team_RPI
from main.dbgame import DB_Game_Interface
from.forms import TeamSearch

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
        latest_team_list = db.get_by_team("Arkansas")
        template = loader.get_template('TeamStatistics.html')
        context = {
            'team_name' : "Arkansas",
            'latest_team_list': latest_team_list,
            'form' : TeamSearch()
        }
        return HttpResponse(template.render(context, request))

def CurrentRanking(request):
    latest_team_list = Game_Info.objects.order_by('-pub_date')[:5]
    template = loader.get_template('CurrentRanking.html')
    context = {
        'latest_team_list': latest_team_list,
    }
    return HttpResponse(template.render(context, request))