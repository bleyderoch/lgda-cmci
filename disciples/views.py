from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Disciple, AssiduiteCulte
from .forms import DiscipleForm, AmiProcheFormSet, FamilleProcheFormSet, AssiduiteCulteForm
from core.decorators import write_required


def _qs_pour_user(user):
    """Queryset disciples filtré selon le rôle."""
    qs = Disciple.objects.select_related('assemblee', 'mentor')
    if user.is_gestionnaire or user.is_dirigeant:
        if user.assemblee:
            return qs.filter(assemblee=user.assemblee)
        return qs.none()
    return qs  # Super Admin et Évangéliste voient tout


@login_required
def disciple_list(request):
    disciples = _qs_pour_user(request.user)
    # Filtres optionnels
    q = request.GET.get('q', '')
    if q:
        disciples = disciples.filter(nom__icontains=q) | disciples.filter(prenoms__icontains=q) | disciples.filter(matricule__icontains=q)
    return render(request, 'disciples/disciple_list.html', {
        'disciples': disciples,
        'q': q,
    })


@login_required
def disciple_detail(request, pk):
    disciple = get_object_or_404(Disciple, pk=pk)
    user = request.user
    if (user.is_gestionnaire or user.is_dirigeant) and user.assemblee != disciple.assemblee:
        messages.error(request, "Accès refusé.")
        return redirect('disciples:disciple_list')
    statut_list = [
        ('Repentance', disciple.repentance),
        ('Baptême', disciple.bapteme),
        ('Brisement de liens', disciple.brisement_liens),
        ('Formation du disciple', disciple.formation_disciple),
    ]
    return render(request, 'disciples/disciple_detail.html', {
        'disciple': disciple,
        'amis': disciple.amis_proches.all(),
        'familles': disciple.familles_proches.all(),
        'assiduites': disciple.assiduites.order_by('-date_dimanche')[:12],
        'statut_list': statut_list,
    })


@login_required
@write_required
def disciple_create(request):
    if request.method == 'POST':
        form = DiscipleForm(request.POST, user=request.user)
        ami_fs = AmiProcheFormSet(request.POST, prefix='amis')
        famille_fs = FamilleProcheFormSet(request.POST, prefix='familles')
        if form.is_valid() and ami_fs.is_valid() and famille_fs.is_valid():
            disciple = form.save()
            ami_fs.instance = disciple
            ami_fs.save()
            famille_fs.instance = disciple
            famille_fs.save()
            messages.success(request, f'Disciple {disciple.matricule} créé.')
            return redirect('disciples:disciple_detail', pk=disciple.pk)
    else:
        form = DiscipleForm(user=request.user)
        ami_fs = AmiProcheFormSet(prefix='amis')
        famille_fs = FamilleProcheFormSet(prefix='familles')
    return render(request, 'disciples/disciple_form.html', {
        'form': form,
        'ami_formset': ami_fs,
        'famille_formset': famille_fs,
        'titre': 'Ajouter un disciple',
    })


@login_required
@write_required
def disciple_edit(request, pk):
    disciple = get_object_or_404(Disciple, pk=pk)
    user = request.user
    if (user.is_gestionnaire or user.is_dirigeant) and user.assemblee != disciple.assemblee:
        messages.error(request, "Accès refusé.")
        return redirect('disciples:disciple_list')
    if request.method == 'POST':
        form = DiscipleForm(request.POST, instance=disciple, user=user)
        ami_fs = AmiProcheFormSet(request.POST, instance=disciple, prefix='amis')
        famille_fs = FamilleProcheFormSet(request.POST, instance=disciple, prefix='familles')
        if form.is_valid() and ami_fs.is_valid() and famille_fs.is_valid():
            form.save()
            ami_fs.save()
            famille_fs.save()
            messages.success(request, 'Disciple mis à jour.')
            return redirect('disciples:disciple_detail', pk=disciple.pk)
    else:
        form = DiscipleForm(instance=disciple, user=user)
        ami_fs = AmiProcheFormSet(instance=disciple, prefix='amis')
        famille_fs = FamilleProcheFormSet(instance=disciple, prefix='familles')
    return render(request, 'disciples/disciple_form.html', {
        'form': form,
        'ami_formset': ami_fs,
        'famille_formset': famille_fs,
        'titre': f'Modifier {disciple}',
        'disciple': disciple,
    })


@login_required
@write_required
def assiduite_create(request, disciple_pk):
    disciple = get_object_or_404(Disciple, pk=disciple_pk)
    user = request.user
    if (user.is_gestionnaire or user.is_dirigeant) and user.assemblee != disciple.assemblee:
        messages.error(request, "Accès refusé.")
        return redirect('disciples:disciple_list')
    if request.method == 'POST':
        form = AssiduiteCulteForm(request.POST)
        if form.is_valid():
            ass = form.save(commit=False)
            ass.disciple = disciple
            ass.save()
            messages.success(request, 'Présence enregistrée.')
            return redirect('disciples:disciple_detail', pk=disciple.pk)
    else:
        form = AssiduiteCulteForm()
    return render(request, 'disciples/assiduite_form.html', {
        'form': form,
        'disciple': disciple,
    })
