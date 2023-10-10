from django.http import HttpResponse
from . import consultas

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
    resultados = consultas.electronics_between_100_and_200()
    return render(request, "shop/products_list.html", {"resultados": consulta1})

def consulta_2(request):
    return HttpResponse("Consulta 2")

def consulta_3(request):
    return HttpResponse("Consulta 3")

def consulta_4(request):
    return HttpResponse("Consulta 4")

def consulta_5(request):
    return HttpResponse("Consulta 5")

def consulta_6(request):
    return HttpResponse("Consulta 6")