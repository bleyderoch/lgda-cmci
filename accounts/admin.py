from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'role', 'assemblee', 'must_change_password', 'is_active']
    list_filter = ['role', 'is_active', 'must_change_password']
    fieldsets = UserAdmin.fieldsets + (
        ('Informations LGDA-CMCI', {
            'fields': ('role', 'assemblee', 'telephone', 'must_change_password')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations LGDA-CMCI', {
            'fields': ('role', 'assemblee', 'telephone')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Limiter à 5 Super Administrateurs
        if obj.role == Utilisateur.SUPER_ADMIN:
            count = Utilisateur.objects.filter(role=Utilisateur.SUPER_ADMIN).exclude(pk=obj.pk).count()
            if count >= 5:
                from django.contrib import messages
                self.message_user(request, "Maximum 5 Super Administrateurs autorisés.", level='ERROR')
                return
        super().save_model(request, obj, form, change)
