from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema
from bson.objectid import ObjectId
from . import Seed
from typing import List
from ninja.security import django_auth
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

api = NinjaExtraAPI(auth=GlobalAuth())
	
class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):  # sirve para validar y para documentación
	id:    str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
	
class ProductSchemaIn(Schema):
	title: str
	price: float
	description: str
	category: str
	rating: Rate
	
	
class ErrorSchema(Schema):
	message: str
	
def busca_prod(id):
    client = Seed.BaseDatos()
    prod = client.productos.find_one({"_id": ObjectId(id)})
    if prod is None:
        raise Exception(f'No existe el producto con id {id}')
    return prod

@api.put("/productos/{id}", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def modify_product(request, id: str, payload: ProductSchemaIn):
    try:
        data = busca_prod(id)
        client = Seed.BaseDatos()
        for attr, value in payload.dict().items():
            data = client.productos.update_one({"_id": ObjectId(id)}, {"$set": {attr: value}})
        data['id'] = str(data['_id'])
        del data['_id']
        return 202, data
    except:
        return 404, {'message': 'no encontrado'}

@api.get("/productos", auth=None,tags=['TIENDA DAI'], response={202: List[ProductSchema], 404: ErrorSchema})
def get_products(request, offset: int = 0, limit: int = 10):
    try:
        client = Seed.BaseDatos()
        data = list(client.productos.find({}).skip(offset).limit(offset+limit))
        for prod in data:
            prod['id'] = str(prod['_id'])
            del prod['_id']
        return 202, data
    except:
        return 404, {'message': 'no encontrado'}

@api.get("/productos/{id}", auth=None,tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def get_product(request, id: str):
    try:
        data = busca_prod(id)
        data['id'] = str(data['_id'])
        del data['_id']
        return 202, data
    except:
        return 404, {'message': 'no encontrado'}

@api.delete("/productos/{id}", tags=['TIENDA DAI'], response={200: None, 404: ErrorSchema})
def delete_product(request, id: str):
    try:
        client = Seed.BaseDatos()
        client.productos.delete_one({"_id": ObjectId(id)})
        return 200, None
    except:
        return 404, {'message': 'no encontrado'}

@api.post("/productos", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def add_product(request, payload: ProductSchemaIn):
    client = Seed.BaseDatos()
    insert = payload.dict()
    client.productos.insert_one(insert)
    insert['id'] = str(insert['_id'])
    del insert['_id']
    return 202, insert
