from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
from io import BytesIO
from utilisateurs.models import Utilisateurs
from django.templatetags.static import static
from django.db.models import Sum
from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum
from xhtml2pdf import pisa
import base64
from io import BytesIO

from django.db import models

import base64


class PDFView_liste_utilisateurs(View):
    def get(self, request, *args, **kwargs):
        # Récupérer la liste des utilisateurs
        utilisateurs = Utilisateurs.objects.all()

        # Récupérer le chemin du logo
        logo_path = ('logo.png')

        # Convertir le logo en base64
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Créer un objet BytesIO pour stocker le PDF
        pdf_data = BytesIO()

        # Récupérer le template HTML
        template_path = 'pdf_liste_utilisateur.html'
        template = get_template(template_path)

        # Contexte pour le rendu du template
        context = {'utilisateurs': utilisateurs, 'logo_base64': logo_base64}

        # Rendre le template au format HTML
        html = template.render(context)

        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="liste_utilisateurs.pdf"'

        # Utiliser pisa pour générer le PDF
        pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

        # S'assurer que la génération du PDF s'est déroulée correctement
        if pisa_status.err:
            return HttpResponse("Erreur lors de la génération du PDF", status=500)

        return response       
    


class PDFView_liste_personnels(View):
    def get(self, request, *args, **kwargs):
        # Récupérer la liste des personnels
        personnels = personnels.objects.all()

        # Récupérer le chemin du logo
        logo_path = 'logo.png'

        # Convertir le logo en base64
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Créer un objet BytesIO pour stocker le PDF
        pdf_data = BytesIO()

        # Récupérer le template HTML
        template_path = 'pdf_liste_personnels.html'
        template = get_template(template_path)

        # Contexte pour le rendu du template
        context = {'personnels': personnels, 'logo_base64': logo_base64}

        # Rendre le template au format HTML
        html = template.render(context)

        # Créer le PDF avec orientation paysage
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="liste_personnels.pdf"'

        # Ajouter une balise de style pour l'orientation paysage
        html = f'<html><head><style type="text/css"> @page {{ size: landscape; }} </style></head><body>{html}</body></html>'

        # Utiliser pisa pour générer le PDF
        pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

        # S'assurer que la génération du PDF s'est déroulée correctement
        if pisa_status.err:
            return HttpResponse("Erreur lors de la génération du PDF", status=500)

        return response


