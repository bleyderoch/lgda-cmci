from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Pays
    path('pays/', views.pays_list, name='pays_list'),
    path('pays/ajouter/', views.pays_create, name='pays_create'),
    path('pays/<int:pk>/modifier/', views.pays_edit, name='pays_edit'),

    # Ville
    path('villes/', views.ville_list, name='ville_list'),
    path('villes/ajouter/', views.ville_create, name='ville_create'),
    path('villes/<int:pk>/modifier/', views.ville_edit, name='ville_edit'),

    # Zone
    path('zones/', views.zone_list, name='zone_list'),
    path('zones/ajouter/', views.zone_create, name='zone_create'),
    path('zones/<int:pk>/modifier/', views.zone_edit, name='zone_edit'),

    # Sous-centre
    path('sous-centres/', views.sous_centre_list, name='sous_centre_list'),
    path('sous-centres/ajouter/', views.sous_centre_create, name='sous_centre_create'),
    path('sous-centres/<int:pk>/modifier/', views.sous_centre_edit, name='sous_centre_edit'),

    # Assemblée
    path('assemblees/', views.assemblee_list, name='assemblee_list'),
    path('assemblees/creer/', views.assemblee_create, name='assemblee_create'),
    path('assemblees/<int:pk>/', views.assemblee_detail, name='assemblee_detail'),
    path('assemblees/<int:pk>/modifier/', views.assemblee_edit, name='assemblee_edit'),
]
