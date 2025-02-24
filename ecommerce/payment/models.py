from django.db import models
from django.contrib.auth.models import User
from store.models import Product


# Create your models here.
class ShippingAddress(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
  shipping_fullname = models.CharField(max_length=55)
  shipping_email = models.CharField(max_length=100)
  shipping_address1 = models.CharField(max_length=200)
  shipping_address2 = models.CharField(max_length=200, null=True, blank=True)
  shipping_city = models.CharField(max_length=25)
  shipping_state = models.CharField(max_length=30, null=True, blank=True)
  shipping_zipcode = models.CharField(max_length=15, null=True, blank=True)
  shipping_country = models.CharField(max_length=50)

  # To Remove pluralize address
  class Meta:
    verbose_name_plural = "Shipping Address"

  def __str__(self):
    return f"Shipping Address - {str(self.id)} "
  


# Create Order model
class Order(models.Model):
  # Foreign key
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  full_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=200)
  shipping_address = models.TextField(max_length=15000)
  amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
  date_orderd = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Order  -  {str(self.id)} " 


# Create Order Item Model
class OrderItem(models.Model):
  #Foreign keys
  order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

  quantity = models.PositiveBigIntegerField(default=1)
  price = models.DecimalField(max_digits=10, decimal_places=2)
 
  def __str__(self):
   return f"Order Item - {str(self.id)}"