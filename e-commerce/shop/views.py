from django.http import HttpResponse
from . import consultas
from django.shortcuts import render
from pymongo import MongoClient
import sys
import re
client = MongoClient('mongo', 27017)

def index(request):
    return render(request, "shop/index.html")

def buscar(request):

    busqueda = request.GET.get('busqueda', 'No items found')
    regex = re.compile(f".*{re.escape(busqueda)}.*", re.IGNORECASE)
    p=client.tienda.productos.find({"title": regex})
    productos=list(p)
    context={
        'busqueda' : busqueda,
        'productos' : productos
    }
    return render(request, "shop/busqueda.html", context)

def busq_cat(request, busqueda):

    p = client.tienda.productos.find({"category": busqueda})
    productos = list(p)

    context={
        'busqueda': busqueda,
        'productos': productos
    }
    return render(request, "shop/categorias.html", context)

def consulta_1(request):
    consulta = consultas.electronics_between_100_and_200()
    return render(request, "shop/products_list.html", {"consulta":consulta})

def consulta_2(request):
    consulta = consultas.products_containing_word_pocket()
    return render(request, "shop/products_list.html", {"consulta":consulta})

def consulta_3(request):
    consulta = consultas.products_with_rating_above_4()
    return render(request, "shop/products_list.html", {"consulta":consulta})

def consulta_4(request):
    consulta = consultas.mens_clothing_sorted_by_rating()
    return render(request, "shop/products_list.html", {"consulta":consulta})

def consulta_5(request):
    consulta = consultas.total_revenue()
    return HttpResponse(consulta)

def consulta_6(request):
    consulta = consultas.revenue_by_category()
    return HttpResponse(consulta)