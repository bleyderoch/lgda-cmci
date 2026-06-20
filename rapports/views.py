from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q, Count
from datetime import date

from core.models import Assemblee, Pays, Ville, Zone, SousCentre
from disciples.models import Disciple, AssiduiteCulte
from evangelisation.models import Evangeliste, PlanningEvangelisation
from .exports import export_excel, export_pdf, export_word


def _get_semaines_du_mois(annee, mois):
    """Retourne les numéros de semaine ISO couvrant le mois donné."""
    from isoweek import Week
    semaines = set()
    for jour in range(1, 32):
        try:
            d = date(annee, mois, jour)
            semaines.add(d.isocalendar()[1])
        except ValueError:
            break
    return semaines


def _get_semaines_de_lannee_partielle(annee):
    """Retourne les numéros de semaine ISO des mois achevés dans l'année."""
    aujourd_hui = date.today()
    mois_actuels = aujourd_hui.month if aujourd_hui.year == annee else 12
    semaines = set()
    for mois in range(1, mois_actuels):
        semaines.update(_get_semaines_du_mois(annee, mois))
    return semaines


# ─── LISTE ASSEMBLÉES ────────────────────────────────────────────────────────

@login_required
def liste_assemblees(request):
    qs = Assemblee.objects.select_related('sous_centre__zone__ville__pays')
    # Filtres périmètre
    pays_id = request.GET.get('pays')
    ville_id = request.GET.get('ville')
    zone_id = request.GET.get('zone')
    sc_id = request.GET.get('sous_centre')
    if pays_id:
        qs = qs.filter(sous_centre__zone__ville__pays_id=pays_id)
    if ville_id:
        qs = qs.filter(sous_centre__zone__ville_id=ville_id)
    if zone_id:
        qs = qs.filter(sous_centre__zone_id=zone_id)
    if sc_id:
        qs = qs.filter(sous_centre_id=sc_id)

    fmt = request.GET.get('format', '')
    if fmt in ('pdf', 'xlsx', 'docx'):
        entetes = ['N° Assemblée', 'Nom', 'Pays', 'Ville', 'Zone', 'Sous-centre', 'Dirigeant', 'Gestionnaire']
        lignes = [[
            a.numero, a.nom,
            str(a.pays), str(a.ville), str(a.zone), str(a.sous_centre),
            f'{a.dirigeant_nom} {a.dirigeant_prenom}',
            f'{a.gestionnaire_nom} {a.gestionnaire_prenom}',
        ] for a in qs]
        titre = 'Liste des Assemblées – LGDA-CMCI'
        if fmt == 'xlsx':
            return export_excel(titre, entetes, lignes, 'liste_assemblees.xlsx')
        elif fmt == 'pdf':
            return export_pdf(titre, entetes, lignes, 'liste_assemblees.pdf')
        else:
            return export_word(titre, entetes, lignes, 'liste_assemblees.docx')

    ctx = {
        'assemblees': qs,
        'pays_list': Pays.objects.all(),
        'villes': Ville.objects.all(),
        'zones': Zone.objects.all(),
        'sous_centres': SousCentre.objects.all(),
        'selected': {'pays': pays_id, 'ville': ville_id, 'zone': zone_id, 'sous_centre': sc_id},
    }
    return render(request, 'rapports/liste_assemblees.html', ctx)


# ─── LISTE DISCIPLES ─────────────────────────────────────────────────────────

@login_required
def liste_disciples(request):
    user = request.user
    qs = Disciple.objects.select_related('assemblee__sous_centre__zone__ville__pays')
    if user.is_gestionnaire or user.is_dirigeant:
        if user.assemblee:
            qs = qs.filter(assemblee=user.assemblee)
        else:
            qs = qs.none()

    pays_id = request.GET.get('pays')
    ville_id = request.GET.get('ville')
    zone_id = request.GET.get('zone')
    sc_id = request.GET.get('sous_centre')
    assemblee_id = request.GET.get('assemblee')
    if pays_id:
        qs = qs.filter(assemblee__sous_centre__zone__ville__pays_id=pays_id)
    if ville_id:
        qs = qs.filter(assemblee__sous_centre__zone__ville_id=ville_id)
    if zone_id:
        qs = qs.filter(assemblee__sous_centre__zone_id=zone_id)
    if sc_id:
        qs = qs.filter(assemblee__sous_centre_id=sc_id)
    if assemblee_id:
        qs = qs.filter(assemblee_id=assemblee_id)

    fmt = request.GET.get('format', '')
    if fmt in ('pdf', 'xlsx', 'docx'):
        entetes = ['Matricule', 'Nom', 'Prénom(s)', 'Sexe', 'Tél.', 'Assemblée', 'Baptisé', 'Travaille']
        lignes = [[
            d.matricule, d.nom, d.prenoms, d.get_sexe_display(), d.telephone,
            str(d.assemblee), 'Oui' if d.bapteme else 'Non', 'Oui' if d.travaille else 'Non',
        ] for d in qs]
        titre = 'Liste des Disciples – LGDA-CMCI'
        if fmt == 'xlsx':
            return export_excel(titre, entetes, lignes, 'liste_disciples.xlsx')
        elif fmt == 'pdf':
            return export_pdf(titre, entetes, lignes, 'liste_disciples.pdf')
        else:
            return export_word(titre, entetes, lignes, 'liste_disciples.docx')

    ctx = {
        'disciples': qs,
        'pays_list': Pays.objects.all(),
        'villes': Ville.objects.all(),
        'zones': Zone.objects.all(),
        'sous_centres': SousCentre.objects.all(),
        'assemblees': Assemblee.objects.all(),
        'selected': {'pays': pays_id, 'ville': ville_id, 'zone': zone_id, 'sous_centre': sc_id, 'assemblee': assemblee_id},
    }
    return render(request, 'rapports/liste_disciples.html', ctx)


# ─── LISTE ÉVANGÉLISTES ──────────────────────────────────────────────────────

@login_required
def liste_evangelistes(request):
    qs = Evangeliste.objects.select_related('sous_centre__zone__ville__pays')
    pays_id = request.GET.get('pays')
    ville_id = request.GET.get('ville')
    zone_id = request.GET.get('zone')
    sc_id = request.GET.get('sous_centre')
    if pays_id:
        qs = qs.filter(sous_centre__zone__ville__pays_id=pays_id)
    if ville_id:
        qs = qs.filter(sous_centre__zone__ville_id=ville_id)
    if zone_id:
        qs = qs.filter(sous_centre__zone_id=zone_id)
    if sc_id:
        qs = qs.filter(sous_centre_id=sc_id)

    fmt = request.GET.get('format', '')
    if fmt in ('pdf', 'xlsx', 'docx'):
        entetes = ['Nom', 'Prénom(s)', 'Tél.', 'Qualité', 'Sous-centre', 'Zone', 'Ville', 'Pays']
        lignes = [[
            e.nom, e.prenoms, e.telephone, e.get_qualite_display(),
            str(e.sous_centre), str(e.sous_centre.zone), str(e.sous_centre.zone.ville),
            str(e.sous_centre.zone.ville.pays),
        ] for e in qs]
        titre = 'Liste des Évangélistes – LGDA-CMCI'
        if fmt == 'xlsx':
            return export_excel(titre, entetes, lignes, 'liste_evangelistes.xlsx')
        elif fmt == 'pdf':
            return export_pdf(titre, entetes, lignes, 'liste_evangelistes.pdf')
        else:
            return export_word(titre, entetes, lignes, 'liste_evangelistes.docx')

    ctx = {
        'evangelistes': qs,
        'pays_list': Pays.objects.all(),
        'villes': Ville.objects.all(),
        'zones': Zone.objects.all(),
        'sous_centres': SousCentre.objects.all(),
        'selected': {'pays': pays_id, 'ville': ville_id, 'zone': zone_id, 'sous_centre': sc_id},
    }
    return render(request, 'rapports/liste_evangelistes.html', ctx)


# ─── RAPPORT ÉVANGÉLISATION ──────────────────────────────────────────────────

@login_required
def rapport_evangelisation(request):
    periode = request.GET.get('periode', 'hebdomadaire')
    semaine = request.GET.get('semaine', date.today().isocalendar()[1])
    mois = request.GET.get('mois', date.today().month)
    annee = request.GET.get('annee', date.today().year)
    perimetre = request.GET.get('perimetre', 'assemblee')

    try:
        semaine = int(semaine)
        mois = int(mois)
        annee = int(annee)
    except (ValueError, TypeError):
        semaine, mois, annee = date.today().isocalendar()[1], date.today().month, date.today().year

    qs = PlanningEvangelisation.objects.all()

    # Filtre temporel
    if periode == 'hebdomadaire':
        qs = qs.filter(semaine=semaine)
    elif periode == 'mensuel':
        semaines_mois = _get_semaines_du_mois(annee, mois)
        qs = qs.filter(semaine__in=semaines_mois)
    elif periode == 'annuel':
        semaines_annee = _get_semaines_de_lannee_partielle(annee)
        qs = qs.filter(semaine__in=semaines_annee)

    # Filtre périmètre
    perimetre_id = request.GET.get('perimetre_id')
    if perimetre == 'evangeliste' and perimetre_id:
        qs = qs.filter(evangeliste_id=perimetre_id)
    elif perimetre == 'assemblee' and perimetre_id:
        qs = qs.filter(assemblee_id=perimetre_id)
    elif perimetre == 'sous_centre' and perimetre_id:
        qs = qs.filter(assemblee__sous_centre_id=perimetre_id)
    elif perimetre == 'zone' and perimetre_id:
        qs = qs.filter(assemblee__sous_centre__zone_id=perimetre_id)
    elif perimetre == 'ville' and perimetre_id:
        qs = qs.filter(assemblee__sous_centre__zone__ville_id=perimetre_id)
    elif perimetre == 'pays' and perimetre_id:
        qs = qs.filter(assemblee__sous_centre__zone__ville__pays_id=perimetre_id)

    total = qs.count()
    rdv_ok = qs.filter(statut_rdv='ok').count()
    engagements_ok = qs.filter(statut_engagement='ok').count()
    taux_rdv = round(rdv_ok / total * 100, 1) if total else 0
    taux_engagement = round(engagements_ok / total * 100, 1) if total else 0

    stats = {
        'total': total,
        'rdv_ok': rdv_ok,
        'taux_rdv': taux_rdv,
        'engagements_ok': engagements_ok,
        'taux_engagement': taux_engagement,
    }

    fmt = request.GET.get('format', '')
    if fmt in ('pdf', 'xlsx', 'docx'):
        entetes = ['Indicateur', 'Valeur', 'Taux (%)']
        lignes = [
            ['Nombre RDV pris', total, '100%'],
            ['Nombre RDV réalisés', rdv_ok, f'{taux_rdv}%'],
            ['Nombre engagements obtenus', engagements_ok, f'{taux_engagement}%'],
        ]
        titre = f'Rapport d\'évangélisation – LGDA-CMCI ({periode})'
        if fmt == 'xlsx':
            return export_excel(titre, entetes, lignes, 'rapport_evangelisation.xlsx')
        elif fmt == 'pdf':
            return export_pdf(titre, entetes, lignes, 'rapport_evangelisation.pdf')
        else:
            return export_word(titre, entetes, lignes, 'rapport_evangelisation.docx')

    ctx = {
        'stats': stats,
        'periode': periode,
        'semaine': semaine,
        'mois': mois,
        'annee': annee,
        'perimetre': perimetre,
        'perimetre_id': perimetre_id,
        'evangelistes': Evangeliste.objects.all(),
        'assemblees': Assemblee.objects.all(),
        'sous_centres': SousCentre.objects.all(),
        'zones': Zone.objects.all(),
        'villes': Ville.objects.all(),
        'pays_list': Pays.objects.all(),
        'annees': list(range(2020, date.today().year + 1)),
        'mois_list': [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)],
        'semaines_list': list(range(1, 54)),
    }
    return render(request, 'rapports/rapport_evangelisation.html', ctx)


# ─── RAPPORT ASSIDUITÉ ───────────────────────────────────────────────────────

@login_required
def rapport_assiduite(request):
    periode = request.GET.get('periode', 'mensuel')
    semaine = request.GET.get('semaine', date.today().isocalendar()[1])
    mois = request.GET.get('mois', date.today().month)
    annee = request.GET.get('annee', date.today().year)
    perimetre = request.GET.get('perimetre', 'assemblee')

    try:
        semaine = int(semaine)
        mois = int(mois)
        annee = int(annee)
    except (ValueError, TypeError):
        semaine, mois, annee = date.today().isocalendar()[1], date.today().month, date.today().year

    qs = AssiduiteCulte.objects.select_related('disciple__assemblee')

    # Filtre temporel
    if periode == 'hebdomadaire':
        qs = qs.filter(semaine=semaine)
    elif periode == 'mensuel':
        semaines_mois = _get_semaines_du_mois(annee, mois)
        qs = qs.filter(semaine__in=semaines_mois)
    elif periode == 'annuel':
        semaines_annee = _get_semaines_de_lannee_partielle(annee)
        qs = qs.filter(semaine__in=semaines_annee)

    # Filtre périmètre
    perimetre_id = request.GET.get('perimetre_id')
    if perimetre == 'disciple' and perimetre_id:
        qs = qs.filter(disciple_id=perimetre_id)
    elif perimetre == 'assemblee' and perimetre_id:
        qs = qs.filter(disciple__assemblee_id=perimetre_id)
    elif perimetre == 'sous_centre' and perimetre_id:
        qs = qs.filter(disciple__assemblee__sous_centre_id=perimetre_id)
    elif perimetre == 'zone' and perimetre_id:
        qs = qs.filter(disciple__assemblee__sous_centre__zone_id=perimetre_id)
    elif perimetre == 'ville' and perimetre_id:
        qs = qs.filter(disciple__assemblee__sous_centre__zone__ville_id=perimetre_id)
    elif perimetre == 'pays' and perimetre_id:
        qs = qs.filter(disciple__assemblee__sous_centre__zone__ville__pays_id=perimetre_id)

    total = qs.count()
    presents = qs.filter(present=True).count()
    absents = total - presents
    taux_presence = round(presents / total * 100, 1) if total else 0
    taux_absence = round(absents / total * 100, 1) if total else 0

    stats = {
        'total': total,
        'presents': presents,
        'absents': absents,
        'taux_presence': taux_presence,
        'taux_absence': taux_absence,
    }

    fmt = request.GET.get('format', '')
    if fmt in ('pdf', 'xlsx', 'docx'):
        entetes = ['Indicateur', 'Valeur', 'Taux (%)']
        lignes = [
            ["Nombre d'adorations (entrées)", total, '100%'],
            ['Présences', presents, f'{taux_presence}%'],
            ['Absences', absents, f'{taux_absence}%'],
        ]
        titre = f"Rapport d'assiduité à l'adoration – LGDA-CMCI ({periode})"
        if fmt == 'xlsx':
            return export_excel(titre, entetes, lignes, 'rapport_assiduite.xlsx')
        elif fmt == 'pdf':
            return export_pdf(titre, entetes, lignes, 'rapport_assiduite.pdf')
        else:
            return export_word(titre, entetes, lignes, 'rapport_assiduite.docx')

    ctx = {
        'stats': stats,
        'periode': periode,
        'semaine': semaine,
        'mois': mois,
        'annee': annee,
        'perimetre': perimetre,
        'perimetre_id': perimetre_id,
        'disciples': Disciple.objects.all(),
        'assemblees': Assemblee.objects.all(),
        'sous_centres': SousCentre.objects.all(),
        'zones': Zone.objects.all(),
        'villes': Ville.objects.all(),
        'pays_list': Pays.objects.all(),
        'annees': list(range(2020, date.today().year + 1)),
        'mois_list': [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)],
        'semaines_list': list(range(1, 54)),
    }
    return render(request, 'rapports/rapport_assiduite.html', ctx)
