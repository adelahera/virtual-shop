from django.http import HttpResponse
from . import consultas
from django.shortcuts import render
from pymongo import MongoClient

def index(request):
    html = "<h1>¡Bienvenido a la tienda!</h1>" \
           "<ul>" \
           "<li><a href='consulta1/'>Consulta 1</a></li>" \
           "<li><a href='consulta2/'>Consulta 2</a></li>" \
           "<li><a href='consulta3/'>Consulta 3</a></li>" \
           "<li><a href='consulta4/'>Consulta 4</a></li>" \
           "<li><a href='consulta5/'>Consulta 5</a></li>" \
           "<li><a href='consulta6/'>Consulta 6</a></li>" \
           "</ul>"
    return HttpResponse(html)

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