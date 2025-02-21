from store. models import Product

class Cart():
  def __init__(self, request):
    self.session =  request.session

    # Get current session key if it exists
    cart = self.session.get('session_key')

    #if user is new to website create session "no session key"
    if 'session_key' not in request.session:
      cart = self.session['session_key'] = {}

    # to make sure cart available in all pages of site
    self.cart = cart


  def add(self, product, quantity):
    product_id = str(product.id)
    product_qty = str(quantity)

    if product_id in self.cart:
      pass
    else: 
      # self.cart[product_id] =  {'price':str(product.price)}
      self.cart[product_id]  = int(product_qty)

    self.session.modified = True

  def __len__(self):
    return len(self.cart)
  

  def get_prods(self):
    # get id from the cart
    product_ids = self.cart.keys()

    # use id to lookup products in database model
    products = Product.objects.filter(id__in = product_ids)
    return products
  

  def get_quants(self):
    quantities = self.cart
    return quantities
  

  def update(self, product, quantity):
    product_id = str(product)
    product_qty = int(quantity)

    # to get cart   
    our_cart = self.cart

    # update dictionary {'2': 3}
    our_cart[product_id] = product_qty

    self.session.modified = True

    thing = self.cart
    return thing
