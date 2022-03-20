from django.contrib import admin
from django.urls import path

from .views import*


urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

]
