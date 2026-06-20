from django import forms
from .models import Pays, Ville, Zone, SousCentre, Assemblee


class PaysForm(forms.ModelForm):
    class Meta:
        model = Pays
        fields = ['nom', 'code']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = ['nom', 'pays']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.Select(attrs={'class': 'form-select'}),
        }


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['nom', 'ville']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.Select(attrs={'class': 'form-select'}),
        }


class SousCentreForm(forms.ModelForm):
    class Meta:
        model = SousCentre
        fields = ['nom', 'zone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'zone': forms.Select(attrs={'class': 'form-select'}),
        }


class AssembleeForm(forms.ModelForm):
    class Meta:
        model = Assemblee
        fields = [
            'nom', 'sous_centre',
            'dirigeant_nom', 'dirigeant_prenom', 'dirigeant_telephone', 'dirigeant_qualite',
            'gestionnaire_nom', 'gestionnaire_prenom', 'gestionnaire_telephone', 'gestionnaire_qualite',
        ]
        labels = {
            'nom': "Nom de l'assemblée",
            'sous_centre': 'Sous-centre',
            'dirigeant_nom': 'Nom',
            'dirigeant_prenom': 'Prénom(s)',
            'dirigeant_telephone': 'Tél.',
            'dirigeant_qualite': 'Qualité',
            'gestionnaire_nom': 'Nom',
            'gestionnaire_prenom': 'Prénom(s)',
            'gestionnaire_telephone': 'Tél.',
            'gestionnaire_qualite': 'Qualité',
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'sous_centre': forms.Select(attrs={'class': 'form-select'}),
            'dirigeant_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'dirigeant_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'dirigeant_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'dirigeant_qualite': forms.Select(attrs={'class': 'form-select'}),
            'gestionnaire_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'gestionnaire_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'gestionnaire_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'gestionnaire_qualite': forms.Select(attrs={'class': 'form-select'}),
        }
