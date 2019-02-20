from django.urls import path

from . import views

urlpatterns = [
	path('',views.CurrentRanking,name='CurrentRanking'),
	path('index',views.index,name='index'),
	path('CurrentRanking',views.CurrentRanking,name='CurrentRanking')
]
