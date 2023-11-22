from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema
from bson.objectid import ObjectId
from . import Seed

api = NinjaExtraAPI()
	
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
            client.productos.update_one({"_id": ObjectId(id)}, {"$set": {attr: value}})
        return 202, data
    except:
        return 404, {'message': 'no encontrado'}

@api.get("/productos/{id}", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def get_product(request, id: str):
    try:
        data = busca_prod(id)
        return 202, data
    except:
        return 404, {'message': 'no encontrado'}

@api.delete("/productos/{id}", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def delete_product(request, id: str):
    try:
        data = busca_prod(id)
        client = Seed.BaseDatos()
        client.productos.delete_one({"_id": ObjectId(id)})
        return 202, data
    except:
        return 404, {'message': 'no encontrado'}

@api.post("/productos", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def add_product(request, payload: ProductSchemaIn):
    client = Seed.BaseDatos()
    client.productos.insert_one(payload.dict())
    return 202, payload.dict()
