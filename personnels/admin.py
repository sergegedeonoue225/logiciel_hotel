from django.contrib import admin
from .models import Personnel

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('nom_prenom', 'poste', 'date_embauche', 'statut')
    list_filter = ('poste', 'statut', 'genre')
    search_fields = ('nom_prenom', 'poste', 'adresse', 'telephone', 'email')

    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('nom_prenom', 'date_naissance', 'nationalite', 'lieu_naissance', 'numero_cni', 'genre')
        }),
        ('Poste et Statut', {
            'fields': ('poste', 'date_embauche', 'statut')
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'telephone', 'email')
        }),
        ('Images et Documents', {
            'fields': ('profile_image', 'piece_identite_recto', 'piece_identite_verso')
        }),
    )

admin.site.register(Personnel, PersonnelAdmin)
