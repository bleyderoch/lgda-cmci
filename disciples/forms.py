from django import forms
from django.forms import inlineformset_factory
from .models import Disciple, AmiProche, FamilleProche, AssiduiteCulte
from core.models import Assemblee


class DiscipleForm(forms.ModelForm):
    class Meta:
        model = Disciple
        exclude = ['matricule', 'date_creation', 'date_modification']
        widgets = {
            'assemblee': forms.Select(attrs={'class': 'form-select'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.RadioSelect(),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'indication': forms.TextInput(attrs={'class': 'form-control'}),
            'repere': forms.TextInput(attrs={'class': 'form-control'}),
            'rue': forms.TextInput(attrs={'class': 'form-control'}),
            'cite_villa': forms.TextInput(attrs={'class': 'form-control'}),
            'immeuble_appt': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu_habitation': forms.TextInput(attrs={'class': 'form-control'}),
            'faiseur_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'faiseur_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'mentor': forms.Select(attrs={'class': 'form-select'}),
            'mentor_qualite': forms.Select(attrs={'class': 'form-select'}),
            'date_bapteme': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'employeur': forms.TextInput(attrs={'class': 'form-control'}),
            'fonction': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau_etude': forms.Select(attrs={'class': 'form-select'}),
            'diplome': forms.TextInput(attrs={'class': 'form-control'}),
            'details_formation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and (user.is_gestionnaire or user.is_dirigeant) and user.assemblee:
            # Restreindre à l'assemblée de l'utilisateur
            self.fields['assemblee'].queryset = Assemblee.objects.filter(pk=user.assemblee.pk)
            self.fields['assemblee'].initial = user.assemblee
            self.fields['mentor'].queryset = Disciple.objects.filter(assemblee=user.assemblee)
        else:
            self.fields['mentor'].queryset = Disciple.objects.all()


class AmiProcheForm(forms.ModelForm):
    class Meta:
        model = AmiProche
        fields = ['nom_prenoms', 'telephone', 'lieu_habitation']
        widgets = {
            'nom_prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu_habitation': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FamilleProcheForm(forms.ModelForm):
    class Meta:
        model = FamilleProche
        fields = ['nom_famille', 'point_focal_nom', 'telephone', 'lieu_habitation']
        widgets = {
            'nom_famille': forms.TextInput(attrs={'class': 'form-control'}),
            'point_focal_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu_habitation': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AssiduiteCulteForm(forms.ModelForm):
    class Meta:
        model = AssiduiteCulte
        fields = ['semaine', 'date_dimanche', 'present']
        widgets = {
            'semaine': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_dimanche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


AmiProcheFormSet = inlineformset_factory(
    Disciple, AmiProche, form=AmiProcheForm, extra=1, max_num=10, validate_max=True, can_delete=True
)

FamilleProcheFormSet = inlineformset_factory(
    Disciple, FamilleProche, form=FamilleProcheForm, extra=1, max_num=5, validate_max=True, can_delete=True
)
