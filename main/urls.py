from django.urls import path

from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('index',views.index,name='index'),
	path('CurrentRanking',views.CurrentRanking,name='CurrentRanking')
]
