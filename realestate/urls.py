
from turtle import update
from django.contrib import admin
from django.urls import path

from .views import addproperty, index, sellhome, buy, agent, auction, rent, homeloan, bid, applyagent, dashboard, propertydetails, addproperty,update_property,delete,serach_property,property_detail,bidders_list


# admin.site.site_header = "REMS"
# admin.site.site_title = "welcome to REMS"
# admin.site.index_title = "Welcome to the portal"
urlpatterns = [
    path('', index, name='home'),
    path('sellhome', sellhome),
    path('buy', buy, name = 'buy'),
    path('agent', agent, name = 'agent'),
    path('applyagent', applyagent, name = 'applyagent'),
    path('auction', auction),
    path('rent', rent),
    path('homeloan', homeloan),
    path('bid/<int:pk>/', bid, name = 'bid'),
    path('dashboard', dashboard),
    path('propertydetails', propertydetails,name = "propertydetails"),
    path('addproperty', addproperty),
    path('updateproperty/<int:pk>/',update_property,name = "update"),
    path('removeproperty/<int:pk>/',delete,name = "remove"),
    path('search-prop/', serach_property, name ='search-prop'),

    path('addproperty/', addproperty, name='addproperty'),

    path('property-detail/<int:pk>/', property_detail, name = 'property_detail'),

    path('bidder-list/<int:pk>/', bidders_list, name = 'bidder-list')
]
