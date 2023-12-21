import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from utilisateurs.models import Utilisateurs
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.apps import apps  
from itertools import chain
from django.db.models import Sum  
from django.contrib.auth.decorators import login_required
from .forms import TypeChambreForm, ChambreForm, ClientForm, AffectationChambreForm
from .models import TypeChambre, Chambre, Client, AffectationChambre
from .models import Chambre, Client
from personnels.models import Personnel
from utilisateurs.models import Utilisateurs
from datetime import datetime

from datetime import timedelta

# views.py

from django.shortcuts import render
from .models import AffectationChambre, Chambre

from django.contrib.auth.decorators import login_required

@login_required(login_url='connexion')
def index(request):

    maintenant = timezone.now()
    un_jour_plus_tard = maintenant + timedelta(days=1)

    debut_semaine = maintenant - timedelta(days=maintenant.weekday())
    fin_semaine = debut_semaine + timedelta(days=6)

    nb_utilisateurs = Utilisateurs.objects.count()
    nb_personnels = Personnel.objects.count()
    nb_chambres = Chambre.objects.count()
    nb_clients = Client.objects.count()

    notifications_expirees = Notification.objects.filter(
        date_notification__lt=maintenant - timedelta(hours=23)
    ).order_by('date_notification', 'heure_notification')

    notifications_expirees.delete()

    notifications_prochaines = Notification.objects.filter(
        date_notification__gte=maintenant.date(),
        date_notification__lte=un_jour_plus_tard
    ).order_by('date_notification', 'heure_notification')

    # Chambres
    chambres = Chambre.objects.all()
    nb_chambres_occupees = sum(chambre.nombre_chambres_occupees() for chambre in chambres)
    nb_chambres_libres = Chambre.objects.filter(etat='disponible', affectationchambre__isnull=True).count()
    nb_chambres_indisponibles = Chambre.objects.filter(etat='indisponible').count()
    nb_total_chambres = Chambre.objects.count()

    # Réservations
    nb_reservations_jour = AffectationChambre.nombre_reservations_jour()
    nb_reservations_semaine = AffectationChambre.nombre_reservations_semaine()
    nb_reservations_mois = AffectationChambre.nombre_reservations_mois()
    nb_total_reservations = AffectationChambre.nombre_total_reservations()

    context = {
        'nb_utilisateurs': nb_utilisateurs,
        'nb_personnels': nb_personnels,
        'nb_chambres': nb_chambres,
        'nb_clients': nb_clients,
        'notifications_prochaines': notifications_prochaines,
        'notifications_expirees': notifications_expirees,

        'nb_chambres_occupees': nb_chambres_occupees,
        'nb_chambres_libres': nb_chambres_libres,
        'nb_chambres_indisponibles': nb_chambres_indisponibles,
        'nb_total_chambres': nb_total_chambres,

        'nb_reservations_jour': nb_reservations_jour,
        'nb_reservations_semaine': nb_reservations_semaine,
        'nb_reservations_mois': nb_reservations_mois,
        'nb_total_reservations': nb_total_reservations,
    }

    return render(request, "index.html", context)





@login_required(login_url='connexion')
def ajouter_type_chambre(request):
    if request.method == 'POST':
        form = TypeChambreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le type de chambre a été ajouté avec succès.')
            return redirect('ajouter_type_chambre')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = TypeChambreForm()

    return render(request, 'ajouter_type_chambre.html', {'form': form})

@login_required(login_url='connexion')
def ajouter_chambre(request):
    if request.method == 'POST':
        form = ChambreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La chambre a été ajoutée avec succès.')
            return redirect('ajouter_chambre')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = ChambreForm()

    return render(request, 'ajouter_chambre.html', {'form': form})

@login_required(login_url='connexion')
def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le client a été ajouté avec succès.')
            return redirect('ajouter_client')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = ClientForm()

    return render(request, 'ajouter_client.html', {'form': form})


@login_required(login_url='connexion')
def ajouter_affectation(request):
    if request.method == 'POST':
        form = AffectationChambreForm(request.POST)
        if form.is_valid():
            affectation = form.save(commit=False)

            # Vérifier que la date et l'heure de début ne sont pas dans le passé
            maintenant = datetime.now()
            date_heure_debut = datetime.combine(affectation.date_debut, affectation.heure_debut)
            if date_heure_debut < maintenant:
                messages.error(request, 'La date et l\'heure de début ne peuvent pas être dans le passé.')
                return redirect('ajouter_affectation')

            # Vérifier que la chambre n'est pas déjà affectée à un client dans la même période
            affectations_conflit = AffectationChambre.objects.filter(
                chambre=affectation.chambre,
                date_fin__gt=affectation.date_debut,
                date_debut__lt=affectation.date_fin
            )
            if affectations_conflit.exists():
                messages.error(request, 'La chambre est déjà réservée pour cette période.')
                return redirect('ajouter_affectation')

            # Vérifier que la chambre n'est pas indisponible
            if affectation.chambre.etat == 'indisponible':
                messages.error(request, 'La chambre est actuellement indisponible.')
                return redirect('ajouter_affectation')

            # Vérifier que la chambre n'est pas occupée dans la même période
            if affectation.chambre.nombre_chambres_occupees() > 0:
                messages.error(request, 'La chambre est déjà occupée pour cette période.')
                return redirect('ajouter_affectation')

            # Enregistrer l'affectation si toutes les vérifications sont passées
            affectation.save()
            messages.success(request, 'L\'affectation de chambre a été ajoutée avec succès.')

            return redirect('ajouter_affectation')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = AffectationChambreForm()

    return render(request, 'ajouter_affectation.html', {'form': form})



@login_required(login_url='connexion')
def liste_type_chambres(request):
    types_chambres = TypeChambre.objects.all()
    return render(request, 'liste_type_chambres.html', {'types_chambres': types_chambres})

@login_required(login_url='connexion')
def liste_chambres(request):
    chambres = Chambre.objects.all()
    return render(request, 'liste_chambres.html', {'chambres': chambres})

@login_required(login_url='connexion')
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'liste_clients.html', {'clients': clients})

@login_required(login_url='connexion')
def liste_affectations(request):
    affectations = AffectationChambre.objects.all()
    return render(request, 'liste_affectations.html', {'affectations': affectations})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='connexion')
def supprimer_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)
    nom = type_chambre.nom  # Stockez le nom avant la suppression
    type_chambre.delete()
    messages.success(request, f"Le type de chambre {nom} a été supprimé avec succès.")
    return redirect('liste_type_chambres')

@login_required(login_url='connexion')
def supprimer_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)
    numero = chambre.numero  # Stockez le numéro avant la suppression
    chambre.delete()
    messages.success(request, f"La chambre {numero} a été supprimée avec succès.")
    return redirect('liste_chambres')

@login_required(login_url='connexion')
def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    nom_prenom = client.nom_prenom  # Stockez le nom_prenom avant la suppression
    client.delete()
    messages.success(request, f"Le client {nom_prenom} a été supprimé avec succès.")
    return redirect('liste_clients')

@login_required(login_url='connexion')
def supprimer_affectation(request, pk):
    affectation = get_object_or_404(AffectationChambre, pk=pk)
    chambre_info = f"{affectation.chambre} - {affectation.client}"  # Stockez les informations avant la suppression
    affectation.delete()
    messages.success(request, f"L'affectation de chambre {chambre_info} a été supprimée avec succès.")
    return redirect('liste_affectations')



@login_required(login_url='connexion')
def modifier_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)

    if request.method == 'POST':
        form = TypeChambreForm(request.POST, instance=type_chambre)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les informations du type de chambre {type_chambre.nom} ont été mises à jour.")
            return redirect('liste_type_chambres')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = TypeChambreForm(instance=type_chambre)

    return render(request, 'modifier_type_chambre.html', {'form': form, 'type_chambre': type_chambre})

@login_required(login_url='connexion')
def modifier_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)

    if request.method == 'POST':
        form = ChambreForm(request.POST, instance=chambre)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les informations de la chambre {chambre.numero} ont été mises à jour.")
            return redirect('liste_chambres')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = ChambreForm(instance=chambre)

    return render(request, 'modifier_chambre.html', {'form': form, 'chambre': chambre})

@login_required(login_url='connexion')
def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les informations du client {client.nom_prenom} ont été mises à jour.")
            return redirect('liste_clients')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = ClientForm(instance=client)

    return render(request, 'modifier_client.html', {'form': form, 'client': client})

@login_required(login_url='connexion')
def modifier_affectation(request, pk):
    affectation = get_object_or_404(AffectationChambre, pk=pk)

    if request.method == 'POST':
        form = AffectationChambreForm(request.POST, instance=affectation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les informations de l'affectation de chambre {affectation.chambre} ont été mises à jour.")
            return redirect('liste_affectations')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = AffectationChambreForm(instance=affectation)

    return render(request, 'modifier_affectation.html', {'form': form, 'affectation': affectation})



from .forms import PiecesJointesForm


@login_required(login_url='connexion')
def creer_piece_jointe(request):
    if request.method == 'POST':
        form = PiecesJointesForm(request.POST, request.FILES)
        if form.is_valid():
            piece_jointe = form.save()
            messages.success(request, f'La pièce jointe "{piece_jointe.titre}" a été créée avec succès.')

            return redirect('creer_piece_jointe')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez corriger les erreurs.')
    else:
        form = PiecesJointesForm()

    return render(request, 'creer_piece_jointe.html', {'form': form})



from .models import PiecesJointes



@login_required(login_url='connexion')
def listes_piece_jointe(request):
    pieces_jointes = PiecesJointes.objects.all()
    return render(request, 'listes_piece_jointe.html', {'pieces_jointes': pieces_jointes})


@login_required(login_url='connexion')
def supprimer_piece_jointe(request, pk):
    pieces_jointes = get_object_or_404(PiecesJointes, pk=pk)
    pieces_jointes.delete()
    messages.success(request, f"Suppression effectuée avec succès.")
    return redirect('listes_piece_jointe')



from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from .forms import NotificationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.utils import timezone
from .models import Notification

@login_required(login_url='connexion')
def liste_notifications(request):
    notifications = Notification.objects.all()

    # Filtrer les notifications actives
    notifications_actives = [n for n in notifications if n.date_notification >= timezone.now().date()
                             and n.heure_notification >= timezone.now().time()]

    # Filtrer les notifications expirées
    notifications_expirees = [n for n in notifications if n.date_notification < timezone.now().date()
                              or (n.date_notification == timezone.now().date()
                                  and n.heure_notification < timezone.now().time())]

    return render(request, 'liste_notifications.html', {
        'notifications_actives': notifications_actives,
        'notifications_expirees': notifications_expirees,
    })



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .context_processors import notifications_toutes

@login_required(login_url='connexion')
def header(request):
    context = notifications_toutes(request)
    nombre_notifications = len(context['notifications_toutes'])
    return render(request, 'header.html', {'notifications': context['notifications_toutes'], 'nombre_notifications': nombre_notifications})



@login_required(login_url='connexion')
def ajouter_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La notification a été ajoutée avec succès.')
            return redirect('ajouter_notification')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = NotificationForm()

    return render(request, "ajouter_notification.html", {'form': form})

@login_required(login_url='connexion')
def supprimer_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    nom_notification = notification.nom_notification
    notification.delete()
    messages.success(request, f"La notification '{nom_notification}' a été supprimée avec succès.")
    return redirect('liste_notifications')

@login_required(login_url='connexion')
def modifier_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)

    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            messages.success(request, f"La notification '{notification.nom_notification}' a été mise à jour.")
            return redirect('liste_notifications')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = NotificationForm(instance=notification)

    return render(request, 'modifier_notification.html', {'form': form, 'notification': notification})
