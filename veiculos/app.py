from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        result = [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "links": [
                    {"rel": "self", "href": f"/products/{product.id}"},
                    {"rel": "update", "href": f"/products/{product.id}"},
                    {"rel": "delete", "href": f"/products/{product.id}"},
                ],
            }
            for product in products
        ]
        return jsonify(result)

    def post(self):
        data = request.get_json()
        new_product = Product(name=data["name"], price=data["price"])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created", "id": new_product.id})

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "links": [
                {"rel": "self", "href": f"/products/{product.id}"},
                {"rel": "update", "href": f"/products/{product.id}"},
                {"rel": "delete", "href": f"/products/{product.id}"},
            ],
        })

    def put(self, product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product.name = data["name"]
        product.price = data["price"]
        db.session.commit()
        return jsonify({"message": "Product updated"})

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted"})
api.add_resource(ProductList, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
