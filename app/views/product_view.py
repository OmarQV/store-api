def render_product_list(products):
   # Representa una lista de productos como una lista de diccionarios
   return [
      {
         "id": product.id,
         "name": product.name,
         "description": product.description,
         "price": product.price,
         "stock": product.stock,
      }
      for product in products
   ]

def render_product_detail(product):
   # Representa los detalles de un producto como un diccionario
   return {
      "id": product.id,
      "name": product.name,
      "description": product.description,
      "price": product.price,
      "stock": product.stock,
   }
