from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.http import HttpResponse
from django.db.models import Q
from .forms import addprop
from .models import Properti
# Create your views here.
def index(request):
    return render(request, 'index.html')


def user_logout(request):
    logout(request,request.user)
    return redirect('home')

def sellhome(request):
    return render(request, 'sellhome.html')

def buy(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    if search:
        buy = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search)| Q(title__icontains = search),status = "Sale")
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
        rent = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search) | Q(title__icontains = search),status = "Rent" )
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
    property = Properti.objects.filter(added_by = request.user)
    content = {'property':property}
    return render(request, 'dashboard/property_details.html',content)

def addproperty(request):
    fm = addprop()
    if request.method == 'POST':
        fm = addprop(request.POST,request.FILES)
        if fm.is_valid():
            fm.save()
            return redirect('propertydetails')
        else:
            print('form is not valid')
    return render(request, 'dashboard/add_property.html', {'form':fm})

def update_property(request,pk):
    property = Properti.objects.get(id = pk)
    fm = addprop(instance=property)
    if request.method == "POST":
        fm = addprop(request.POST,instance=property)
        if fm.is_valid():
            fm.save()
            return redirect('propertydetails')
    
    return render(request,'dashboard/add_property.html',{'form':fm})

def remove_property(request,pk):
    property = Properti.objects.get(id = pk)
    property.delete()
    return redirect('propertydetails')