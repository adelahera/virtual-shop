from django.http import HttpResponse
from . import consultas
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from pymongo import MongoClient
import sys
import re
import random
import logging
from .forms import ProductForm
from . import Seed

client = Seed.BaseDatos()

logger = logging.getLogger(__name__)

def index(request):

    p=client.productos.find()
    prods=list(p)
    if len(prods) >= 3:
        productos = random.sample(prods, 3)
    else:
        productos = random.sample(prods, len(prods))

    context = {
        'productos': productos
    }

    return render(request, "shop/index.html", context)

def buscar(request):

    busqueda = request.GET.get('busqueda', 'No items found')
    regex = re.compile(f".*{re.escape(busqueda)}.*", re.IGNORECASE)
    p=client.productos.find({"title": regex})
    productos=list(p)

    context={
        'busqueda' : busqueda,
        'productos' : productos,
    }
    return render(request, "shop/busqueda.html", context)

def busq_cat(request, busqueda):

    p = client.productos.find({"category": busqueda})
    productos = list(p) 

    context={
        'busqueda': busqueda,
        'productos': productos
    }
    return render(request, "shop/categorias.html", context)

@login_required
def añadir(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        logger.info("Form is POST")
        if form.is_valid():            
            logger.info("Form is valid")
            data = form.cleaned_data
            if 'image' in request.FILES:
                imagen = request.FILES['image']
                with open(f'static/imagenes/{imagen.name}', 'wb+') as destination:
                    for chunk in imagen.chunks():
                        destination.write(chunk)
                # guarda la ruta de la imagen en el campo image del form
                data['image'] = imagen.name

            logger.debug(data)
            client.tienda.productos.insert_one(data)
            messages.success(request, 'Product added successfully')
            return redirect('index')
        else:
            logger.info("Form is not valid")
            logger.error(form.errors)
            messages.error(request, 'Error adding product')

    else:
        form = ProductForm()

    context={
        'form': form,
    }

    return render(request, "shop/añadir.html", context)

def salir(request):
    logout(request)
    logger.info("User logged out")
    messages.success(request, 'Logged out successfully')
    return redirect('index')

# def consulta_1(request):
#     consulta = consultas.electronics_between_100_and_200()
#     return render(request, "shop/products_list.html", {"consulta":consulta})

# def consulta_2(request):
#     consulta = consultas.products_containing_word_pocket()
#     return render(request, "shop/products_list.html", {"consulta":consulta})

# def consulta_3(request):
#     consulta = consultas.products_with_rating_above_4()
#     return render(request, "shop/products_list.html", {"consulta":consulta})

# def consulta_4(request):
#     consulta = consultas.mens_clothing_sorted_by_rating()
#     return render(request, "shop/products_list.html", {"consulta":consulta})

# def consulta_5(request):
#     consulta = consultas.total_revenue()
#     return HttpResponse(consulta)

# def consulta_6(request):
#     consulta = consultas.revenue_by_category()
#     return HttpResponse(consulta)