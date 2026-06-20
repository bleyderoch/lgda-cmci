from django.contrib import admin
from .models import Evangeliste, PlanningEvangelisation


@admin.register(Evangeliste)
class EvangelisteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenoms', 'telephone', 'sous_centre', 'qualite']
    list_filter = ['qualite', 'sous_centre__zone__ville__pays']
    search_fields = ['nom', 'prenoms']


@admin.register(PlanningEvangelisation)
class PlanningAdmin(admin.ModelAdmin):
    list_display = ['assemblee', 'semaine', 'jour', 'heure', 'ame_nom', 'evangeliste', 'statut_rdv', 'statut_engagement']
    list_filter = ['assemblee', 'statut_rdv', 'statut_engagement', 'semaine']
    search_fields = ['ame_nom']
