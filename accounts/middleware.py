from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    """
    Redirige l'utilisateur vers la page de changement de mot de passe
    si must_change_password est True.
    """
    EXEMPT_URLS = [
        '/accounts/login/',
        '/accounts/logout/',
        '/accounts/changer-mot-de-passe/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if (
                getattr(request.user, 'must_change_password', False)
                and request.path not in self.EXEMPT_URLS
                and not request.path.startswith('/admin/')
            ):
                return redirect(reverse('accounts:changer_mot_de_passe'))
        return self.get_response(request)
