from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order)


# Create Order item inline
class OrderItemInline(admin.StackedInline):
  model = OrderItem
  extra = 0
  


#extend order model
class OrderAdmin(admin.ModelAdmin):
  model = Order
  readonly_fields = ["date_ordered"]
  fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "shipped_date"]
  inlines = [OrderItemInline]
 

# unregister the order model
admin.site.unregister(Order)

# Re register the order model and orderitem
admin.site.register(Order, OrderAdmin)