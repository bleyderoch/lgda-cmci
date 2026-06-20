from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, ChangePasswordForm, ProfilForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next', 'dashboard'))
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def changer_mot_de_passe(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.must_change_password = False
            user.save(update_fields=['must_change_password'])
            update_session_auth_hash(request, user)
            messages.success(request, 'Mot de passe modifié avec succès.')
            return redirect('dashboard')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/changer_mot_de_passe.html', {
        'form': form,
        'force': request.user.must_change_password,
    })


@login_required
def profil(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour.')
            return redirect('accounts:profil')
    else:
        form = ProfilForm(instance=request.user)
    return render(request, 'accounts/profil.html', {'form': form})
