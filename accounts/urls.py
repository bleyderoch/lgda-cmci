from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('changer-mot-de-passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    path('profil/', views.profil, name='profil'),
]
