from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def super_admin_required(view_func):
    """Réserve la vue aux Super Administrateurs."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_super_admin:
            messages.error(request, "Accès réservé aux Super Administrateurs.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def write_required(view_func):
    """Réserve la vue aux utilisateurs ayant le droit d'écriture (Super Admin + Gestionnaire)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.can_write:
            messages.error(request, "Vous n'avez pas les droits pour effectuer cette action.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
