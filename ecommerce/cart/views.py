from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def cart(request):
  # to get the cart
  cart = Cart(request)
  cart_products = cart.get_prods
  quantities = cart.get_quants

  return render (request, 'cart.html', {'cart_products':cart_products, 'quantities':quantities})


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

    return response

 




def cart_delete(request):
  pass






def cart_update(request):
  cart = Cart(request)
  
  #test for post
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    product_qty =  int(request.POST.get('product_qty'))

    # calling update function
    cart.update(product=product_id, quantity=product_qty)

    response =  JsonResponse({'qty':product_qty})
    return response

 