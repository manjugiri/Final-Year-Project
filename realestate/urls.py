
from django.contrib import admin
from django.urls import path

from .views import index, login, signup, sellhome, buy, agent, auction, rent, homeloan, bid, applyagent, dashboard

# admin.site.site_header = "REMS"
# admin.site.site_title = "welcome to REMS"
# admin.site.index_title = "Welcome to the portal"
urlpatterns = [
    path('', index, name='home'),
    path('login', login),
    path('signup', signup),
    path('sellhome', sellhome),
    path('buy', buy),
    path('agent', agent),
    path('auction', auction),
    path('rent', rent),
    path('homeloan', homeloan),
    path('bid', bid),
    path('applyagent', applyagent),
    path('dashboard', dashboard),

]
