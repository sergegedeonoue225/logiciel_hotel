from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from utilisateurs.models import RecentAction, Utilisateurs
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import Personnel
from .forms import PersonnelForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='connexion')
def ajouter_personnel(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le personnel Personnel a été ajouté avec succès.')
            return redirect('ajouter_personnel')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = PersonnelForm()

        action = f'ajout du personnel "{Personnel.email}"'
        user = request.user
        RecentAction.objects.create(action=action, user=user)
        

    return render(request, "ajouter_personnel.html", {'form': form})





@login_required(login_url='connexion')
def liste_personnel(request):
    personnels = Personnel.objects.all()
    return render(request, 'liste_personnel.html', {'personnels': personnels})


@login_required(login_url='connexion')
def supprimer_personnel(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    nom_prenom = personnel.nom_prenom  # Stockez le nom_prenom avant la suppression
    personnel.delete()
    messages.success(request, f"Le personnel {nom_prenom} a été supprimé avec succès.")
    return redirect('liste_personnel')


@login_required(login_url='connexion')
def modifier_personnel(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)

    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=personnel)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les informations de {personnel.nom_prenom} ont été mises à jour.")
            return redirect('liste_personnel')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = PersonnelForm(instance=personnel)

    return render(request, 'modifier_personnel.html', {'form': form, 'personnel': personnel})
