from django.shortcuts import render, redirect
from . models import Product, Category
# for login and logout
from django.contrib.auth import authenticate, login, logout
# to display the message when loged in or logedout
from django.contrib import messages
from . forms import *

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
      return redirect('home')
    else:
      messages.success(request, 'Please Register again with valid creditionals')
      return redirect('register')
  else:
    return render(request, 'register.html', {'form':form})