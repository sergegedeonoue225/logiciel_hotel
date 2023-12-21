from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from guardian.mixins import GuardianUserMixin
from simple_history.models import HistoricalRecords


class Fonction(models.Model):
    nom_fonction = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField('Permission', related_name='fonctions', blank=True)

    def __str__(self):
        return self.nom_fonction

class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class UtilisateursManager(BaseUserManager):
    def create_user(self, email, fonction, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fonction=fonction, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Notez que nous ne passons pas la fonction ici
        return self.create_user(email, None, password, **extra_fields)

class Utilisateurs(AbstractBaseUser, PermissionsMixin, GuardianUserMixin):
    email = models.EmailField(unique=True)
    fonction = models.ForeignKey(Fonction, on_delete=models.CASCADE, null=True, blank=True)
    nom_complet = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    history = HistoricalRecords()
    action = models.CharField(max_length=255, null=True, blank=True)

  
    objects = UtilisateursManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Les admins et utilisateurs"
        verbose_name_plural = "Les admins et utilisateurs"



from utilisateurs.models import Utilisateurs

class RecentAction(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, related_name="recent_actions_utilisateurs") 
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.action} par {self.user.nom_complet} le {self.timestamp}"
