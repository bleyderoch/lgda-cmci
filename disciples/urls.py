from django.urls import path
from . import views

app_name = 'disciples'

urlpatterns = [
    path('', views.disciple_list, name='disciple_list'),
    path('ajouter/', views.disciple_create, name='disciple_create'),
    path('<int:pk>/', views.disciple_detail, name='disciple_detail'),
    path('<int:pk>/modifier/', views.disciple_edit, name='disciple_edit'),
    path('<int:disciple_pk>/assiduite/', views.assiduite_create, name='assiduite_create'),
]
