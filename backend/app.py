# backend/app.py
import os
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from controllers.auth_controller import auth_controller

load_dotenv()

app = Flask(__name__, 
            static_folder='static', 
            template_folder='frontend/build')


# CORS yapılandırmasını güncelledik, tüm domainlerden gelen isteklere izin veriyoruz
CORS(app, origins="*")

# Blueprint'i kayıt ediyoruz
#app.register_blueprint(physical_controller, url_prefix='/api/physical-development')
app.register_blueprint(auth_controller, url_prefix='/api/auth')

@app.route('/')
def home():
    return "Welcome to the GreenCat API!"

@app.route('/<path:path>')
def serve_react_app(path):
    return send_from_directory(app.template_folder, path)


@app.route('/static/graphs/physical_graphs/<path:filename>')
def serve_physical_graph(filename):
    graphs_dir = os.path.join(app.root_path, 'static', 'graphs', 'physical_graphs')
    return send_from_directory(graphs_dir, filename)

@app.route('/static/graphs/conditional_graphs/<path:filename>')
def serve_conditional_graph(filename):
    graphs_dir = os.path.join(app.root_path, 'static', 'graphs', 'conditional_graphs')
    return send_from_directory(graphs_dir, filename)

@app.route('/static/graphs/endurance_graphs/<path:filename>')
def serve_endurance_graph(filename):
    graphs_dir = os.path.join(app.root_path, 'static', 'graphs', 'endurance_graphs')
    return send_from_directory(graphs_dir, filename)

@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
