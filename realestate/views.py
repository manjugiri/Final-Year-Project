from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Properti
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
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    if search:
        buy = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search))
        content = {'property':buy}
    else:
        properti = Properti.objects.filter(status = "Sale")
        content = {'property':properti}
    return render(request, 'buy.html', content)

def homeloan(request):
    return render(request, 'homeloan.html')

def rent(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    if search:
        rent = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search))
        content = {'rent':rent}
    else:
        rent_properti = Properti.objects.filter(status = "Rent")
        content = {'rent': rent_properti,}
    return render(request, 'rent.html',content)

def auction(request):
    return render(request, 'auction.html')

def agent(request):
    return render(request, 'agent.html')

def estate(request):
    return render(request, 'estate.html')

def bid(request):
    return render(request, 'bid.html')

def applyagent(request):
    return render(request, 'dashboard/apply_agent.html')

def dashboard(request):
    return render(request, 'dashboard/profile.html')

def propertydetails(request):
    return render(request, 'dashboard/property_details.html')

def addproperty(request):
    return render(request, 'dashboard/add_property.html')
