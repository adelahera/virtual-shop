from django.http import HttpResponse


def index(request):
    return HttpResponse("<br>Hello </br>, world. You're at the polls index.")