from django.http import HttpResponse
from . import consultas
from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient
import sys
import re
import random
import logging
from .forms import ProductForm

logger = logging.getLogger(__name__)

client = MongoClient('mongo', 27017)

def index(request):

    p=client.tienda.productos.find()
    prods=list(p)
    if len(prods) >= 3:
        productos = random.sample(prods, 3)
    else:
        productos = random.sample(prods, len(prods))

    for prod in productos:
        prod['image'] = prod.get('image').replace('https://fakestoreapi.com/img/','')

    context = {
        'productos': productos
    }

    logger.debug("Debug message")
    return render(request, "shop/index.html", context)

def buscar(request):

    busqueda = request.GET.get('busqueda', 'No items found')
    regex = re.compile(f".*{re.escape(busqueda)}.*", re.IGNORECASE)
    p=client.tienda.productos.find({"title": regex})
    productos=list(p)

    for prod in productos:
        prod['image'] = prod.get('image').replace('https://fakestoreapi.com/img/','')

    context={
        'busqueda' : busqueda,
        'productos' : productos,
    }
    return render(request, "shop/busqueda.html", context)

def busq_cat(request, busqueda):

    p = client.tienda.productos.find({"category": busqueda})
    productos = list(p)

    for prod in productos:
        prod['image'] = prod.get('image').replace('https://fakestoreapi.com/img/','')    

    context={
        'busqueda': busqueda,
        'productos': productos
    }
    return render(request, "shop/categorias.html", context)

def añadir(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            # client.tienda.productos.insert_one(data)
            logger.debug(form.cleaned_data)
            messages.success(request, 'Product added successfully')
            return redirect('index')

    else:
        form = ProductForm()

    context={
        'form': form,
    }

    return render(request, "shop/añadir.html", context)

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