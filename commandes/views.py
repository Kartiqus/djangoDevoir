from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from .models import Commande, Plat, Client, Categorie
from django.contrib import messages
from .forms import *

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.middleware.csrf import get_token

# Assuming Commande model is defined elsewhere
# from .models import Commande


@require_POST
def changer_statut_commande(request, commande_id, nouveau_statut):
    commande = get_object_or_404(Commande, id=commande_id)
    if nouveau_statut in dict(Commande.STATUT_CHOICES):
        commande.status_commande = nouveau_statut
        commande.save()
        return JsonResponse({
            'success': True,
            'message': f"Le statut de la commande a été changé en '{commande.get_status_commande_display()}'.",
            'new_status': nouveau_statut,
            'new_status_display': commande.get_status_commande_display()
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "Statut invalide."
        }, status=400)



def changer_statut_commande(request, commande_id, nouveau_statut):
    commande = get_object_or_404(Commande, id=commande_id)
    if nouveau_statut in dict(Commande.STATUT_CHOICES):
        commande.status_commande = nouveau_statut
        commande.save()
        messages.success(request, f"Le statut de la commande a été changé en '{commande.get_status_commande_display()}'.")
    else:
        messages.error(request, "Statut invalide.")
    return redirect('liste_commandes')

def creer_plat(request):
    if request.method == "POST":
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le plat a été ajouté avec succès.")
            return redirect('plats/')
        else:
            messages.error(request, "Il y a eu une erreur. Veuillez vérifier le formulaire.")
    else:
        form = PlatForm()

    categories = Categorie.objects.all()
    return render(request, 'plats/ajouter.html', {'form': form, 'categories': categories})

def index(request):
    return render(request, 'index.html')
def liste_plats(request):
    # Récupérer tous les plats avec un stock > 0
    plats = Plat.objects.filter(stock__gt=0)
    
    context = {
        'plats': plats
    }
    
    return render(request, 'plats/index.html', context)

def liste_commandes(request):
    """ Affiche la liste des commandes """
    commandes = Commande.objects.all().order_by('-date_commande')
    return render(request, "commandes/liste_commandes.html", {"commandes": commandes})


def creer_commande(request):
    """ Vue pour enregistrer une nouvelle commande """
    plats = Plat.objects.filter(stock__gt=0)
    
    if request.method == "POST":
        client_nom = request.POST.get("client_nom")
        plat_id = request.POST.get("plat")
        quantite = int(request.POST.get("quantite"))
        status_livraison = request.POST.get("status_livraison") == "on"

        if not client_nom or not plat_id or quantite <= 0:
            messages.error(request, "Veuillez remplir tous les champs correctement.")
            return redirect("creer_commande")

        plat = Plat.objects.get(id=plat_id)

        if plat.stock < quantite:
            messages.error(request, "Stock insuffisant pour ce plat.")
            return redirect("creer_commande")

        # Vérifier si le client existe déjà ou le créer
        client, created = Client.objects.get_or_create(nom=client_nom)

        # Création de la commande
        commande = Commande.objects.create(
            client=client,
            plat=plat,
            quantite=quantite,
            status_livraison=status_livraison
        )

        messages.success(request, "Commande enregistrée avec succès.")
        return redirect("liste_commandes")

    return render(request, "commandes/creer_commande.html", {"plats": plats})
