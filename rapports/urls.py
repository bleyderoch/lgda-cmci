from django.urls import path
from . import views

app_name = 'rapports'

urlpatterns = [
    path('assemblees/', views.liste_assemblees, name='liste_assemblees'),
    path('disciples/', views.liste_disciples, name='liste_disciples'),
    path('evangelistes/', views.liste_evangelistes, name='liste_evangelistes'),
    path('evangelisation/', views.rapport_evangelisation, name='rapport_evangelisation'),
    path('assiduite/', views.rapport_assiduite, name='rapport_assiduite'),
]
