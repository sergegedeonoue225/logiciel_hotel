from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateurs, Fonction

class UtilisateursAdmin(UserAdmin):
    model = Utilisateurs
    list_display = ['email', 'nom_complet', 'profile_image','fonction', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('nom_complet','profile_image', 'fonction')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom_complet','profile_image', 'fonction', 'password1', 'password2'),
        }),
    )
    search_fields = ['email']
    ordering = ['email']

class FonctionAdmin(admin.ModelAdmin):
    list_display = ['nom_fonction']

admin.site.register(Utilisateurs, UtilisateursAdmin)
admin.site.register(Fonction, FonctionAdmin)

admin.site.site_header = "Administration de GESTHOTEL"
admin.site.site_title = "Administration de GESTHOTEL"
admin.site.index_title = "Bienvenue dans l'Administration de GESTHOTEL"
