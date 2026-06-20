from django.urls import path
from . import views

app_name = 'evangelisation'

urlpatterns = [
    path('evangelistes/', views.evangeliste_list, name='evangeliste_list'),
    path('evangelistes/ajouter/', views.evangeliste_create, name='evangeliste_create'),
    path('evangelistes/<int:pk>/modifier/', views.evangeliste_edit, name='evangeliste_edit'),

    path('planning/', views.planning_list, name='planning_list'),
    path('planning/creer/', views.planning_create, name='planning_create'),
    path('planning/<int:pk>/modifier/', views.planning_edit, name='planning_edit'),
]
