from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages


# Create your views here.
def cart(request):
  # to get the cart
  cart = Cart(request)
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()

  return render (request, 'cart.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals})


def cart_add(request):
  #get the cart
  cart = Cart(request)

  #test for post
  if request.POST.get('action') == 'post':
    # get the products
    product_id = int(request.POST.get('product_id'))

    # get the product quantity
    product_qty =  int(request.POST.get('product_qty'))


    # lookup product in database
    product = get_object_or_404(Product, id=product_id)

    # save to session
    cart.add(product= product, quantity = product_qty )

    # get cart quantity
    # cart_quantity =  cart.__len__()
    cart_quantity =  len(cart)

    #return response for json
    # response = JsonResponse({'product_name: ': product.name})
    response =  JsonResponse({'qty': cart_quantity})
    messages.success(request, ("Product added to cart...."))
    return response

 




def cart_delete(request):
  cart = Cart(request)

  #test for post
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))

    # Call delete function in cart
    cart.remove(product = product_id)
    messages.success(request, ("Product removed from the cart...."))
    return JsonResponse({'product':product_id})






def cart_update(request):
  cart = Cart(request)

  #test for post
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    product_qty =  int(request.POST.get('product_qty'))

    # calling update function
    cart.update(product=product_id, quantity=product_qty)

    response =  JsonResponse({'qty':product_qty})
    messages.success(request, ("Item Quantity Updated.."))
    return response

 