from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Utilisateurs, RecentAction
from .forms import UtilisateursCreationForm, UtilisateurmettreajourForm


def acces_oublier(request):
    return render(request, "acces_oublier.html")

def changer_motdepasse(request):
    return render(request, "changer_motdepasse.html")

def connexion(request):
    return render(request, "connexion.html")

def lienenvoyer_mdp(request):
    return render(request, "lienenvoyer_mdp.html")


def merci_motdepasse(request):
    return render(request, "merci_motdepasse.html")

def merci_mdp_changer(request):
    return render(request, "merci_mdp_changer.html")

def connexion(request):

  if request.method == 'POST':

    email = request.POST.get('email')
    password = request.POST.get('password')
    
    try:
      validate_email(email)
    except ValidationError as e:
      messages.error(request, f"Adresse email invalide: {e}")
      return redirect('connexion')
      
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
      login(request, user)
      return redirect('index')
      
    else:
      messages.error(request, "Email ou mot de passe incorrect.")
      return redirect('connexion')

  return render(request, 'connexion.html')




def deconnexion(request):
  logout(request)
  messages.success(request, "Déconnexion réussie.")
  return redirect('connexion')


@login_required(login_url='connexion')
def profile(request):
    # Obtenez les informations de l'utilisateur actuellement connecté
    user = request.user
    user_info = {
        'email': user.email,
        'nom_complet': user.nom_complet,
        'fonction': user.fonction.nom_fonction if user.fonction else None,
    }

    return render(request, "profile.html", {'user_info': user_info})



from django.shortcuts import render
from guardian.shortcuts import assign_perm
from .models import Fonction

def permissions_view(request):
    # Liste des fonctions disponibles
    fonctions = Fonction.objects.all()

    if request.method == 'POST':
        selected_fonction = request.POST.get('fonction')
        selected_permission = request.POST.get('permission')
        user = request.user

        # Supprime toutes les autorisations existantes pour cet utilisateur et cette fonction
        for permission in ['can_view_dashboard', 'can_view_utilisateurs', ...]:  # Ajoutez toutes vos permissions
            assign_perm(permission, user, Fonction.objects.get(pk=selected_fonction))

        # Assignez la nouvelle autorisation sélectionnée
        assign_perm(selected_permission, user, Fonction.objects.get(pk=selected_fonction))

    context = {'fonctions': fonctions}
    return render(request, 'permissions.html', context)







@login_required(login_url='connexion')
def ajouter_utilisateurs(request):
    if request.method == 'POST':
        form = UtilisateursCreationForm(request.POST, request.FILES)
        if form.is_valid():
            utilisateur = form.save()
            messages.success(request, f'L\'utilisateur "{utilisateur.email}" a été ajouté avec succès.')
            
            # Enregistrez l'action récente avec le nom de l'utilisateur
            action = f'Ajout de l\'utilisateur "{utilisateur.email}"'
            user = request.user
            RecentAction.objects.create(action=action, user=user)
            
            return redirect('ajouter_utilisateurs')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = UtilisateursCreationForm()

    return render(request, "ajouter_utilisateurs.html", {'form': form})

@login_required(login_url='connexion')
def supprimer_utilisateur(request, user_id):
    if request.method == 'GET':
        utilisateur = get_object_or_404(Utilisateurs, id=user_id)
        
        # Enregistrez l'action récente avec le nom de l'utilisateur avant de le supprimer
        action = f'Suppression de l\'utilisateur "{utilisateur.email}"'
        user = request.user
        RecentAction.objects.create(action=action, user=user)
        
        utilisateur.delete()
        messages.success(request, 'Utilisateur supprimé avec succès')
        return redirect('listes_utilisateurs')
    else:
        # Gérer les autres méthodes HTTP si nécessaire
        return HttpResponseNotAllowed(['GET'])

@login_required(login_url='connexion')
def modifier_utilisateur(request, user_id):
    utilisateur = get_object_or_404(Utilisateurs, id=user_id)

    if request.method == 'POST':
        form = UtilisateurmettreajourForm(request.POST, request.FILES, instance=utilisateur)
        if form.is_valid():
            if not form.cleaned_data.get('password'):
                form.fields['password'].required = False
            form.save()
            messages.success(request, f'L\'utilisateur "{utilisateur.email}" a été modifié avec succès.')
            
            # Enregistrez l'action récente avec le nom de l'utilisateur
            action = f'Modification de l\'utilisateur "{utilisateur.email}"'
            user = request.user
            RecentAction.objects.create(action=action, user=user)
            
            return redirect('modifier_utilisateur')
        else:
            messages.error(request, 'Il y a des erreurs dans le formulaire. Veuillez le corriger.')
    else:
        form = UtilisateurmettreajourForm(instance=utilisateur)

    return render(request, 'modifier_utilisateur.html', {'utilisateur': utilisateur, 'form': form})


@login_required(login_url='connexion')
def listes_utilisateurs(request):
    utilisateurs = Utilisateurs.objects.all()
    context = {'utilisateurs': utilisateurs}
    return render(request, "listes_utilisateurs.html", context)
