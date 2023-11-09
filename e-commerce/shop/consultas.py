# from pymongo import MongoClient
# from pprint import pprint

# client = MongoClient('mongo', 27017)
    
# tienda_db = client.tienda
# productos_collection = tienda_db.productos
# compras_collection = tienda_db.compras

# def electronics_between_100_and_200():
#     results = []
#     for prod in productos_collection.find({"category": "electronics", "price": {"$gt": 100, "$lt": 200}}):
#         results.append(prod)
#     return results
        
# # Productos que contienen la palabra "pocket" en su descripción
# def products_containing_word_pocket():
#     results = []
#     for prod in productos_collection.find({"description": {"$regex": ".*pocket.*"}}):
#         results.append(prod)
#     return results

# # Productos con rating mayor que 4
# def products_with_rating_above_4():
#     results = []
#     for prod in productos_collection.find({"rating.rate": {"$gt": 4}}):
#         results.append(prod)
#     return results

# # Ropa de hombre ordenada por rating
# def mens_clothing_sorted_by_rating():
#     results = []
#     for prod in productos_collection.find({"category": "men's clothing"}).sort("rating.rate"):
#         results.append(prod)
#     return results

# # Facturación total
# def total_revenue():
#     total = 0
#     for compra in compras_collection.find():
#         for prod in compra.get('products'):
#             producto = productos_collection.find_one({"_id": prod.get('_id')})
#             total += producto.get('price') * prod.get('quantity')
#     return total

# # Facturacion total mostrando por cada categoria, el total de ventas
# def revenue_by_category():
#     results = []
#     for prod in productos_collection.find():
#         total = 0
#         for compra in compras_collection.find():
#             for prod_compra in compra.get('products'):
#                 if prod_compra.get('_id') == prod.get('_id'):
#                     total += prod.get('price') * prod_compra.get('quantity')
#         results.append({"category": prod.get('category'), "total": total})
#     return results

