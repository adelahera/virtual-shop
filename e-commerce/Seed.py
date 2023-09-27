# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os

		
# https://requests.readthedocs.io/en/latest/
def getProductos(api):
	response = requests.get(api)
	return response.json()

def getCompras(api):
	response = requests.get(api)
	return response.json()

# limpia la base de datos
def limpiarBD():
	productos_collection.delete_many({})
	compras_collection.delete_many({})

# descargar imagenes a partir de una url 
def downloadImage(url, filename):
	#comprueba que filename no existe
	if os.path.exists(filename):
		print("El fichero ya existe")
		return 
	response = requests.get(url)
	if response.status_code == 200:
		with open(filename, 'wb') as f:
			f.write(response.content)

# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Nota(BaseModel):
	rate: float = Field(ge=0., lt=5.)
	count: int = Field(ge=1)
				
class Producto(BaseModel):
	_id: Any
	name: str
	price: float
	description: str
	category: str
	image: FilePath | None
	rating: Nota

class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	date: datetime
	productos: list	

# Conexión a la BD	
client = MongoClient('mongo', 27017)

# Directorio para las imágenes
directorio_imgs = "/e-commerce/imagenes"

# Base de Datos
tienda_db = client.tienda                	
productos = getProductos('https://fakestoreapi.com/products')
compras = getCompras('https://fakestoreapi.com/carts')

productos_collection = tienda_db.productos  # Colección
compras_collection = tienda_db.compras  # Colección
	
limpiarBD()

for prod in productos:
	prod.pop('id')

for comp in compras:
	comp.pop('id')


# Insertar todos los productos y compras
productos_collection.insert_many(productos)
compras_collection.insert_many(compras)

# Descargar las imagenes de los productos en la carpeta imagenes
for prod in productos_collection.find():
	url = prod.get('image')
	ruta_archivo = directorio_imgs + "/" + str(url)
	if url is not None:
		downloadImage(url, ruta_archivo)	

# Consultas a la base de datos
# Electrónica entre 100 y 200€, ordenados por precio
for prod in productos_collection.find({"category":"electronics", "price": {"$gt": 100, "$lt": 200}}).sort("price"):
	pprint(prod)

# # Productos que contengan la palabra 'pocket' en la descripción
# for prod in productos_collection.find({"description": {"$regex": ".*pocket.*"}}):
# 	pprint(prod)

# # Productos con puntuación mayor de 4
# for prod in productos_collection.find({"rating.rate": {"$gt": 4}}):
# 	pprint(prod)

# # Productos de categoria men's clothing, ordenada por puntuación
# for prod in productos_collection.find({"category":"men's clothing"}).sort("rating.rate"):
# 	pprint(prod)

# Facturación total de la tienda
# total = 0
# for comp in compras_collection.find():
#     productos = comp.get('productos')
#     if productos is not None and isinstance(productos, list):
#         for prod in productos:
#             total += prod.get('price')

# print("Facturación total: " + str(total) + "€")

# Facturación por categoría de producto
# categorias = []
# for prod in productos_collection.find():
# 	categorias.append(prod.get('category'))
