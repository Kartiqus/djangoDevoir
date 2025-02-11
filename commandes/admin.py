from django.contrib import admin
from .models import Categorie, Plat, Client, Commande

# Admin pour le modèle Categorie
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')  # Champs à afficher dans la liste
    search_fields = ('nom',)  # Permet la recherche par nom
    ordering = ('nom',)  # Tri par nom

# Admin pour le modèle Plat
class PlatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'stock')  # Champs à afficher dans la liste
    search_fields = ('nom', 'categorie__nom')  # Recherche par nom et catégorie
    list_filter = ('categorie',)  # Permet de filtrer par catégorie
    ordering = ('nom',)  # Tri par nom

# Admin pour le modèle Client
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'email')  # Champs à afficher dans la liste
    search_fields = ('nom', 'email')  # Recherche par nom et email
    ordering = ('nom',)  # Tri par nom

# Admin pour le modèle Commande
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('client', 'plat', 'quantite', 'montant_total', 'status_commande','status_livraison', 'date_commande')  # Champs à afficher dans la liste
    search_fields = ('client__nom', 'plat__nom')  # Recherche par client ou plat
    list_filter = ('status_commande','status_livraison')  # Permet de filtrer par statut de la commande
    ordering = ('date_commande',)  # Tri par date de commande
    readonly_fields = ('montant_total',)  # Champ montant_total est en lecture seule

# Enregistrement des classes Admin
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Plat, PlatAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Commande, CommandeAdmin)
