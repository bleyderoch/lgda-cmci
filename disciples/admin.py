from django.contrib import admin
from .models import Disciple, AmiProche, FamilleProche, AssiduiteCulte


class AmiProcheInline(admin.TabularInline):
    model = AmiProche
    extra = 0
    max_num = 10


class FamilleProcheInline(admin.TabularInline):
    model = FamilleProche
    extra = 0
    max_num = 5


class AssiduiteCulteInline(admin.TabularInline):
    model = AssiduiteCulte
    extra = 0
    ordering = ['-date_dimanche']


@admin.register(Disciple)
class DiscipleAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'nom', 'prenoms', 'sexe', 'assemblee', 'telephone']
    list_filter = ['assemblee', 'sexe', 'repentance', 'bapteme']
    search_fields = ['nom', 'prenoms', 'matricule', 'telephone']
    readonly_fields = ['matricule']
    inlines = [AmiProcheInline, FamilleProcheInline, AssiduiteCulteInline]
    fieldsets = (
        ('Identité', {'fields': ('matricule', 'assemblee', 'nom', 'prenoms', 'sexe', 'telephone')}),
        ('Adresse', {'fields': ('lieu_habitation', 'indication', 'repere', 'rue', 'cite_villa', 'immeuble_appt')}),
        ('Faiseur de disciple & Mentor', {'fields': ('faiseur_nom', 'faiseur_contact', 'mentor', 'mentor_qualite')}),
        ('Statut spirituel', {'fields': ('repentance', 'bapteme', 'date_bapteme', 'brisement_liens', 'formation_disciple')}),
        ('Situation professionnelle', {'fields': ('travaille', 'employeur', 'fonction', 'niveau_etude', 'cpe', 'certificat', 'diplome', 'details_formation')}),
    )
