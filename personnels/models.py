from django.db import models

class Personnel(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('Autre', 'Autre'),
    ]

    POSTE_CHOICES = [
        ('Receptionniste', 'Réceptionniste'),
        ('Concierge', 'Concierge'),
        ('Service de chambre', 'Service de chambre'),
        ('Gestionnaire', 'Gestionnaire'),
        ('Autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('Actif', 'Actif'),
        ('Inactif', 'Inactif'),
        ('En congé', 'En congé'),
        ('Autre', 'Autre'),
    ]

    nom_prenom = models.CharField(max_length=50, verbose_name='Nom')
    date_naissance = models.DateField(verbose_name='Date de naissance')
    nationalite = models.CharField(max_length=255, verbose_name="Nationalité")
    lieu_naissance = models.CharField(max_length=255, verbose_name="Lieu de naissance")
    numero_cni = models.CharField(max_length=255, verbose_name="Numéro CNI")
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, verbose_name='Genre')
    poste = models.CharField(max_length=50, choices=POSTE_CHOICES, verbose_name='Poste')
    date_embauche = models.DateField(verbose_name='Date d\'embauche')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, verbose_name='Statut')
    adresse = models.TextField(verbose_name='Adresse')
    telephone = models.CharField(max_length=15, verbose_name='Téléphone')
    email = models.EmailField(verbose_name='Adresse e-mail')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  
    piece_identite_recto = models.FileField(upload_to='pieces_identite/', null=True, blank=True, verbose_name="Pièce d'identité - Recto")
    piece_identite_verso = models.FileField(upload_to='pieces_identite/', null=True, blank=True, verbose_name="Pièce d'identité - Verso")

    def __str__(self):
        return f' {self.nom_prenom} - {self.poste}'

    class Meta:
        verbose_name = 'Personnel'
        verbose_name_plural = 'Personnel'
