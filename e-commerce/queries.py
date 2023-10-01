import os
from pymongo import MongoClient
from pprint import pprint

# Crea el directorio salida_consultas si no existe
if not os.path.exists("salida_consultas"):
    os.makedirs("salida_consultas")

def realizar_consultas():
    
    client = MongoClient('mongo', 27017)
    
    tienda_db = client.tienda
    productos_collection = tienda_db.productos
    compras_collection = tienda_db.compras

    # Funcion para guardar los resultados de las consultas en un fichero
    def save_results_to_file(file_name, results):
        file_path = os.path.join("salida_consultas", file_name)
        with open(file_path, 'w') as file:
            for result in results:
                file.write(str(result) + '\n')

    # Electrónica entre 100 y 200€, ordenados por precio
    def electronics_between_100_and_200():
        results = []
        for prod in productos_collection.find({"category": "electronics", "price": {"$gt": 100, "$lt": 200}}).sort("price"):
            results.append(prod)
        save_results_to_file("electronics_between_100_and_200.txt", results)

    # Productos que contienen la palabra "pocket" en su descripción
    def products_containing_word_pocket():
        results = []
        for prod in productos_collection.find({"description": {"$regex": ".*pocket.*"}}):
            results.append(prod)
        save_results_to_file("products_containing_word_pocket.txt", results)

    # Productos con rating mayor que 4
    def products_with_rating_above_4():
        results = []
        for prod in productos_collection.find({"rating.rate": {"$gt": 4}}):
            results.append(prod)
        save_results_to_file("products_with_rating_above_4.txt", results)

    # Ropa de hombre ordenada por rating
    def mens_clothing_sorted_by_rating():
        results = []
        for prod in productos_collection.find({"category": "men's clothing"}).sort("rating.rate"):
            results.append(prod)
        save_results_to_file("mens_clothing_sorted_by_rating.txt", results)

    # Facturación total
    def total_revenue():
        total = 0
        for compra in compras_collection.find():
            for prod in compra.get('products'):
                producto = productos_collection.find_one({"_id": prod.get('_id')})
                total += producto.get('price') * prod.get('quantity')
        with open(os.path.join("salida_consultas", "total_revenue.txt"), 'w') as file:
            file.write("Total revenue: " + str(total) + "€\n")

    # Facturacion total por cada categoria, mostrando la categoria y la facturacion
    def revenue_by_category():
        results = []
        for prod in productos_collection.find():
            total = 0
            for compra in compras_collection.find():
                for prod_compra in compra.get('products'):
                    if prod_compra.get('_id') == prod.get('_id'):
                        total += prod.get('price') * prod_compra.get('quantity')
            results.append({"category": prod.get('category'), "revenue": total})
        save_results_to_file("revenue_by_category.txt", results)

    electronics_between_100_and_200()
    products_containing_word_pocket()
    products_with_rating_above_4()
    mens_clothing_sorted_by_rating()
    total_revenue()
    revenue_by_category()

if __name__ == "__main__":
    realizar_consultas()