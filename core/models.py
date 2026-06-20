from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name='Nom du pays')
    code = models.CharField(max_length=5, blank=True, verbose_name='Code')

    class Meta:
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Ville(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom de la ville')
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='villes')

    class Meta:
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'
        ordering = ['nom']
        unique_together = ['nom', 'pays']

    def __str__(self):
        return f'{self.nom} ({self.pays})'


class Zone(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom de la zone')
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='zones')

    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
        ordering = ['nom']
        unique_together = ['nom', 'ville']

    def __str__(self):
        return f'{self.nom} – {self.ville}'


class SousCentre(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom du sous-centre')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='sous_centres')

    class Meta:
        verbose_name = 'Sous-centre'
        verbose_name_plural = 'Sous-centres'
        ordering = ['nom']
        unique_together = ['nom', 'zone']

    def __str__(self):
        return f'{self.nom} – {self.zone}'


class Assemblee(models.Model):
    """
    Assemblée locale LGDA-CMCI.
    Numéro auto-incrémenté : A, B, C, …, Z, AA, AB, …
    """
    QUALITE_CHOICES = [
        ('pasteur', 'Pasteur'),
        ('missionnaire', 'Missionnaire'),
        ('disciple', 'Disciple'),
    ]

    numero = models.CharField(max_length=10, unique=True, editable=False, verbose_name='N° Assemblée')
    nom = models.CharField(max_length=200, verbose_name="Nom de l'assemblée")
    sous_centre = models.ForeignKey(SousCentre, on_delete=models.PROTECT, related_name='assemblees')

    # Dirigeant
    dirigeant_nom = models.CharField(max_length=100, verbose_name='Nom du dirigeant')
    dirigeant_prenom = models.CharField(max_length=150, verbose_name='Prénom(s) du dirigeant')
    dirigeant_telephone = models.CharField(max_length=30, blank=True, verbose_name='Tél. dirigeant')
    dirigeant_qualite = models.CharField(max_length=15, choices=QUALITE_CHOICES, verbose_name='Qualité du dirigeant')

    # Gestionnaire
    gestionnaire_nom = models.CharField(max_length=100, verbose_name='Nom du gestionnaire')
    gestionnaire_prenom = models.CharField(max_length=150, verbose_name='Prénom(s) du gestionnaire')
    gestionnaire_telephone = models.CharField(max_length=30, blank=True, verbose_name='Tél. gestionnaire')
    gestionnaire_qualite = models.CharField(max_length=15, choices=QUALITE_CHOICES, verbose_name='Qualité du gestionnaire')

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Assemblée'
        verbose_name_plural = 'Assemblées'
        ordering = ['numero']

    def __str__(self):
        return f'[{self.numero}] {self.nom}'

    @property
    def pays(self):
        return self.sous_centre.zone.ville.pays

    @property
    def ville(self):
        return self.sous_centre.zone.ville

    @property
    def zone(self):
        return self.sous_centre.zone

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self._generer_numero()
        super().save(*args, **kwargs)

    @classmethod
    def _generer_numero(cls):
        """Génère le prochain numéro : A, B, …, Z, AA, AB, …"""
        import string
        lettres = string.ascii_uppercase
        existing = set(cls.objects.values_list('numero', flat=True))

        # Séquence : A-Z, puis AA-AZ, BA-BZ, …
        for longueur in range(1, 10):
            from itertools import product
            for combo in product(lettres, repeat=longueur):
                candidat = ''.join(combo)
                if candidat not in existing:
                    return candidat
        return 'ERR'
