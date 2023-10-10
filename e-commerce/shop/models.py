from django.db import models
from pydantic import BaseModel, FilePath, Field, EmailStr, field_validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os
import queries

# https://requests.readthedocs.io/en/latest/
def getFromApi(api):
	response = requests.get(api)
	return response.json()

# limpia la base de datos
def cleanDB():
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

	# Incluye validación para el nombre que debe empezar por mayúscula
	@field_validator('name')
	def validate_name(cls, value):
		if not value[0].isupper():
			raise ValueError('El nombre debe empezar por mayúscula')
		return value

class Compra(BaseModel):
	_id: Any
	user: EmailStr
	date: datetime
	products: list[Ticket]

# Directorio para las imágenes
directorio_imgs = "/e-commerce/imagenes"

# Conexión a la BD	
client = MongoClient('mongo', 27017)

# Base de Datos
tienda_db = client.tienda                	
productos = getFromApi('https://fakestoreapi.com/products')
compras = getFromApi('https://fakestoreapi.com/carts')
usuarios = getFromApi('https://fakestoreapi.com/users')

# Elimina el id del producto en el json
for prod in productos:
	prod.pop('id')

productos_collection = tienda_db.productos  # Colección
compras_collection = tienda_db.compras  # Colección

# Limpia la base de datos para evitar duplicados
cleanDB()

# Insertar todos los productos
productos_collection.insert_many(productos)

# Guardar los ids de los productos en una lista
lista_ids_productos = []
for prod in productos_collection.find():
	lista_ids_productos.append(prod.get('_id'))

# Añadir el email del usuario y eliminar los ids de usuario y compra
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

if __name__ == "__main__":
    queries.realizar_consultas()
