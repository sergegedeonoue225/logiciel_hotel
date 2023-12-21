from django.conf import settings
from django.contrib import admin
from django.urls import path, reverse_lazy
from utilisateurs import views as utilisateurs_views
from gesthotel import views as gesthotel_views, views_pdf
from personnels import views as personnels_views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from finances import views as finances_views



urlpatterns = [
    path('pdf_liste_utilisateurs/', views_pdf.PDFView_liste_utilisateurs.as_view(), name='pdf_liste_utilisateurs'),
    path('pdf_liste_personnels/', views_pdf.PDFView_liste_personnels.as_view(), name='pdf_liste_personnels'),






    path('admin/', admin.site.urls),
    path("", gesthotel_views.index, name="index"), 
    path("acces_oublier/", utilisateurs_views.acces_oublier, name="acces_oublier"),
    path("changer_motdepasse/", utilisateurs_views.changer_motdepasse, name="changer_motdepasse"),
    path("connexion/", utilisateurs_views.connexion, name="connexion"),
    path("lienenvoyer_mdp/", utilisateurs_views.lienenvoyer_mdp, name="lienenvoyer_mdp"), 
    path("merci_motdepasse/", utilisateurs_views.merci_motdepasse, name="merci_motdepasse"), 
    path("deconnexion/", utilisateurs_views.deconnexion, name="deconnexion"),
    path("profile/", utilisateurs_views.profile, name="profile"),
    path("merci_mdp_changer/", utilisateurs_views.merci_mdp_changer, name="merci_mdp_changer"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='acces_oublier.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='lienenvoyer_mdp.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='merci_motdepasse.html'), name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='profile.html'), name='password_change'),   
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='merci_mdp_changer.html'), name='password_change_done'),
    
    path("ajouter_utilisateurs/", utilisateurs_views.ajouter_utilisateurs, name="ajouter_utilisateurs"), 
    path('modifier_utilisateur/<int:user_id>/', utilisateurs_views.modifier_utilisateur, name='modifier_utilisateur'),
    path("listes_utilisateurs/", utilisateurs_views.listes_utilisateurs, name="listes_utilisateurs"), 
    path('supprimer_utilisateur/<int:user_id>/',utilisateurs_views.supprimer_utilisateur, name='supprimer_utilisateur'),


    path("ajouter_personnel/", personnels_views.ajouter_personnel, name="ajouter_personnel"), 
    path('liste_personnel/', personnels_views.liste_personnel, name='liste_personnel'),
    path('supprimer_personnel/<int:pk>/', personnels_views.supprimer_personnel, name='supprimer_personnel'),
    path('modifier_personnel/<int:pk>/', personnels_views.modifier_personnel, name='modifier_personnel'),


    path('ajouter_type_chambre/', gesthotel_views.ajouter_type_chambre, name='ajouter_type_chambre'),
    path('modifier_type_chambre/<int:pk>/', gesthotel_views.modifier_type_chambre, name='modifier_type_chambre'),
    path('liste_type_chambres/', gesthotel_views.liste_type_chambres, name='liste_type_chambres'),
    path('supprimer_type_chambre/<int:pk>/', gesthotel_views.supprimer_type_chambre, name='supprimer_type_chambre'),

    # URLs pour Chambre
    path('ajouter_chambre/', gesthotel_views.ajouter_chambre, name='ajouter_chambre'),
    path('modifier_chambre/<int:pk>/', gesthotel_views.modifier_chambre, name='modifier_chambre'),
    path('liste_chambres/', gesthotel_views.liste_chambres, name='liste_chambres'),
    path('supprimer_chambre/<int:pk>/', gesthotel_views.supprimer_chambre, name='supprimer_chambre'),

    # URLs pour Client
    path('ajouter_client/', gesthotel_views.ajouter_client, name='ajouter_client'),
    path('modifier_client/<int:pk>/', gesthotel_views.modifier_client, name='modifier_client'),
    path('liste_clients/', gesthotel_views.liste_clients, name='liste_clients'),
    path('supprimer_client/<int:pk>/', gesthotel_views.supprimer_client, name='supprimer_client'),

    # URLs pour AffectationChambre
    path('ajouter_affectation/', gesthotel_views.ajouter_affectation, name='ajouter_affectation'),
    path('modifier_affectation/<int:pk>/', gesthotel_views.modifier_affectation, name='modifier_affectation'),
    path('liste_affectations/', gesthotel_views.liste_affectations, name='liste_affectations'),
    path('supprimer_affectation/<int:pk>/', gesthotel_views.supprimer_affectation, name='supprimer_affectation'),

    path("creer_piece_jointe/", gesthotel_views.creer_piece_jointe, name="creer_piece_jointe"),
    path("listes_piece_jointe/", gesthotel_views.listes_piece_jointe, name="listes_piece_jointe"), 
    path('supprimer_piece_jointe/<int:pk>/', gesthotel_views.supprimer_piece_jointe, name='supprimer_piece_jointe'),
    

    path("ajouter_notification/", gesthotel_views.ajouter_notification, name="ajouter_notification"),
    path("liste_notifications/", gesthotel_views.liste_notifications, name="liste_notifications"), 
    path('supprimer_notification/<int:pk>/', gesthotel_views.supprimer_notification, name='supprimer_notification'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
