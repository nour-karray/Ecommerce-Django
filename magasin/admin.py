from django.contrib import admin

from .models import Product, Categorie , Fournisseur , ProduitNC, Commande ,Customer,Order,OrderItem,ShippingAddress
admin.site.register(Product)
admin.site.register(Categorie)
admin.site.register(Fournisseur)
admin.site.register(ProduitNC)
admin.site.register(Commande)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# Register your models here.
