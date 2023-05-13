from sre_parse import CATEGORIES
from django.shortcuts import redirect, render, get_object_or_404
from .models import Categorie,Product
from .models import Fournisseur, Commande
from .forms import CategorieForm , CommandeForm , UserRegistrationForm , FournisseurForm , ProduitForm 
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.models import Categorie
from magasin.serializers import CategorySerializer
from magasin.serializers import ProduitSerializer
from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
def index(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            list = Product.objects.all()
            return render(request, 'Produits/vitrineP.html', {'list': list})
    else:
        form = ProduitForm()  # créer formulaire vide
        list = Product.objects.all()
        return render(request, 'Produits/create_product.html', {'form': form, 'list': list})

def CreateProduct(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            products = Product.objects.all()
            return render(request, 'store/catalogue.html', {'products': products})
    else:
        form = ProduitForm()  # créer formulaire vide
        products = Product.objects.all()
        return render(request, 'store/create_product.html', {'form': form, 'products': products})
    

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            produit = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['img']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                produit.img = nouvelle_image
            # Sauvegarder le produit
            produit.save()
            return redirect('Catalogue')
    else:
        form = ProduitForm(instance=product)
        return render(request, 'Produits/edit_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('Catalogue')
    return render(request, 'Produits/delete_product.html', {'product': product})


def detail_product(request, product_id):
    produit = get_object_or_404(Product, id=product_id)
    context = {'produit': produit}
    return render(request, 'Produits/detail_product.html', context)


def Catalogue(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'Produits/mesProduits.html', context)

def CatalogueProduct(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/catalogue.html', context)


def indexA(request):
    return render(request, 'magasin/acceuil.html')

def ListFournisseur(request):
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'Fournisseurs/mesFournisseurs.html', context)


def nouveauFournisseur(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST, request.FILES)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            frns = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['logo']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                frns.logo = nouvelle_image
            # Sauvegarder le produit
            form.save()
            fournisseurs = Fournisseur.objects.all()
            return render(request, 'Fournisseurs/mesFournisseurs.html', {'fournisseurs': fournisseurs})
    else:
        form = FournisseurForm()  # créer formulaire vide
        fournisseurs = Fournisseur.objects.all()
        return render(request, 'Fournisseurs/create_For.html', {'form': form, 'fournisseurs': fournisseurs})
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


class ChangePasswordView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('home')


def edit_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        form = FournisseurForm(
            request.POST, request.FILES, instance=fournisseur)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            frns = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['logo']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                frns.logo = nouvelle_image
            # Sauvegarder le produit
            frns.save()
            return redirect('fournisseurs')
    else:
        form = FournisseurForm(instance=fournisseur)
        return render(request, 'Fournisseurs/edit_For.html', {'form': form})

def delete_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('fournisseurs')
    return render(request, 'Fournisseurs/delete_For.html', {'fournisseur': fournisseur})


def detail_Fournisseur(request, for_id):
    fournisseur = get_object_or_404(Fournisseur, id=for_id)
    context = {'fournisseur': fournisseur}
    return render(request, 'Fournisseurs/detail_For.html', context)


def create_commande(request):
    if request.method == "POST":
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            commandes = Commande.objects.all()

            return render(request, 'Commandes/mesCommandes.html', {'commandes': commandes})
    else:
        form = CommandeForm()  # créer formulaire vide
        commandes = Commande.objects.all()
        return render(request, 'Commandes/create_commande.html', {'form': form, 'commandes': commandes})


def edit_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            commande.save()
            return redirect('ListCommande')
    else:
        form = CommandeForm(instance=commande)
        return render(request, 'Commandes/edit_commande.html', {'form': form})


def delete_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('ListCommande')
    return render(request, 'Commandes/delete_commande.html', {'commande': commande})


def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    context = {'commande': commande}
    return render(request, 'Commandes/detail_commande.html', context)


def ListCommande(request):
    commandes = Commande.objects.all()
    context = {'commandes': commandes}
    return render(request, 'Commandes/mesCommandes.html', context)


def create_categorie(request):
       if request.method == "POST" :
         form = CategorieForm(request.POST)
         if form.is_valid():
              form.save() 
              categories=Categorie.objects.all()
              
              return render(request,'Categories/mesCategories.html',{'categories':categories})
       else : 
            form = CategorieForm() #créer formulaire vide 
            categories=Categorie.objects.all()
            return render(request,'Categories/create_categorie.html',{'form':form,'categories':categories})

def edit_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            categorie.save()
            return redirect('ListCategorie')
    else:
        form = CategorieForm(instance=categorie)
        return render(request, 'Categories/edit_categorie.html', {'form': form})


def delete_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('ListCategorie')
    return render(request, 'Categories/delete_categorie.html', {'categorie': categorie})


def detail_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    context = {'categorie': categorie}
    return render(request, 'Categories/detail_categorie.html', context)

def ListCategorie(request):
    categories = Categorie.objects.all()
    context = {'categories': categories}
    return render(request, 'Categories/mesCategories.html', context)

class CategoryAPIView(APIView):
 
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

class ProduitListAPIView(APIView):
    def get(self, request):
        produits = Product.objects.filter(id__in=[1, 2, 3])
        serializer = ProduitSerializer(produits, many=True)

        return Response(serializer.data)
class ProductViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProduitSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
def search(request):
    query = request.GET.get('q')
    if query:
        produits = Product.objects.filter(label__icontains=query)
        context = {'query': query, 'produits': produits}
        return render(request, 'magasin/search_results.html', context)
    else:
        return render(request, 'magasin/search_results.html')

