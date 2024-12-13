from django.urls import path
from . import views

urlpatterns = [
    path('save_index/', views.save_index, name='save_index'),
    path('search/', views.search_view, name='search'),
    #path('search/', views.search_view, name='search_view'),
]