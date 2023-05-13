from rest_framework.serializers import ModelSerializer
 
from magasin.models import Categorie
from magasin.models import Product
class CategorySerializer(ModelSerializer):
 
    class Meta:
        model = Categorie
        fields = ['id', 'name']
        
class ProduitSerializer(ModelSerializer):
    model = Product
    fields = ['id', 'name', 'description', 'id_categorie']