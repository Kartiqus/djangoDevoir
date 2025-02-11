from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Plat(models.Model):
    nom = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="plats/", blank=True, null=True)

    def __str__(self):
        return self.nom


class Client(models.Model):
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.nom


class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    status_commande = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date_commande = models.DateTimeField(auto_now_add=True)
    status_livraison = models.BooleanField(
        default=False, 
        verbose_name="Type de commande",
        help_text="Cochez si la commande est sur place, sinon elle est livrée."
    )
    def save(self, *args, **kwargs):
        """ Vérifie le stock et calcule le montant total avant d'enregistrer. """
        if self.plat.stock < self.quantite:
            raise ValueError("Stock insuffisant pour ce plat.")

        self.montant_total = self.plat.prix * self.quantite
        super().save(*args, **kwargs)

        # Mise à jour du stock après l'enregistrement
        self.plat.stock -= self.quantite
        self.plat.save()

    def __str__(self):
        return f"{self.client.nom} - {self.plat.nom} ({self.quantite}) - {self.get_status_commande_display()}"
