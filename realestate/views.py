from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def sellhome(request):
    return render(request, 'sellhome.html')

def buy(request):
    return render(request, 'buy.html')
def homeloan(request):
    return render(request, 'homeloan.html')

def rent(request):
    return render(request, 'rent.html')

def auction(request):
    return render(request, 'auction.html')

def agent(request):
    return render(request, 'agent.html')

def estate(request):
    return render(request, 'estate.html')

def bid(request):
    return render(request, 'bid.html')

def applyagent(request):
    return render(request, 'applyagent.html')

def dashboard(request):
    return render(request, 'dashboard/index.html')