from django.db import models
from django.core.validators import MaxValueValidator
from core.models import Assemblee


class Disciple(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    QUALITE_CHOICES = [
        ('pasteur', 'Pasteur'),
        ('missionnaire', 'Missionnaire'),
        ('disciple', 'Disciple'),
    ]
    NIVEAU_CHOICES = [
        ('analphabete', 'Analphabète'),
        ('cm2', 'Niveau CM2'),
        ('bac', 'Niveau BAC'),
        ('superieur', 'Niveau Supérieur'),
    ]

    # Identité
    matricule = models.CharField(max_length=15, unique=True, editable=False, verbose_name='Matricule')
    assemblee = models.ForeignKey(Assemblee, on_delete=models.PROTECT, related_name='disciples')
    nom = models.CharField(max_length=100, verbose_name='Nom')
    prenoms = models.CharField(max_length=200, verbose_name='Prénom(s)')
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Tél.')

    # Adresse
    indication = models.CharField(max_length=200, blank=True, verbose_name='Indication')
    repere = models.CharField(max_length=200, blank=True, verbose_name='Repère')
    rue = models.CharField(max_length=200, blank=True, verbose_name='Rue')
    cite_villa = models.CharField(max_length=200, blank=True, verbose_name='Cité / N° Villa')
    immeuble_appt = models.CharField(max_length=200, blank=True, verbose_name='Immeuble / N° Appt')
    lieu_habitation = models.CharField(max_length=300, blank=True, verbose_name="Lieu d'habitation")

    # Faiseur de disciple
    faiseur_nom = models.CharField(max_length=200, blank=True, verbose_name='Nom du faiseur de disciple')
    faiseur_contact = models.CharField(max_length=50, blank=True, verbose_name='Contact du faiseur de disciple')

    # Mentor
    mentor = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='disciples_mentores', verbose_name='Mentor'
    )
    mentor_qualite = models.CharField(
        max_length=15, choices=QUALITE_CHOICES, blank=True, verbose_name='Qualité du mentor'
    )

    # Statut spirituel
    repentance = models.BooleanField(default=False, verbose_name='Repentance')
    bapteme = models.BooleanField(default=False, verbose_name='Baptême')
    date_bapteme = models.DateField(null=True, blank=True, verbose_name='Date du baptême')
    brisement_liens = models.BooleanField(default=False, verbose_name='Brisement de liens')
    formation_disciple = models.BooleanField(default=False, verbose_name='Formation du disciple')

    # Situation professionnelle
    travaille = models.BooleanField(default=False, verbose_name='Travaille')
    employeur = models.CharField(max_length=200, blank=True, verbose_name='Employeur')
    fonction = models.CharField(max_length=200, blank=True, verbose_name='Fonction actuelle')
    niveau_etude = models.CharField(
        max_length=20, choices=NIVEAU_CHOICES, blank=True, verbose_name="Niveau d'étude"
    )
    cpe = models.BooleanField(default=False, verbose_name='CPE')
    certificat = models.BooleanField(default=False, verbose_name='Certificat')
    diplome = models.CharField(max_length=200, blank=True, verbose_name='Diplôme / Certificat')
    details_formation = models.TextField(blank=True, verbose_name='Détails formation')

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Disciple'
        verbose_name_plural = 'Disciples'
        ordering = ['matricule']

    def __str__(self):
        return f'{self.matricule} – {self.nom} {self.prenoms}'

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = self._generer_matricule()
        super().save(*args, **kwargs)

    def _generer_matricule(self):
        """Génère A001, A002, … pour l'assemblée donnée."""
        prefix = self.assemblee.numero
        existing = Disciple.objects.filter(
            assemblee=self.assemblee
        ).values_list('matricule', flat=True)
        nums = []
        for m in existing:
            try:
                nums.append(int(m[len(prefix):]))
            except (ValueError, IndexError):
                pass
        next_num = max(nums, default=0) + 1
        return f'{prefix}{next_num:03d}'


class AmiProche(models.Model):
    """10 amis proches max par disciple."""
    disciple = models.ForeignKey(Disciple, on_delete=models.CASCADE, related_name='amis_proches')
    nom_prenoms = models.CharField(max_length=200, verbose_name='Nom et prénom(s)')
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Tél.')
    lieu_habitation = models.CharField(max_length=300, blank=True, verbose_name="Lieu d'habitation")

    class Meta:
        verbose_name = 'Ami proche'
        verbose_name_plural = 'Amis proches'

    def __str__(self):
        return self.nom_prenoms


class FamilleProche(models.Model):
    """5 familles proches max par disciple."""
    disciple = models.ForeignKey(Disciple, on_delete=models.CASCADE, related_name='familles_proches')
    nom_famille = models.CharField(max_length=100, verbose_name='Nom de la famille')
    point_focal_nom = models.CharField(max_length=200, verbose_name='Nom et prénom(s) du point focal')
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Tél.')
    lieu_habitation = models.CharField(max_length=300, blank=True, verbose_name="Lieu d'habitation")

    class Meta:
        verbose_name = 'Famille proche'
        verbose_name_plural = 'Familles proches'

    def __str__(self):
        return f'Famille {self.nom_famille}'


class AssiduiteCulte(models.Model):
    """Enregistrement de présence à l'adoration du dimanche."""
    disciple = models.ForeignKey(Disciple, on_delete=models.CASCADE, related_name='assiduites')
    semaine = models.PositiveSmallIntegerField(verbose_name='N° semaine')
    date_dimanche = models.DateField(verbose_name='Dimanche le')
    present = models.BooleanField(default=False, verbose_name='Présent')

    class Meta:
        verbose_name = "Assiduité culte"
        verbose_name_plural = "Assiduités culte"
        unique_together = ['disciple', 'date_dimanche']
        ordering = ['date_dimanche']

    def __str__(self):
        statut = 'Présent' if self.present else 'Absent'
        return f'{self.disciple} – {self.date_dimanche} – {statut}'
