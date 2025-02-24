from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create customer profile
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  date_modified = models.DateTimeField(User, auto_now=True )
  phone  = models.CharField(max_length=20, blank=True)
  address1 = models.CharField(max_length=200, blank=True)
  address2 = models.CharField(max_length=200, blank=True)
  city  = models.CharField(max_length=50, blank=True)
  state = models.CharField(max_length=50, blank=True)
  zipcode = models.CharField(max_length=200, blank=True)
  country = models.CharField(max_length=50, blank=True)
  old_cart = models.CharField(max_length=50, blank=True, null=True)

  def __str__(self):
    return self.user.username
  

# create a user profile by default when user sign up
def create_profile(sender, instance, created, **kwargs):
  if created:
    user_profile = Profile(user = instance)
    user_profile.save()

# to automate the profile stuff
post_save.connect(create_profile, sender = User)    


# This is model for Catagories.
class Category(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name
  
  # for renaming the name of the models
  class Meta:
    verbose_name_plural = 'categories'

# This is model for Customers.
class Customer(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  phone = models.CharField(max_length=10)
  email = models.EmailField(max_length=100)
  password = models.CharField(max_length=100)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'
  

# This is model for Products in the website.
class Product(models.Model):
  name = models.CharField(max_length=100)
  price = models.DecimalField(default=0,decimal_places=2, max_digits=6)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
  description = models.CharField(max_length=250, default='', blank=True, null=True)
  image =  models.ImageField(upload_to ='uploads/product/')

  # add sales stuff
  is_sales = models.BooleanField(default=False)
  sale_price =  models.DecimalField(default=0,decimal_places=2, max_digits=6)

  def __str__(self):
    return self.name

#customer Orders
class Order(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  address = models.CharField(max_length=150 ,default='', blank=True, null=True)
  phone = models.CharField(max_length=20,default='', blank=True, null=True)
  date = models.DateField(default=datetime.datetime.today)
  status = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.product}'