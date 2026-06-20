from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Pays, Ville, Zone, SousCentre, Assemblee
from .forms import PaysForm, VilleForm, ZoneForm, SousCentreForm, AssembleeForm
from .decorators import super_admin_required, write_required
from disciples.models import Disciple
from evangelisation.models import Evangeliste, PlanningEvangelisation


@login_required
def dashboard(request):
    user = request.user
    ctx = {'user': user}

    if user.is_super_admin:
        ctx['nb_assemblees'] = Assemblee.objects.count()
        ctx['nb_disciples'] = Disciple.objects.count()
        ctx['nb_evangelistes'] = Evangeliste.objects.count()
        ctx['nb_pays'] = Pays.objects.count()
    elif user.is_gestionnaire or user.is_dirigeant:
        if user.assemblee:
            ctx['assemblee'] = user.assemblee
            ctx['nb_disciples'] = Disciple.objects.filter(assemblee=user.assemblee).count()
    elif user.is_evangeliste:
        ctx['nb_assemblees'] = Assemblee.objects.count()
        ctx['nb_disciples'] = Disciple.objects.count()

    return render(request, 'core/dashboard.html', ctx)


# ─── PAYS ───────────────────────────────────────────────────────────────────

@login_required
@super_admin_required
def pays_list(request):
    pays = Pays.objects.all()
    return render(request, 'core/pays_list.html', {'pays_list': pays})


@login_required
@super_admin_required
def pays_create(request):
    if request.method == 'POST':
        form = PaysForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pays ajouté.')
            return redirect('core:pays_list')
    else:
        form = PaysForm()
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Ajouter un pays'})


@login_required
@super_admin_required
def pays_edit(request, pk):
    pays = get_object_or_404(Pays, pk=pk)
    if request.method == 'POST':
        form = PaysForm(request.POST, instance=pays)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pays modifié.')
            return redirect('core:pays_list')
    else:
        form = PaysForm(instance=pays)
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Modifier le pays'})


# ─── VILLE ──────────────────────────────────────────────────────────────────

@login_required
@super_admin_required
def ville_list(request):
    return render(request, 'core/ville_list.html', {'villes': Ville.objects.select_related('pays').all()})


@login_required
@super_admin_required
def ville_create(request):
    if request.method == 'POST':
        form = VilleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ville ajoutée.')
            return redirect('core:ville_list')
    else:
        form = VilleForm()
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Ajouter une ville'})


@login_required
@super_admin_required
def ville_edit(request, pk):
    ville = get_object_or_404(Ville, pk=pk)
    if request.method == 'POST':
        form = VilleForm(request.POST, instance=ville)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ville modifiée.')
            return redirect('core:ville_list')
    else:
        form = VilleForm(instance=ville)
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Modifier la ville'})


# ─── ZONE ───────────────────────────────────────────────────────────────────

@login_required
@super_admin_required
def zone_list(request):
    return render(request, 'core/zone_list.html', {'zones': Zone.objects.select_related('ville__pays').all()})


@login_required
@super_admin_required
def zone_create(request):
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zone ajoutée.')
            return redirect('core:zone_list')
    else:
        form = ZoneForm()
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Ajouter une zone'})


@login_required
@super_admin_required
def zone_edit(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    if request.method == 'POST':
        form = ZoneForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zone modifiée.')
            return redirect('core:zone_list')
    else:
        form = ZoneForm(instance=zone)
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Modifier la zone'})


# ─── SOUS-CENTRE ────────────────────────────────────────────────────────────

@login_required
@super_admin_required
def sous_centre_list(request):
    return render(request, 'core/sous_centre_list.html', {
        'sous_centres': SousCentre.objects.select_related('zone__ville__pays').all()
    })


@login_required
@super_admin_required
def sous_centre_create(request):
    if request.method == 'POST':
        form = SousCentreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sous-centre ajouté.')
            return redirect('core:sous_centre_list')
    else:
        form = SousCentreForm()
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Ajouter un sous-centre'})


@login_required
@super_admin_required
def sous_centre_edit(request, pk):
    sc = get_object_or_404(SousCentre, pk=pk)
    if request.method == 'POST':
        form = SousCentreForm(request.POST, instance=sc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sous-centre modifié.')
            return redirect('core:sous_centre_list')
    else:
        form = SousCentreForm(instance=sc)
    return render(request, 'core/form_generic.html', {'form': form, 'titre': 'Modifier le sous-centre'})


# ─── ASSEMBLÉE ──────────────────────────────────────────────────────────────

@login_required
def assemblee_list(request):
    user = request.user
    qs = Assemblee.objects.select_related('sous_centre__zone__ville__pays')
    if user.is_gestionnaire or user.is_dirigeant:
        if user.assemblee:
            qs = qs.filter(pk=user.assemblee.pk)
    return render(request, 'core/assemblee_list.html', {'assemblees': qs})


@login_required
@super_admin_required
def assemblee_create(request):
    if request.method == 'POST':
        form = AssembleeForm(request.POST)
        if form.is_valid():
            assemblee = form.save()
            messages.success(request, f'Assemblée {assemblee.numero} créée.')
            return redirect('core:assemblee_list')
    else:
        form = AssembleeForm()
    return render(request, 'core/assemblee_form.html', {'form': form, 'titre': 'Créer une assemblée'})


@login_required
def assemblee_detail(request, pk):
    assemblee = get_object_or_404(Assemblee, pk=pk)
    user = request.user
    # Sécurité : Dirigeant/Gestionnaire ne voient que leur assemblée
    if (user.is_gestionnaire or user.is_dirigeant) and user.assemblee != assemblee:
        messages.error(request, "Accès refusé.")
        return redirect('core:assemblee_list')
    disciples = Disciple.objects.filter(assemblee=assemblee)
    return render(request, 'core/assemblee_detail.html', {
        'assemblee': assemblee,
        'disciples': disciples,
    })


@login_required
@super_admin_required
def assemblee_edit(request, pk):
    assemblee = get_object_or_404(Assemblee, pk=pk)
    if request.method == 'POST':
        form = AssembleeForm(request.POST, instance=assemblee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assemblée modifiée.')
            return redirect('core:assemblee_list')
    else:
        form = AssembleeForm(instance=assemblee)
    return render(request, 'core/assemblee_form.html', {'form': form, 'titre': 'Modifier l\'assemblée'})
