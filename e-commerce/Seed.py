# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests

		
# https://requests.readthedocs.io/en/latest/
def getProductos(api):
	response = requests.get(api)
	return response.json()
				
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


# dato = { 
# 	'name': "MBJ Women's Solid Short Sleeve Boat Neck V ", 
# 	'price': 9.85, 
# 	'description': '95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem', 'category': "women's clothing", 
# 	'category': "women's clothing",
# 	'iamge': None, 
# 	'rating': {'rate': 4.7, 'count': 130}
# }

# # Valida con el esquema:
# # daría error si no corresponde algún tipo 
# producto = Producto(**dato)

# print(producto.descripción)
# pprint(producto.model_dump()) # Objeto -> python dict


# # Conexión con la BD				
# # https://pymongo.readthedocs.io/en/stable/tutorial.html
				
# productos_collection.insert_one(producto.model_dump()) 
				
# print(productos_collection.count_documents({}))

# # todos los productos
# lista_productos_ids = []
# for prod in productos_collection.find():
# 	pprint(prod)
# 	print(prod.get('_id'))   # Autoinsertado por mongo
# 	lista_productos_ids.append(prod.get('_id'))
	
# print(lista_productos_ids)
	
# nueva_compra = {
# 	'usuario': 'fulanito@correo.com',
# 	'fecha': datetime.now(),
# 	'productos': lista_productos_ids
# }
	
# # valida
# compra = Compra(**nueva_compra)
# pprint(compra.model_dump())
# # añade a BD
# compras_collection = tienda_db.compras  # Colección
# compras_collection.insert_one(compra.model_dump())
	
# for com in compras_collection.find():
# 	pprint(com)

client = MongoClient('mongo', 27017)

tienda_db = client.tienda                	# Base de Datos
productos = getProductos('https://fakestoreapi.com/products')

# Insertar todos los productos
productos_collection = tienda_db.productos  # Colección

for prod in productos_collection.find():
	prod.pop('_id')
	pprint(prod)

productos_collection.insert_many(productos)