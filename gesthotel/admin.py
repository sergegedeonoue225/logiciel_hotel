from django.contrib import admin
from .models import TypeChambre, Chambre, Client, AffectationChambre

class TypeChambreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix_nuit', 'prix_heure')
    search_fields = ('nom',)

class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'type_chambre', 'etat', 'nombre_lits', 'date_creation', 'date_mise_a_jour')
    list_filter = ('etat', 'type_chambre')
    search_fields = ('numero', 'type_chambre__nom')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom_prenom', 'telephone', 'email')
    search_fields = ('nom_prenom', 'telephone')

class AffectationChambreAdmin(admin.ModelAdmin):
    list_display = ('chambre', 'date_debut', 'heure_debut', 'date_fin', 'heure_fin', 'client', 'client_anonyme')
    list_filter = ('date_debut', 'date_fin', 'client_anonyme')
    search_fields = ('chambre__numero', 'client__nom_prenom', 'client__telephone')

admin.site.register(TypeChambre, TypeChambreAdmin)
admin.site.register(Chambre, ChambreAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(AffectationChambre, AffectationChambreAdmin)


from django.contrib import admin
from .models import PiecesJointes

class PiecesJointesAdmin(admin.ModelAdmin):
    list_display = ('titre', 'contenu', 'piece_jointe', 'date_creation')
    search_fields = ('titre', 'date_creation')
    list_filter = ('date_creation',)

admin.site.register(PiecesJointes, PiecesJointesAdmin)


from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('nom_notification', 'date_notification', 'heure_notification',)
    search_fields = ('nom_notification','date_notification',)

admin.site.register(Notification, NotificationAdmin)