from store. models import Product, Profile

class Cart():
  def __init__(self, request):
    self.session =  request.session

    # to get request
    self.request = request

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

    # deal with loged in user
    if self.request.user.is_authenticated:
      # get the current user profile
      current_user = Profile.objects.filter(user__id=self.request.user.id) 
      #{'3':1, '2':3} to {"3":1, "2":3}
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      # to save the carty
      current_user.update(old_cart = str(carty))




  def db_add(self, product, quantity):
    product_id = str(product)
    product_qty = str(quantity)

    if product_id in self.cart:
      pass
    else: 
      # self.cart[product_id] =  {'price':str(product.price)}
      self.cart[product_id]  = int(product_qty)

    self.session.modified = True

    # deal with loged in user
    if self.request.user.is_authenticated:
      # get the current user profile
      current_user = Profile.objects.filter(user__id=self.request.user.id) 
      #{'3':1, '2':3} to {"3":1, "2":3}
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      # to save the carty
      current_user.update(old_cart = str(carty))


  


  def cart_total(self):
    product_ids = self.cart.keys()
    # lookup those keys in product database model
    products = Product.objects.filter(id__in = product_ids)
    # to get quantities
    quants = self.cart
    # start count from 0
    total = 0

    for key, value in quants.items():
      # convert key string to integer
      key = int(key)
      for product in products:
        if product.id == key:
          if product.is_sales:
            total += (product.sale_price * value)
          else:
            total += (product.price * value)

    return total

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

  
     # deal with loged in user
    if self.request.user.is_authenticated:
      # get the current user profile
      current_user = Profile.objects.filter(user__id=self.request.user.id) 
      #{'3':1, '2':3} to {"3":1, "2":3}
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      # to save the carty
      current_user.update(old_cart = str(carty))

    thing = self.cart
    return thing
  


  def remove(self, product):
    product_id = str(product)  ##--  because the "id" in the dictionary is in string

    # delete from dictionary / cart
    if product_id in self.cart:
      del self.cart[product_id]

    self.session.modified = True 

     # deal with loged in user
    if self.request.user.is_authenticated:
      # get the current user profile
      current_user = Profile.objects.filter(user__id=self.request.user.id) 
      #{'3':1, '2':3} to {"3":1, "2":3}
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      # to save the carty
      current_user.update(old_cart = str(carty))
  
