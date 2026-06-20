"""
Commande Django pour créer le Super Administrateur N°1 par défaut.

Usage : python manage.py init_super_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

DEFAULT_USERNAME = 'LGDA-CMCI'
DEFAULT_PASSWORD = 'Administrateur'


class Command(BaseCommand):
    help = 'Crée le Super Administrateur N°1 par défaut (login: LGDA-CMCI / mdp: Administrateur)'

    def handle(self, *args, **options):
        if User.objects.filter(username=DEFAULT_USERNAME).exists():
            self.stdout.write(self.style.WARNING(
                f"L'utilisateur '{DEFAULT_USERNAME}' existe déjà."
            ))
            return

        count = User.objects.filter(role=User.SUPER_ADMIN).count()
        if count >= 5:
            self.stdout.write(self.style.ERROR('Maximum 5 Super Administrateurs atteint.'))
            return

        user = User.objects.create_superuser(
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
            role=User.SUPER_ADMIN,
            must_change_password=True,
            first_name='Super',
            last_name='Administrateur',
        )
        self.stdout.write(self.style.SUCCESS(
            f"✅ Super Administrateur créé.\n"
            f"   Login    : {DEFAULT_USERNAME}\n"
            f"   Mot de passe : {DEFAULT_PASSWORD}\n"
            f"   ⚠️  Changez le mot de passe à la première connexion !"
        ))
