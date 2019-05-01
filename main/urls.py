from django.urls import path
from background_task import tasks
import main.tasks

from . import views

urlpatterns = [
	path('',views.CurrentRanking,name='CurrentRanking'),
	path('TeamStatistics',views.TeamStatistics,name='TeamStatistics'),
	path('CurrentRanking',views.CurrentRanking,name='CurrentRanking')
]
