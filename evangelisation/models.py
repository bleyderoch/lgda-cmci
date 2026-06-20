from django.db import models
from core.models import SousCentre, Assemblee


class Evangeliste(models.Model):
    QUALITE_CHOICES = [
        ('pasteur', 'Pasteur'),
        ('missionnaire', 'Missionnaire'),
        ('disciple', 'Disciple'),
    ]

    nom = models.CharField(max_length=100, verbose_name='Nom')
    prenoms = models.CharField(max_length=200, verbose_name='Prénom(s)')
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Tél.')
    sous_centre = models.ForeignKey(
        SousCentre, on_delete=models.PROTECT, related_name='evangelistes', verbose_name='Sous-centre'
    )
    faiseur_nom = models.CharField(max_length=200, blank=True, verbose_name='Nom du faiseur de disciple')
    faiseur_contact = models.CharField(max_length=50, blank=True, verbose_name='Contact du faiseur de disciple')
    qualite = models.CharField(max_length=15, choices=QUALITE_CHOICES, verbose_name='Qualité')

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Évangéliste'
        verbose_name_plural = 'Évangélistes'
        ordering = ['nom', 'prenoms']

    def __str__(self):
        return f'{self.nom} {self.prenoms}'


class PlanningEvangelisation(models.Model):
    JOUR_CHOICES = [
        ('L', 'Lundi'), ('M', 'Mardi'), ('Me', 'Mercredi'),
        ('J', 'Jeudi'), ('V', 'Vendredi'), ('S', 'Samedi'), ('D', 'Dimanche'),
    ]
    TYPE_AME_CHOICES = [('ami', 'Ami'), ('famille', 'Famille')]
    STATUT_CHOICES = [('ok', 'OK'), ('nok', 'NOK'), ('en_attente', 'En attente')]

    assemblee = models.ForeignKey(
        Assemblee, on_delete=models.CASCADE, related_name='plannings', verbose_name='Assemblée'
    )
    semaine = models.PositiveSmallIntegerField(verbose_name='N° semaine')
    jour = models.CharField(max_length=3, choices=JOUR_CHOICES, verbose_name='Jour')
    heure = models.TimeField(verbose_name='Heure')

    # Âme à rencontrer
    type_ame = models.CharField(max_length=10, choices=TYPE_AME_CHOICES, verbose_name='Type')
    ame_nom = models.CharField(max_length=200, verbose_name="Nom de l'âme")
    ame_telephone = models.CharField(max_length=30, blank=True, verbose_name='Tél.')
    lieu_rdv = models.CharField(max_length=300, verbose_name='Lieu de RDV')

    # Résultats
    statut_rdv = models.CharField(
        max_length=10, choices=STATUT_CHOICES, default='en_attente', verbose_name='Statut RDV'
    )
    statut_engagement = models.CharField(
        max_length=10, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut engagement"
    )

    # Évangéliste affecté (même sous-centre que l'assemblée)
    evangeliste = models.ForeignKey(
        Evangeliste, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='plannings', verbose_name='Évangéliste affecté'
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Planning d'évangélisation"
        verbose_name_plural = "Plannings d'évangélisation"
        ordering = ['semaine', 'jour', 'heure']

    def __str__(self):
        return f'S{self.semaine} {self.get_jour_display()} {self.heure} – {self.ame_nom}'

    def conflit_evangeliste(self):
        """Retourne True si l'évangéliste a déjà un RDV ce jour à cette heure."""
        if not self.evangeliste:
            return False
        return PlanningEvangelisation.objects.filter(
            evangeliste=self.evangeliste,
            semaine=self.semaine,
            jour=self.jour,
            heure=self.heure,
        ).exclude(pk=self.pk).exists()
