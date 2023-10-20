from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar', views.buscar, name='buscar'),
    path('busq/<str:busqueda>', views.busq_cat, name='busq_cat'),
    path('consulta1/', views.consulta_1, name='consulta_1'),
    path('consulta2/', views.consulta_2, name='consulta_2'),
    path('consulta3/', views.consulta_3, name='consulta_3'),
    path('consulta4/', views.consulta_4, name='consulta_4'),
    path('consulta5/', views.consulta_5, name='consulta_5'),
    path('consulta6/', views.consulta_6, name='consulta_6'),
]