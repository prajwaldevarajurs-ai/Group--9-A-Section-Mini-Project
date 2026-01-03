from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('searchhistory/', views.searchhistory, name='searchhistory'),
    path('about/', views.about),
    path('contact/', views.contact),
]




