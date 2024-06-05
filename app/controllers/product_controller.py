from flask import Blueprint, request, jsonify
from app.models.product_model import Product
from app.views.product_view import render_product_list, render_product_detail
#! JWT
from app.utils.decorators import jwt_required, roles_required

# Crear un blueprint para el controlador de productoes
product_bp = Blueprint("product", __name__)


# Ruta para obtener la lista de productoes
@product_bp.route("/products", methods=["GET"])
@jwt_required
#! implementando roles
@roles_required(roles=["admin", "user"])
def get_products():
   products = Product.get_all()
   return jsonify(render_product_list(products))


# Ruta para obtener un producto específico por su ID
@product_bp.route("/products/<int:id>", methods=["GET"])
@jwt_required
#! implementando roles
@roles_required(roles=["admin", "user"])
def get_product(id):
   product = Product.get_by_id(id)
   if product:
      return jsonify(render_product_detail(product))
   return jsonify({"error": "Producto no encontrado"}), 404


# Ruta para crear un nuevo producto
@product_bp.route("/products", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_product():
   data = request.json
   name = data.get("name")
   description = data.get("description")
   price = data.get("price")
   stock = data.get("stock")
   # Validación simple de datos de entrada
   if not name or not description or not price>=0 or not stock>=0:
      return jsonify({"error": "Faltan datos requeridos"}), 400
   # Crear un nuevo producto y guardarlo en la base de datos
   product = Product(name=name, description=description, price=price, stock=stock)
   product.save()

   return jsonify(render_product_detail(product)), 201


# Ruta para actualizar un producto existente
@product_bp.route("/products/<int:id>", methods=["PUT"])
@jwt_required
#! implementando roles
@roles_required(roles=["admin"])
def update_product(id):
   product = Product.get_by_id(id)
   if not product:
      return jsonify({"error": "Producto no encontrado"}), 404
   data = request.json
   name = data.get("name")
   description = data.get("description")
   price = data.get("price")
   stock = data.get("stock")
   # Actualizar los datos del producto
   product.update(name=name, description=description, price=price, stock=stock)
   return jsonify(render_product_detail(product))


# Ruta para eliminar un producto existente
@product_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required
#! implementando roles
@roles_required(roles=["admin"])
def delete_product(id):
   product = Product.get_by_id(id)
   if not product:
      return jsonify({"error": "Producto no encontrado"}), 404
   # Eliminar el producto de la base de datos
   product.delete()
   # Respuesta vacía con código de estado 204 (sin contenido)
   return "", 204



