from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
# Create your models here.


class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)     #models.CASCADE = bilamana kita delete category, produk yg attach ngan category pon akan terdelete sekali
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])  #sef=product...category=category line 14 tu...slug= dlug line 8 dalam FILE models.py bawah FOLDER category

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True) # this fx will return color

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True) #This fx will return sizes

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #kita pilih ForeignKey sebab nanti kita nak create VARIATION untuk produk nye.......CASCADE ni once PRODUCT was delete, VARIATION also will be delete
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)  #choices=variation_category_choice ni yg akan jadi dropdown list at ADMIN PANEL
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)    #default=True.....by defaoult , the VARIATION will ACTIVE
    created_date       = models.DateTimeField(auto_now=True)

    objects = VariationManager() #nak bagitau model yang kita dah create VariationManager dalam model ni

    def __str__(self): #-----------NAK BUAT STRING----------
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
