from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from main.models import Game_Info,Team_RPI

# Create your views here.
# Ross made a really cool comment
def index(request):
    latest_team_list = Game_Info.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
        'latest_team_list': latest_team_list,
    }
    return HttpResponse(template.render(context, request))
