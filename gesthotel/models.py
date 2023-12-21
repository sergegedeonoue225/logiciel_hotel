import calendar
from django.db import models
from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone

class TypeChambre(models.Model):
    nom = models.CharField(max_length=50, verbose_name='Nom du type de chambre')
    prix_nuit = models.IntegerField(verbose_name='Prix par nuit')
    prix_heure = models.IntegerField(verbose_name='Prix par heure')
    description = models.TextField(verbose_name='Description du type de chambre')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Type de chambre'
        verbose_name_plural = 'Types de chambres'

class Client(models.Model):
    nom_prenom = models.CharField(max_length=100, verbose_name='Nom du client')
    adresse = models.CharField(max_length=100,blank=True, null=True, verbose_name='Adresse du client')
    email = models.EmailField(blank=True, null=True, verbose_name='Email du client')
    telephone = models.CharField(max_length=15, verbose_name='Téléphone du client')

    def __str__(self):
        return f"{self.nom_prenom} {self.telephone}"
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'






class Chambre(models.Model):
    ETAT_CHOICES = [
        ('disponible', 'Disponible'),
        ('nettoyage', 'En nettoyage'),
        ('indisponible', 'Indisponible'),
    ]

    numero = models.CharField(max_length=10, unique=True, verbose_name='Numéro de chambre')
    type_chambre = models.ForeignKey(TypeChambre, on_delete=models.CASCADE, verbose_name='Type de chambre')
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='disponible', verbose_name='État de la chambre')
    nombre_lits = models.PositiveIntegerField(verbose_name='Nombre de lits')
    description = models.TextField(blank=True, null=True, verbose_name='Description de la chambre')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')

    def __str__(self):
        return f" {self.numero} - {self.type_chambre.nom}"

    class Meta:
        ordering = ['numero']
        verbose_name = 'Chambre'
        verbose_name_plural = 'Chambres'

    def nombre_total_chambres(self):
        return Chambre.objects.count()

 

    def nombre_chambres_occupees(self):
        return AffectationChambre.objects.filter(
            chambre__id=self.id,  # Filtrer par l'id de la chambre actuelle
            date_fin__gte=timezone.now().date(),
            date_debut__lte=timezone.now().date()
        ).count()



    def nombre_chambres_libres(self):
        return Chambre.objects.filter(
            etat='disponible',
            affectationchambre__isnull=True
        ).count()

    def nombre_chambres_indisponibles(self):
        return Chambre.objects.filter(etat='indisponible').count()



class AffectationChambre(models.Model):
    chambre = models.ForeignKey('Chambre', on_delete=models.CASCADE, verbose_name='Chambre')
    date_debut = models.DateField(verbose_name='Date de début')
    heure_debut = models.TimeField(verbose_name='Heure de début')
    date_fin = models.DateField(verbose_name='Date de fin')
    heure_fin = models.TimeField(verbose_name='Heure de fin')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Client')
    client_anonyme = models.BooleanField(default=False, verbose_name='Client anonyme')

    def __str__(self):
        if self.client_anonyme:
            return f'{self.chambre} - Anonyme'
        else:
            return f'{self.chambre} - {self.client}'

    class Meta:
        verbose_name = 'Affectation de chambre'
        verbose_name_plural = 'Affectations de chambres'

        
    @classmethod
    def nombre_reservations_jour(cls):
        maintenant = timezone.now()
        fin_jour = maintenant.replace(hour=23, minute=59, second=59)
        return cls.objects.filter(
            date_debut__lte=fin_jour,
            date_fin__gte=maintenant.date(),
        ).count()

    @classmethod
    def nombre_reservations_semaine(cls):
        maintenant = timezone.now()
        debut_semaine = maintenant - timedelta(days=maintenant.weekday())
        fin_semaine = debut_semaine + timedelta(days=6)
        return cls.objects.filter(
            date_debut__range=(debut_semaine, fin_semaine),
        ).count()

    @classmethod
    def nombre_reservations_mois(cls):
        maintenant = timezone.now()
        debut_mois = maintenant.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        dernier_jour_mois = calendar.monthrange(maintenant.year, maintenant.month)[1]
        fin_mois = maintenant.replace(day=dernier_jour_mois, hour=23, minute=59, second=59)
        return cls.objects.filter(
            date_debut__range=(debut_mois, fin_mois),
        ).count()

    @classmethod
    def nombre_total_reservations(cls):
        return cls.objects.count()


class PiecesJointes(models.Model):
    titre = models.CharField(max_length=255, verbose_name='Titre de la pièce jointe' , null=True, blank=True,)
    contenu = models.TextField(verbose_name='Contenu de la pièce jointe' , null=True, blank=True,)
    piece_jointe = models.FileField(upload_to='pieces_jointes/', null=True, blank=True, verbose_name='Pièce jointe')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')


    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = "Ajouter des pièces joints"
        verbose_name_plural = "Ajouter des pièces joints"



class Notification(models.Model):
    nom_notification = models.CharField(max_length=255)
    date_notification = models.DateField()
    heure_notification = models.TimeField()

    def __str__(self):
        return self.nom_notification
    
