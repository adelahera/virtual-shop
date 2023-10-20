from django.http import HttpResponse
from . import consultas
from django.shortcuts import render
from pymongo import MongoClient

def index(request):
    return render(request, "shop/index.html")

def buscar(request):
    context={
        'busqueda': request.GET.get('busqueda', 'No items found')
    }
    return render(request, "shop/busqueda.html", context)

def busq_cat(request, busqueda):
    context={
        'busqueda': busqueda
    }
    return render(request, "shop/busqueda.html", context)

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