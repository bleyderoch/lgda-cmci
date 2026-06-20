from django.contrib import admin
from .models import Pays, Ville, Zone, SousCentre, Assemblee


@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code']
    search_fields = ['nom']


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays']
    list_filter = ['pays']
    search_fields = ['nom']


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville']
    list_filter = ['ville__pays']
    search_fields = ['nom']


@admin.register(SousCentre)
class SousCentreAdmin(admin.ModelAdmin):
    list_display = ['nom', 'zone']
    search_fields = ['nom']


@admin.register(Assemblee)
class AssembleeAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nom', 'sous_centre', 'dirigeant_nom', 'gestionnaire_nom']
    list_filter = ['sous_centre__zone__ville__pays']
    search_fields = ['nom', 'numero']
    readonly_fields = ['numero']
