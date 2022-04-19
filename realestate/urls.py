
from turtle import update
from django.contrib import admin
from django.urls import path

from .views import addproperty, index, sellhome, buy, agent, auction, rent, homeloan, bid, applyagent, dashboard, propertydetails, addproperty,update_property,remove_property

# admin.site.site_header = "REMS"
# admin.site.site_title = "welcome to REMS"
# admin.site.index_title = "Welcome to the portal"
urlpatterns = [
    path('', index, name='home'),
    path('sellhome', sellhome),
    path('buy', buy),
    path('agent', agent),
    path('auction', auction),
    path('rent', rent),
    path('homeloan', homeloan),
    path('bid', bid),
    path('applyagent', applyagent),
    path('dashboard', dashboard),
    path('propertydetails', propertydetails,name = "propertydetails"),
    path('addproperty', addproperty),
    path('updateproperty/<int:pk>/',update_property,name = "update"),
    path('removeproperty/<int:pk>/',remove_property,name = "remove"),

]
