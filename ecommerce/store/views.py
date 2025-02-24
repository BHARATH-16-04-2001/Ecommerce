from django.shortcuts import render, redirect
from . models import Product, Category, Profile
# for login and logout
from django.contrib.auth import authenticate, login, logout
# to display the message when loged in or logedout
from django.contrib import messages
from . forms import * 
import json
from django.db.models import Q
from cart.cart import Cart

# Create your views here.
def home(request):
  products = Product.objects.all()
  return render(request, 'home.html', {'products':products})


def about(request):
  return render(request, 'about.html') 


def product(request, pk):
  product = Product.objects.get(id=pk)
  return render(request, 'product.html', {'product':product})

def category_summary(request):
  categories = Category.objects.all()
  return render(request, 'category_summary.html', {'categories':categories})


def category(request, foo):
  # to raplace "-" with " " spaces in urls
  foo = foo.replace("-", " ")

  try:
    category = Category.objects.get(name = foo)
    products = Product.objects.filter(category = category)
    return render(request, 'category.html', {'products':products, 'category': category})
  except Exception:
    messages.success(request, "Category not exists ...")
    return redirect('home')
  


def login_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)

    if user is not None:
      login(request, user)

      # Shopping cart stuff
      current_user = Profile.objects.get(user__id=request.user.id)
      
      # get the items saved in the cart
      saved_cart = current_user.old_cart

      #covert databse string to python dictionary
      if saved_cart:
        # convert to dict using json
        converted_cart = json.loads(saved_cart)
        # add loaded dict to session
        cart = Cart(request)
        # loop through the cart and add item from db
        for key, value in converted_cart.items():
          cart.db_add(product=key, quantity=value)


      messages.success(request, "Logged In successfull...")
      return redirect('home')
    else:
      messages.success(request, "Please try again")
      return redirect('login')
  else:
    return render(request, 'login.html')
  

def logout_user(request): 
  logout(request)
  messages.success(request, "Loged out successfully..! Thanks for shopping")
  return redirect('home')


def register_user(request):
  form = SignUpForm()

  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']

      #login user
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, "You have been Register Sucessfully...")
      return redirect('update_info')
    else:
      messages.success(request, 'Please Register again with valid creditionals')
      return redirect('register')
  else:
    return render(request, 'register.html', {'form':form})
  


def update_user(request):
  if request.user.is_authenticated:
    current_users = User.objects.get(id=request.user.id)
    user_form = UpdateProfileForm(request.POST or None, instance=current_users)

    if user_form.is_valid():
      user_form.save() 

      login(request, current_users)
      messages.success(request, "User has been updated..!")
      return redirect('home')
    return render(request, 'update_user.html',{'user_form':user_form})
  else:
    messages.success(request,"You must be log in to access the page...")
    return redirect('home')

def update_password(request):
  if request.user.is_authenticated:
    current_user = request.user
    
    # did they filled the form
    if request.method == 'POST':
      form = ChangePasswordForm(current_user, request.POST) 

      #Is the form is vaild
      if form.is_valid():
        form.save()
        messages.success(request, "Your password is updated...")
        login(request, current_user)
        return redirect('login')
      else:
        for error in list(form.errors.values()):
          messages.error(request, error)
          return redirect('update_password')
    else: 
      form  = ChangePasswordForm(current_user)
      return render(request, 'update_password.html', {'form':form})
    
  else:
    messages.success(request, "You must logged in to view the page")
    return redirect('home')
  

def update_info(request):
  if request.user.is_authenticated:
    current_users = Profile.objects.get(user__id=request.user.id)
    # current_users, created = Profile.objects.get_or_create(user=request.user)
    form = UserInfoForm(request.POST or None, instance=current_users)

    if form.is_valid():
      form.save() 
      messages.success(request, "Your info has been updated..!")
      return redirect('home')
    return render(request, 'update_info.html',{'user_form':form})
  else:
    messages.success(request,"You must be log in to access the page...")
    return redirect('home')


def search(request):
  # if they filled the form
  if request.method == 'POST':
    searched = request.POST['searched']

    # Query the products  DB models
    searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains=searched))

    # Test for null
    if not searched:
      messages.success(request, "The Product is doesn't exists ...Please try again..")
      return render(request, 'search.html', {})
    else:
      return render(request, 'search.html', {'searched':searched})
  else:
    return render(request, 'search.html', {})