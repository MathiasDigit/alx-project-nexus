from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Category, Product, Article

User = get_user_model()

class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError('Price must be greater than 1')
        return value
    
    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Inactive product')
        return value


class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'ecoscore','articles']

    def get_articles(self, instance):
            queryset = instance.articles.filter(active=True)
            serializer = ArticleSerializer(queryset, many=True)
            return serializer.data

class ProductListSerializer(serializers.ModelSerializer):
     class Meta:
          model = Product
          fields = ['id', 'name', 'category', 'ecoscore']

class CategoryListSerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['id', 'name', 'description']

     def validate_name(self, value):
         # Nous verifions que la categories existe
         if Category.objects.filter(name=value).exists():
         # En cas d'erreur, DRF nous met a disposition l'exception validationError
            raise serializers.ValidationError('Category already exists')
         return value
     
     def validate(self, data):
     # Effectuons le controle sur la presence du nom dans la description
         if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
         return data

class CategoryDetailSerializer(serializers.ModelSerializer):

     # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits sont multiples pour une catégorie

    products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']
    
    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductDetailSerializer(queryset, many=True)
        return serializer.data
    


