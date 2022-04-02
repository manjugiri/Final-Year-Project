from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import addprop
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
    return render(request, 'homeloan.html')


def rent(request):
    # search = request.GET.get('search') if request.GET.get('search') != None else ''
    property_type = request.GET.get('property_type', None)
    sort_by = request.GET.get('sort_by', None)
    # if search:
    #     rent_properti = Properti.objects.filter(Q(ptype__icontains = search) | Q(status__icontains = search))
    # else:
    #     rent_properti = Properti.objects.filter(status = "Rent")
    rent_properti = Properti.objects.all()
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
    fm = addprop()
    if request.method == 'POST':
        fm = addprop(request.POST,request.FILES)
        if fm.is_valid():
            fm.save()
            return redirect('home')
        else:
            print('form is not valid')
    return render(request, 'dashboard/add_property.html', {'form':fm})
