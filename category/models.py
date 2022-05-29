from django.db import models
from django.urls import reverse  #die reverse sebab Line 17 tu guna reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True )
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):                              #line 15 dan 16 bring us url bai setiap kategori
            return reverse('products_by_category', args=[self.slug]) #[self.slug]=category slug(line 7)

    def __str__(self):
        return self.category_name
