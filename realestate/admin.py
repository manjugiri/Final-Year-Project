from django.contrib import admin
from .models import  ApplyAgent, Properti, Bank,AgentRating,Bidders

admin.site.register(Properti)
admin.site.register(Bank)
admin.site.register(Bidders)
admin.site.register([ApplyAgent,AgentRating])
