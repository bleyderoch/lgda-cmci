from django import forms
from django.core.exceptions import ValidationError
from .models import Evangeliste, PlanningEvangelisation
from core.models import Assemblee


class EvangelisteForm(forms.ModelForm):
    class Meta:
        model = Evangeliste
        fields = ['nom', 'prenoms', 'telephone', 'sous_centre', 'faiseur_nom', 'faiseur_contact', 'qualite']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'sous_centre': forms.Select(attrs={'class': 'form-select'}),
            'faiseur_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'faiseur_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'qualite': forms.Select(attrs={'class': 'form-select'}),
        }


class PlanningForm(forms.ModelForm):
    class Meta:
        model = PlanningEvangelisation
        fields = [
            'assemblee', 'semaine', 'jour', 'heure',
            'type_ame', 'ame_nom', 'ame_telephone', 'lieu_rdv',
            'statut_rdv', 'statut_engagement', 'evangeliste',
        ]
        widgets = {
            'assemblee': forms.Select(attrs={'class': 'form-select'}),
            'semaine': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 53}),
            'jour': forms.Select(attrs={'class': 'form-select'}),
            'heure': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'type_ame': forms.Select(attrs={'class': 'form-select'}),
            'ame_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'ame_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu_rdv': forms.TextInput(attrs={'class': 'form-control'}),
            'statut_rdv': forms.Select(attrs={'class': 'form-select'}),
            'statut_engagement': forms.Select(attrs={'class': 'form-select'}),
            'evangeliste': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and (user.is_gestionnaire or user.is_dirigeant) and user.assemblee:
            self.fields['assemblee'].queryset = Assemblee.objects.filter(pk=user.assemblee.pk)
            self.fields['assemblee'].initial = user.assemblee
            # Évangélistes du même sous-centre
            self.fields['evangeliste'].queryset = Evangeliste.objects.filter(
                sous_centre=user.assemblee.sous_centre
            )

    def clean(self):
        cleaned = super().clean()
        evangeliste = cleaned.get('evangeliste')
        semaine = cleaned.get('semaine')
        jour = cleaned.get('jour')
        heure = cleaned.get('heure')

        if evangeliste and semaine and jour and heure:
            qs = PlanningEvangelisation.objects.filter(
                evangeliste=evangeliste, semaine=semaine, jour=jour, heure=heure
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    f"⚠️ {evangeliste} a déjà un RDV le {dict(PlanningEvangelisation.JOUR_CHOICES).get(jour)} "
                    f"à {heure} (semaine {semaine}). Veuillez changer la date ou l'évangéliste."
                )
        return cleaned
