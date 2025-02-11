from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path("commandes/", views.liste_commandes, name="liste_commandes"),
    path("commandes/nouvelle/", views.creer_commande, name="creer_commande"),
    path('commandes/changer-statut/<int:commande_id>/<str:nouveau_statut>/', views.changer_statut_commande, name='changer_statut_commande'),
    path("plats/nouveau/", views.creer_plat, name="creer_plat"),
    path('', views.liste_plats, name='plats'),
    path('plats/', views.liste_plats, name='plats'),

]

