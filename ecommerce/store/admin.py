from django.contrib import admin
from . models import Category,Customer, Order, Product, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)


# combine the user info and profile info
class ProfileInline(admin.StackedInline):
  model = Profile

# extend user model
class UserAdmin(admin.ModelAdmin):
  model = User
  fields = ["username", "first_name", "last_name", "email"]
  inlines = [ProfileInline]

# unregister the old way
admin.site.unregister(User)

# re-register the new one
admin.site.register(User, UserAdmin)