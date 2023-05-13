from django.forms import ModelForm
from django import forms
from .models import Product
from .models import Fournisseur 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Fournisseur ,Commande,Categorie
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory


class ProduitForm(ModelForm): 
    class Meta : 
        model = Product 
        fields = "__all__" #pour tous les champs de la table
#fields=['libelle','description'] #pour qulques champs
class FournisseurForm(ModelForm):
     class Meta : 
        model = Fournisseur
        fields = "__all__" #pour tous les champs de la table
        #fields=['libellé','description']  #pour qulques champs
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom')
    last_name = forms.CharField(label='Nom')
    email = forms.EmailField(label='Adresse e-mail')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email')


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = "__all__" 
        widgets = {
          'produits': forms.CheckboxSelectMultiple()
        }

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = "__all__" 

class ProduitForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"  # pour tous les champs de la table
        # fields=['libellé','description']  #pour qulques champs





