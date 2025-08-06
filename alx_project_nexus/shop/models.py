from django.db import models, transaction
import requests

class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    @transaction.atomic
    def disable(self):
      if self.active is False:
        return
      self.active = False
      self.save()
      self.products.update(active=False)

    def __str__(self):
        return self.name


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    @transaction.atomic
    def disable(self):
      if self.active is False:
        return
      self.active = False
      self.save()
      self.articles.update(active=False)
    
    def call_external_api(self, method, url):
       #l'appel doit etre le plus petit possible car appliquer un mock va 
       #va reduire la couverture de tests
       #c'est cette methode qui va etre monkey patchee
       return requests.request(method, url)
    
    @property
    def ecoscore(self):
       # Nous realisons l'appel a open food fact
       response = self.call_external_api('GET', 'https://world.openfoodfacts.org/api/v0/product/3229820787015.json')
       if response.status_code == 200:
          # et renvoyons l'ecoscore que si la reponse est vailde
          return response.json()['product']['ecoscore_grade']

    def __str__(self):
        return self.name
    


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name
