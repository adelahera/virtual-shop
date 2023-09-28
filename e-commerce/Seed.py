# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os

# Directorio para las imágenes
directorio_imgs = "/e-commerce/imagenes"

# https://requests.readthedocs.io/en/latest/
def getFromApi(api):
	response = requests.get(api)
	return response.json()

# limpia la base de datos
def limpiarBD():
	productos_collection.delete_many({})
	compras_collection.delete_many({})

# descargar imagenes a partir de una url 
def downloadImage(url, filename):
	# comprueba si la imagen esta ya descargada
	if os.path.exists(filename):
		print("Imagen ya descargada")
		return 
	
	# crea el directorio imagenes si no existe
	os.makedirs(os.path.dirname(filename), exist_ok=True)

	response = requests.get(url)
	if response.status_code == 200:
		with open(filename, 'wb') as f:
			f.write(response.content)

class Ticket(BaseModel):
	_id: Any
	quantity: int = Field(ge=1)

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
	user: EmailStr
	date: datetime
	products: list[Ticket]

# Conexión a la BD	
client = MongoClient('mongo', 27017)

# Base de Datos
tienda_db = client.tienda                	
productos = getFromApi('https://fakestoreapi.com/products')
compras = getFromApi('https://fakestoreapi.com/carts')
usuarios = getFromApi('https://fakestoreapi.com/users')

# Elimina el id del producto y de la compra en el json
for prod in productos:
	prod.pop('id')

productos_collection = tienda_db.productos  # Colección
compras_collection = tienda_db.compras  # Colección

limpiarBD()

productos_collection.insert_many(productos)

lista_ids_productos = []
for prod in productos_collection.find():
	lista_ids_productos.append(prod.get('_id'))

for c in compras:
	email_usuario = usuarios[c.get('userId') - 1].get('email')
	c['email'] = email_usuario
	c.pop('userId')
	c.pop('id')
	for p in c.get('products'):
		p['_id'] = lista_ids_productos[p.get('productId') - 1]
		p.pop('productId')

# Insertar todos los productos y compras
compras_collection.insert_many(compras)

# Descargar las imagenes de los productos en la carpeta imagenes
for prod in productos_collection.find():
	url = prod.get('image')
	nombre_imagen = url.replace('https://fakestoreapi.com/img/','')
	ruta_archivo = directorio_imgs + '/' + nombre_imagen
	if url is not None:
		downloadImage(url, ruta_archivo)	

# Consultas a la base de datos
# Electrónica entre 100 y 200€, ordenados por precio
# for prod in productos_collection.find({"category":"electronics", "price": {"$gt": 100, "$lt": 200}}).sort("price"):
# 	pprint(prod)

# # Productos que contengan la palabra 'pocket' en la descripción
# for prod in productos_collection.find({"description": {"$regex": ".*pocket.*"}}):
# 	pprint(prod)

# # Productos con puntuación mayor de 4
# for prod in productos_collection.find({"rating.rate": {"$gt": 4}}):
# 	pprint(prod)

# # Productos de categoria men's clothing, ordenada por puntuación
# for prod in productos_collection.find({"category":"men's clothing"}).sort("rating.rate"):
# 	pprint(prod)

# Facturación total teniendo en cuenta la cantidad de productos comprados
total = 0
for compra in compras_collection.find():
	for prod in compra.get('products'):
		producto = productos_collection.find_one({"_id": prod.get('_id')})
		total += producto.get('price') * prod.get('quantity')

print("Facturación total: " + str(total) + "€")

# Facturación por categoría de producto
# categorias = []
# for prod in productos_collection.find():
# 	categorias.append(prod.get('category'))
