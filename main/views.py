from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Ross made a really cool comment
def index(request):
    return HttpResponse("Hello World")
