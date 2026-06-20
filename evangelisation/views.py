from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Evangeliste, PlanningEvangelisation
from .forms import EvangelisteForm, PlanningForm
from core.decorators import write_required, super_admin_required


@login_required
def evangeliste_list(request):
    evangelistes = Evangeliste.objects.select_related('sous_centre__zone__ville__pays')
    return render(request, 'evangelisation/evangeliste_list.html', {'evangelistes': evangelistes})


@login_required
@super_admin_required
def evangeliste_create(request):
    if request.method == 'POST':
        form = EvangelisteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Évangéliste ajouté.')
            return redirect('evangelisation:evangeliste_list')
    else:
        form = EvangelisteForm()
    return render(request, 'evangelisation/evangeliste_form.html', {'form': form, 'titre': 'Ajouter un évangéliste'})


@login_required
@super_admin_required
def evangeliste_edit(request, pk):
    ev = get_object_or_404(Evangeliste, pk=pk)
    if request.method == 'POST':
        form = EvangelisteForm(request.POST, instance=ev)
        if form.is_valid():
            form.save()
            messages.success(request, 'Évangéliste modifié.')
            return redirect('evangelisation:evangeliste_list')
    else:
        form = EvangelisteForm(instance=ev)
    return render(request, 'evangelisation/evangeliste_form.html', {'form': form, 'titre': 'Modifier l\'évangéliste'})


@login_required
def planning_list(request):
    user = request.user
    qs = PlanningEvangelisation.objects.select_related('assemblee', 'evangeliste')
    if user.is_gestionnaire or user.is_dirigeant:
        if user.assemblee:
            qs = qs.filter(assemblee=user.assemblee)
        else:
            qs = qs.none()
    return render(request, 'evangelisation/planning_list.html', {'plannings': qs})


@login_required
@write_required
def planning_create(request):
    if request.method == 'POST':
        form = PlanningForm(request.POST, user=request.user)
        if form.is_valid():
            planning = form.save()
            messages.success(request, 'RDV d\'évangélisation créé.')
            return redirect('evangelisation:planning_list')
    else:
        form = PlanningForm(user=request.user)
    return render(request, 'evangelisation/planning_form.html', {'form': form, 'titre': 'Créer un RDV'})


@login_required
@write_required
def planning_edit(request, pk):
    planning = get_object_or_404(PlanningEvangelisation, pk=pk)
    user = request.user
    if (user.is_gestionnaire or user.is_dirigeant) and user.assemblee != planning.assemblee:
        messages.error(request, "Accès refusé.")
        return redirect('evangelisation:planning_list')
    if request.method == 'POST':
        form = PlanningForm(request.POST, instance=planning, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'RDV mis à jour.')
            return redirect('evangelisation:planning_list')
    else:
        form = PlanningForm(instance=planning, user=user)
    return render(request, 'evangelisation/planning_form.html', {
        'form': form,
        'titre': 'Modifier le RDV',
        'planning': planning,
    })
