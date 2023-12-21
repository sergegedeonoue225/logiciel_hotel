# Generated by Django 4.2.7 on 2023-12-18 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAdministratif',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('profile_image', models.TextField(blank=True, max_length=100, null=True)),
                ('matricule', models.CharField(max_length=255, verbose_name='Matricule')),
                ('nom_prenom', models.CharField(max_length=255, verbose_name='Nom et Prénoms')),
                ('date_naissance', models.DateField(verbose_name='Date de naissance')),
                ('lieu_naissance', models.CharField(max_length=255, verbose_name='Lieu de naissance')),
                ('nationalite', models.CharField(max_length=255, verbose_name='Nationalité')),
                ('numero_cni', models.CharField(max_length=255, verbose_name='Numéro CNI')),
                ('adresse', models.CharField(max_length=255, verbose_name="Lieu d'habitation")),
                ('contacts', models.CharField(max_length=255, verbose_name='Numéro de téléphone')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Email')),
                ('fonction', models.CharField(max_length=255, verbose_name='Fonction')),
                ('date_entree', models.DateField(verbose_name="Date d'entrée")),
                ('salaire', models.IntegerField(blank=True, null=True, verbose_name='Salaire')),
                ('numero_cnps', models.CharField(blank=True, max_length=255, null=True, verbose_name='Numéro CNPS')),
                ('sit_matrimoniale', models.CharField(max_length=255, verbose_name='Situation matrimoniale')),
                ('nbe_enft', models.PositiveIntegerField(verbose_name="Nombre d'enfant")),
                ('nom_prenom_conjoint', models.CharField(max_length=255, verbose_name='Nom et Prénom du conjoint')),
                ('profession_conjoint', models.CharField(max_length=255, verbose_name='Profession du conjoint')),
                ('contact_conjoint', models.CharField(max_length=255, verbose_name='Contact du conjoint')),
                ('nom_prenom_pere', models.CharField(max_length=255, verbose_name='Nom et Prénom du père')),
                ('nom_prenom_mere', models.CharField(max_length=255, verbose_name='Nom et Prénom de la mère')),
                ('piece_identite_recto', models.TextField(blank=True, max_length=100, null=True, verbose_name="Pièce d'identité - Recto")),
                ('piece_identite_verso', models.TextField(blank=True, max_length=100, null=True, verbose_name="Pièce d'identité - Verso")),
                ('personne_urgence_contact', models.CharField(blank=True, max_length=255, null=True, verbose_name="Personne à contacter en cas d'urgence")),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Administratif',
                'verbose_name_plural': 'historical Administratifs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Administratif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('matricule', models.CharField(max_length=255, verbose_name='Matricule')),
                ('nom_prenom', models.CharField(max_length=255, verbose_name='Nom et Prénoms')),
                ('date_naissance', models.DateField(verbose_name='Date de naissance')),
                ('lieu_naissance', models.CharField(max_length=255, verbose_name='Lieu de naissance')),
                ('nationalite', models.CharField(max_length=255, verbose_name='Nationalité')),
                ('numero_cni', models.CharField(max_length=255, verbose_name='Numéro CNI')),
                ('adresse', models.CharField(max_length=255, verbose_name="Lieu d'habitation")),
                ('contacts', models.CharField(max_length=255, verbose_name='Numéro de téléphone')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('fonction', models.CharField(max_length=255, verbose_name='Fonction')),
                ('date_entree', models.DateField(verbose_name="Date d'entrée")),
                ('salaire', models.IntegerField(blank=True, null=True, verbose_name='Salaire')),
                ('numero_cnps', models.CharField(blank=True, max_length=255, null=True, verbose_name='Numéro CNPS')),
                ('sit_matrimoniale', models.CharField(max_length=255, verbose_name='Situation matrimoniale')),
                ('nbe_enft', models.PositiveIntegerField(verbose_name="Nombre d'enfant")),
                ('nom_prenom_conjoint', models.CharField(max_length=255, verbose_name='Nom et Prénom du conjoint')),
                ('profession_conjoint', models.CharField(max_length=255, verbose_name='Profession du conjoint')),
                ('contact_conjoint', models.CharField(max_length=255, verbose_name='Contact du conjoint')),
                ('nom_prenom_pere', models.CharField(max_length=255, verbose_name='Nom et Prénom du père')),
                ('nom_prenom_mere', models.CharField(max_length=255, verbose_name='Nom et Prénom de la mère')),
                ('piece_identite_recto', models.FileField(blank=True, null=True, upload_to='pieces_identite/', verbose_name="Pièce d'identité - Recto")),
                ('piece_identite_verso', models.FileField(blank=True, null=True, upload_to='pieces_identite/', verbose_name="Pièce d'identité - Verso")),
                ('personne_urgence_contact', models.CharField(blank=True, max_length=255, null=True, verbose_name="Personne à contacter en cas d'urgence")),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Administratif',
                'verbose_name_plural': 'Administratifs',
            },
        ),
    ]