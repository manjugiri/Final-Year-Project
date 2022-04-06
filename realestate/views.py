from pyexpat.errors import messages
import re
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .forms import addprop
from .models import Properti, Bidders, Bank 
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'account/login.html')

    return render(request, 'account/login.html')

def signup(request):
    return render(request, 'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def sellhome(request):
    return render(request, 'sellhome.html')

# def serach(request):
#     return render()

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
    loan = Bank.objects.all()
    print('my',loan)
    return render(request, 'homeloan.html', {'homeloan': loan})


def rent(request):
    # search = request.GET.get('search') if request.GET.get('search') != None else ''
    property_type = request.GET.get('property_type', None)
    sort_by = request.GET.get('sort_by', None)
    # if search:
    #     rent_properti = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search))
    # else:
    #     rent_properti = Properti.objects.filter(status = "Rent")
    rent_properti = Properti.objects.filter(status="Rent")
    if property_type and not property_type=='All':
        rent_properti =rent_properti.filter(ptype = property_type)

    if sort_by and not sort_by == 'none_':
        if sort_by == 'lh':
            rent_properti = rent_properti.order_by('price')
        else:
            rent_properti = rent_properti.order_by('-price')

        # price__gte, price__lte
    content = {'rent': rent_properti, 'sort_by':sort_by, 'property_type':property_type}

    return render(request, 'rent.html',content)


from django.shortcuts import get_object_or_404
def property_detail(request, pk):
    property_ = get_object_or_404(Properti, id=pk)
    return render(request, 'property_detail.html',{'property':property_})

def auction(request):
    auction_property = Properti.objects.filter(status = 'Auction')
    return render(request, 'auction.html', {"auction_property":auction_property})

def agent(request):
    return render(request, 'agent.html')

def estate(request):
    return render(request, 'estate.html')

@login_required(login_url = '/login/')
def bid(request, pk):
    auction_property = get_object_or_404(Properti, id=pk)
    user = request.user
    try:
        user_bid = Bidders.objects.get(properti = auction_property, user= user).bid_amount
    except:
        user_bid = 0
    if request.method == 'GET':
        
        return render(request, 'bid.html', {'auction_property':auction_property, 'status':'','user_bid':user_bid})

    if request.method == 'POST':
        bidamt = request.POST.get('BIdamt',None)
        if int(bidamt) < int(auction_property.price):
            error = f'Bid amount must be grater than {auction_property.price}'
            return render(request, 'bid.html', {'auction_property':auction_property,'status':error})
        
        if Bidders.objects.filter(user=request.user, properti=auction_property).exists():
            Bidders.objects.filter(user=request.user, properti=auction_property).update(bid_amount=bidamt)
        else:
            Bidders.objects.create(properti = auction_property, user= user, bid_amount=bidamt)
        try:
            user_bid = Bidders.objects.get(properti = auction_property, user= user).bid_amount
        except:
            user_bid = 0

        return render(request, 'bid.html', {'auction_property':auction_property,'status':'Bid success','user_bid':user_bid})

def applyagent(request):
    return render(request, 'dashboard/apply_agent.html')

def dashboard(request):
    return render(request, 'dashboard/profile.html')

def propertydetails(request):
    return render(request, 'dashboard/property_details.html')

def addproperty(request):
    fm = addprop()
    if request.method == 'POST':
        fm = addprop(request.POST,request.FILES)
        if fm.is_valid():
            fm.save()
            return redirect('home')
        else:
            print('form is not valid')
    return render(request, 'dashboard/add_property.html', {'form':fm})

def delete(request, id):
    if request.method == 'POST':
        pi = Properti.objects.get(pk=id)
        pi.delete()
    return redirect('property_list')

def update_property(request, pk):
    updateprop = get_object_or_404(Properti, id=pk)
    fm = addprop(instance=updateprop)
    if request.method == 'POST':
        fm = addprop(request.POST,request.FILES, instance=updateprop)
        if fm.is_valid():
            fm.save()
            return redirect('property_list')
        else:
            print('form is not valid')
    return render(request, 'dashboard/update_property.html', {'form':fm, 'updateprop': updateprop})

@login_required
def property_list(request):
    if request.method == 'GET':
        prop = Properti.objects.filter(added_by=request.user)
        print (prop)
    return render(request, 'dashboard/property_details.html', {'prop':prop})

@login_required
def bidders_list(request,pk):
    if request.method == 'GET':
        prop = get_object_or_404(Properti, id=pk)
        bidders = Bidders.objects.filter(properti=prop)
        print (bidders)
    return render(request, 'bidders_list.html', {'bidders':bidders})




