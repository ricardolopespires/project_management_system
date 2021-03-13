from django.urls import path
from . import views



app_name = 'documentary'



urlpatterns = [


    path('manager/', views.documentary_manager, name = 'manager'),
    path('search/', views.documentary_search, name = 'search'),
    path('<imdb_id>/details/', views.documentary_details, name = 'details'),

    
]