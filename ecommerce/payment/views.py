from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib import messages
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from payment.forms import ShippingFrom, PaymentForm
from store.models import Product

# Create your views here.
def payment_success(request):
  return render(request, "payment/payment_success.html", {})


def checkout(request):
  cart = Cart(request)
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()

  if request.user.is_authenticated:
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id) 
    shipping_form = ShippingFrom(request.POST or None, instance=shipping_user)

    return render (request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})

  else:
    # checkout as guest
    shipping_form = ShippingFrom(request.POST or None)

    return render (request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})


def billing_info(request):
  if request.POST:
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()


    # Create a session with shipping info
    my_shipping = request.POST
    request.session['my_shipping'] = my_shipping

    #check to see if user is logged in
    if request.user.is_authenticated:
      billing_form = PaymentForm()
      return render (request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
    else:
      billing_form = PaymentForm()
      return render (request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})

    shipping_form = request.POST
    return render (request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
  else:
    messages.success(request, "Access Denied")
    return redirect('home')
  

def proccess_order(request):
  if request.POST:
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    # fecthing billingg info form the last page(billing_info)
    payment_form = PaymentForm(request.POST or None)

    # get shipping session data
    my_shipping = request.session.get('my_shipping')

    # gather order info
    full_name = my_shipping['shipping_fullname']
    email = my_shipping['shipping_email']
    # create shippping addresss from session info
    shipping_address = f"{my_shipping['shipping_address1']}\n {my_shipping['shipping_address2']}\n {my_shipping['shipping_city']}\n {my_shipping['shipping_state']}\n {my_shipping['shipping_zipcode']}\n {my_shipping['shipping_country']}\n "
    amount_paid = totals

    # create order
    if request.user.is_authenticated:
      # logged in
      user = request.user
      create_order = Order(user = user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
      create_order.save()


    # add order item 
      # get order id
      order_id = create_order.pk
      # get product info
      for product in cart_products():
        #get product id
        product_id = product.id
        # get product price
        if product.is_sales:
          price = product.sale_price
        else:
          price = product.price

        # get quanity
        for key, value in quantities().items():
          if int(key) == product.id:
            create_order_item = OrderItem(order_id = order_id , product_id = product_id, user = user , quantity = value , price = price )
            create_order_item.save()

      messages.success(request, "Order Placed..")
      return redirect('home')
    else:
      # user not logged in
      create_order = Order( full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
      create_order.save()

      # order item
      order_id = create_order.pk
      # get product info
      for product in cart_products():
        #get product id
        product_id = product.id
        # get product price
        if product.is_sales:
          price = product.sale_price
        else:
          price = product.price

        # get quanity
        for key, value in quantities().items():
          if int(key) == product.id:
            create_order_item = OrderItem(order_id = order_id , product_id = product_id,  quantity = value , price = price )
            create_order_item.save()



      messages.success(request, "Order Placed..")
      return redirect('home')
   
  else:
    messages.success(request, "Access denied..")
    return redirect('home')
  return render(request, 'proccess_order', {})