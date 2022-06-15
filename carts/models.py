from django.db import models
from store.models import Product, Variation # sebab kita libatkan product, ini fungsinya nak panggil maklumat product daripada folder []store under file [=] models.py dia kene pang


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart   = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):    #create fx. untuk kira subtotal...proses subtotal ada kat [=]cart.html UNDER []store UNDER []templetes
        return self.product.price * self.quantity # * self = refer to "CartItem(models.Model)"....... product.price = refer  "product = models.ForeignKey.." & dalam product model "(Product, on_delete..." ada price

    def __unicode__(self):
        return self.product
