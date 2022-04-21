from pyexpat.errors import messages
from tracemalloc import start
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.http import HttpResponse, HttpResponseRedirect
import re
from datetime import date
from django.db.models import Q
from .forms import addprop
from .forms import apply_agent
from .models import Properti, Bidders, Bank 
from django.contrib.auth.decorators import login_required
from .helpers import send_message
# Create your views here.
def index(request):
    date_now = date.today()
    auction_property = Properti.objects.filter(status = "Auction", bidding_end_time =date_now)
    property = []
    expired_property =[]
    for i in auction_property:
        expired_property.append(i)

    print(expired_property)
    for j in range(len(expired_property)):
        bidders = Bidders.objects.filter(properti = expired_property[j]).first()
        property = Properti.objects.get(title = expired_property[j])
        agent = property.added_by
        print(agent)
        send_message(bidders,agent)
        all_bidders = Bidders.objects.filter(properti = expired_property[j])
        all_bidders.delete()
        expired_property[j].delete()
    
    return render(request, 'index.html')



def user_logout(request):
    logout(request,request.user)
    return redirect('home')



def sellhome(request):
    return render(request, 'sellhome.html')

# def serach(request):
#     return render()

def buy(request):
    property_type = request.GET.get('property_type', None)
    sort_by = request.GET.get('sort_by', None)
    # if search:
    #     rent_properti = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search))
    # else:
    #     rent_properti = Properti.objects.filter(status = "Rent")
    buy_properti = Properti.objects.filter(status="Sale", is_approved=True)
    if property_type and not property_type=='All':
        buy_properti =buy_properti.filter(ptype = property_type)

    if sort_by and not sort_by == 'none_':
        if sort_by == 'lh':
            buy_properti = buy_properti.order_by('price')
        else:
            buy_properti = buy_properti.order_by('-price')

        # price__gte, price__lte
    content = {'property': buy_properti, 'sort_by':sort_by, 'property_type':property_type}

    return render(request, 'buy.html',content)


def homeloan(request):
    loan = Bank.objects.all()
    print('my',loan)
    return render(request, 'homeloan.html', {'homeloan': loan})


def rent(request):

    # search = request.GET.get('search') if request.GET.get('search') != None else ''
    # if search:
    #     rent = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search) | Q(title__icontains = search),status = "Rent" )
    #     content = {'rent':rent}
    # else:
    #     rent_properti = Properti.objects.filter(status = "Rent")
    #     content = {'rent': rent_properti,}
    # search = request.GET.get('search') if request.GET.get('search') != None else ''
    property_type = request.GET.get('property_type', None)
    sort_by = request.GET.get('sort_by', None)
    # if search:
    #     rent_properti = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search))
    # else:
    #     rent_properti = Properti.objects.filter(status = "Rent")
    rent_properti = Properti.objects.filter(status="Rent", is_approved=True)
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
    auction_property = Properti.objects.filter(status = 'Auction', is_approved = True)
    return render(request, 'auction.html', {"auction_property":auction_property})

from .models import ApplyAgent,AgentRating
def agent(request):
    if request.method == 'GET':
        agent = ApplyAgent.objects.filter(is_approved=True)
        return render(request, 'agent.html', {'agent':agent})
    if request.method == 'POST':
        value = request.POST.get('rating_value', None)
        agent = request.POST.get('agent', None)
        if value and agent and not value == 'none':
            if AgentRating.objects.filter(rating_by = request.user, agent_id=agent).exists():
                AgentRating.objects.filter(rating_by = request.user, agent_id=agent).update(value = value)
            else:
                AgentRating.objects.create(agent_id = agent, value=value, rating_by=request.user)
        return redirect('agent')

def estate(request):
    return render(request, 'estate.html')

@login_required(login_url = 'login')
def bid(request, pk):
    auction_property = get_object_or_404(Properti, id=pk)
    date_now = date.today()
    end_date = auction_property.bidding_end_time
    print(end_date)
    # a = f"{end_date.strftime('%Y')}-{end_date.strftime('%m')}-{end_date.strftime('%d')}"
    # print(a)
    if str(date_now) == str(end_date):
        expired = True
    else:
        expired = False
    user = request.user
    try:
        user_bid = Bidders.objects.get(properti = auction_property, user= user).bid_amount
    except:
        user_bid = 0
    if request.method == 'GET':
        
        return render(request, 'bid.html', {'auction_property':auction_property, 'status':'','user_bid':user_bid,'date':expired})

    if request.method == 'POST':
        bidamt = request.POST.get('BIdamt',None)
        if int(bidamt) < int(auction_property.price):
            error = f'Bid amount must be grater than {auction_property.price}'
            return render(request, 'bid.html', {'auction_property':auction_property,'status':error,'date':expired})
        
        if Bidders.objects.filter(user=request.user, properti=auction_property).exists():
            Bidders.objects.filter(user=request.user, properti=auction_property).update(bid_amount=bidamt)
        else:
            Bidders.objects.create(properti = auction_property, user= user, bid_amount=bidamt)
        try:
            user_bid = Bidders.objects.get(properti = auction_property, user= user).bid_amount
        except:
            user_bid = 0

        return render(request, 'bid.html', {'auction_property':auction_property,'status':'Bid success','user_bid':user_bid,'date':expired})


        
# def applyagent(request):
#     print("hello")
#     return render(request, 'dashboard/apply_agent.html')

def dashboard(request):
    return render(request, 'dashboard/profile.html')

def propertydetails(request):
    property = Properti.objects.filter(added_by = request.user)
    content = {'property':property}
    return render(request, 'dashboard/property_details.html',content)


from .permission import is_agent

@is_agent
@login_required(login_url='login')
def addproperty(request):
    fm = addprop()
    if request.method == 'POST':
        start_time = request.POST.get("bidding_start_time")
        end_time = request.POST.get("bidding_end_time")
        fm = addprop(request.POST,request.FILES)
        if fm.is_valid():
            form = fm.save(commit=False)
            form.added_by = request.user
            form.bidding_start_time = start_time
            form.bidding_end_time = end_time
            form.save()
            return redirect('propertydetails')
        else:
            print('form is not valid')
    return render(request, 'dashboard/add_property.html', {'form':fm})



@is_agent
@login_required(login_url='login')
def delete(request, pk):
    if request.method == 'POST':
        pi = Properti.objects.get(id=pk)
        pi.delete()
        return redirect('propertydetails')

@is_agent
@login_required(login_url='login')
def update_property(request, pk):
    updateprop = get_object_or_404(Properti, id=pk)
    fm = addprop(instance=updateprop)
    if request.method == 'POST':
        fm = addprop(request.POST, request.FILES, instance=updateprop)
        if fm.is_valid():
            fm.save()
            return redirect('propertydetails')
        else:
            print('form is not valid')
    return render(request, 'dashboard/update_property.html', {'form':fm, 'updateprop': updateprop})

@is_agent
@login_required(login_url='login')
def property_list(request):
    # if request.user.agent.is_approved:
    if request.method == 'GET':
        prop = Properti.objects.filter(added_by=request.user)
        print (prop)
    return render(request, 'dashboard/property_details.html', {'prop':prop})

@login_required(login_url='login')
def bidders_list(request,pk):
    if request.method == 'GET':
        prop = get_object_or_404(Properti, id=pk)
        bidders = Bidders.objects.filter(properti=prop)
        print (bidders)
    return render(request, 'bidders_list.html', {'bidders':bidders})


def serach_property(request):
    prop = Properti.objects.filter(is_approved=True)
    status = request.GET.get('status', None)
    types = request.GET.get('type', None)
    address = request.GET.get('address', None)
    # prop = prop.filter(status =status, ptype = types)
    # print(prop)
    if status and not status=='none':
        prop = prop.filter(status=status)
        print(prop)
    if types and not types == 'none':
        prop = prop.filter(ptype=types)
        print(prop)
    if address:
        prop = prop.filter(address=address)
        print(prop)
    return render(request, 'search.html', {'prop':prop})




# applyagent
def applyagent(request):
    pass
    if request.method == 'POST':
        try:
            af = apply_agent(request.POST, request.FILES)
            if af.is_valid():
                form = af.save(commit = False)
                form.user=request.user
                form.save()
                return redirect('home')
            else:
                print('form is not valid')
        except:
            print("form is")
            af = apply_agent()
            print(af)
            return render(request, 'dashboard/apply_agent.html', {'form':af})
    else:
        print("form is")
        af = apply_agent()
        print(af)
    return render(request, 'dashboard/apply_agent.html', {'form':af})

