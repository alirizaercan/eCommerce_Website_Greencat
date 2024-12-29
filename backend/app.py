# backend/app.py
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from controllers.auth_controller import auth_controller
from controllers.admin_controller import admin_controller
from controllers.product_controller import product_controller
from controllers.address_controller import address_controller
from controllers.carrier_controller import carrier_controller
from controllers.cart_controller import cart_controller
from controllers.category_controller import category_controller  # Import category_controller
from controllers.discount_controller import discount_controller
from controllers.inventory_controller import inventory_controller
from controllers.order_controller import order_controller
from controllers.payment_controller import payment_controller
from controllers.session_controller import session_controller
from controllers.checkout_controller import checkout_controller

load_dotenv()

app = Flask(__name__,
            static_folder='frontend/build',
            template_folder='frontend/build')

# CORS yapılandırmasını güncelledik, tüm domainlerden gelen isteklere izin veriyoruz
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Blueprint'leri kayıt ediyoruz
app.register_blueprint(admin_controller, url_prefix='/api/admin')
app.register_blueprint(auth_controller, url_prefix='/api/auth')
app.register_blueprint(product_controller, url_prefix='/api/products')
app.register_blueprint(address_controller, url_prefix='/api')
app.register_blueprint(carrier_controller, url_prefix='/api/carrier')
app.register_blueprint(cart_controller, url_prefix='/api/cart')
app.register_blueprint(category_controller, url_prefix='/api/categories')  # Register category_controller
app.register_blueprint(discount_controller, url_prefix='/api/discounts')
app.register_blueprint(inventory_controller, url_prefix='/api/inventory')
app.register_blueprint(order_controller, url_prefix='/api/orders')
app.register_blueprint(payment_controller, url_prefix='/api/payments')
app.register_blueprint(session_controller, url_prefix='/api/sessions')
app.register_blueprint(checkout_controller, url_prefix='/api/checkout')

@app.route('/')
def home():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_app(path):
    return send_from_directory(app.template_folder, path)

app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/static/graphs/admin_graphs/<path:filename>')
def serve_graph(filename):
    return send_from_directory(
        os.path.join(app.config['STATIC_FOLDER'], 'graphs', 'admin_graphs'),
        filename
    )

@app.route('/static/graphs/conditional_graphs/<path:filename>')
def serve_conditional_graph(filename):
    graphs_dir = os.path.join(app.root_path, 'static', 'graphs', 'conditional_graphs')
    return send_from_directory(graphs_dir, filename)

@app.route('/static/graphs/endurance_graphs/<path:filename>')
def serve_endurance_graph(filename):
    graphs_dir = os.path.join(app.root_path, 'static', 'graphs', 'endurance_graphs')
    return send_from_directory(graphs_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)