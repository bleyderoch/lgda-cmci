from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé LGDA-CMCI.
    4 rôles : Super Administrateur, Dirigeant, Gestionnaire, Évangéliste.
    """
    SUPER_ADMIN = 'super_admin'
    DIRIGEANT = 'dirigeant'
    GESTIONNAIRE = 'gestionnaire'
    EVANGELISTE = 'evangeliste'

    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Administrateur'),
        (DIRIGEANT, 'Dirigeant'),
        (GESTIONNAIRE, 'Gestionnaire'),
        (EVANGELISTE, 'Évangéliste'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=GESTIONNAIRE)
    # L'assemblée liée (pour Dirigeant et Gestionnaire)
    assemblee = models.ForeignKey(
        'core.Assemblee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='utilisateurs',
        verbose_name='Assemblée'
    )
    must_change_password = models.BooleanField(
        default=True,
        verbose_name='Doit changer le mot de passe'
    )
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Téléphone')

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_super_admin(self):
        return self.role == self.SUPER_ADMIN

    @property
    def is_dirigeant(self):
        return self.role == self.DIRIGEANT

    @property
    def is_gestionnaire(self):
        return self.role == self.GESTIONNAIRE

    @property
    def is_evangeliste(self):
        return self.role == self.EVANGELISTE

    @property
    def can_write(self):
        """Peut créer/modifier des données (hors lecture seule)."""
        return self.role in [self.SUPER_ADMIN, self.GESTIONNAIRE]
