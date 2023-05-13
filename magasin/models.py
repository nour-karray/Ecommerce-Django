from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Product(models.Model):
    TYPE_CHOICES = [
        ('em', 'Emballé'),
        ('fr', 'Frais'),
        ('cs', 'Conservé')
    ]
    label = models.CharField(max_length=100)
    description = models.TextField(default='Non defini')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(blank=True,upload_to='media/')
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, null=True)
    fournisseur=models.ForeignKey('Fournisseur',on_delete=models.CASCADE,null=True) 

    def __str__(self):
        return f"{self.label} ({self.type}): {self.price} €"
class Categorie(models.Model):
    TYPE_CHOICES=[('AL','Alimentaire'),
                  ('Mb','Meuble'),
                  ('Sn','Sanitaire'),
                  ('Vs','Vaisselle'),
                  ('Vt','Vêtement'),
                  ('Jx','Jouets'),
                  ('Lg','Linge de Maison'),
                  ('Bj','Bijoux'),
                  ('Dc','Décor')
                  
                  ]
    name=models.CharField(max_length=50,default='Al',choices=TYPE_CHOICES)
    

    def __str__(self):
        return self.name
class Fournisseur(models.Model):
    nom=models.CharField(max_length=100)
    adresse=models.TextField(null=True)
    email=models.EmailField(null=True)
    telephone=models.CharField(max_length=8)

    def __str__(self):
        return (self.nom+','+self.adresse+','+self.email+','+self.telephone)
    
    

    def __str__(self):
        return (self.nom+','+self.adresse+','+self.email+','+self.telephone)
    
class ProduitNC(Product):
    Duree_garantie=models.CharField(max_length=100)
    def __str__(self):
        return "objet ProduitNC:%s"%(self.Duree_garantie)

class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField('Product')
def __str__(self):
        return str(self.dateCde) + ' - ' + str(self.totalCde)
class ProduitNC(Product):
    Duree_garantie=models.CharField(max_length=100)
    
    def __str__(self):
        return "objet ProduitNC:%s"%(self.Duree_garantie)

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
