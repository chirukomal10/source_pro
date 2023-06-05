import sys
import os
import json
from flask import Flask, jsonify
from flask_restful import Api
from api.views import UserResource
from admin.routes import admin_blueprint
from database import db, create_database
from login import login_bp
from flask_swagger_ui import get_swaggerui_blueprint

# Get the absolute path to the directory containing main.py
project_dir = os.path.abspath(os.path.dirname(__file__))

# Append the project directory to the import search path
sys.path.append(project_dir)

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
app.register_blueprint(admin_blueprint)
app.register_blueprint(login_bp)

api = Api(app)
api.add_resource(UserResource, '/users/', '/users/<int:user_id>')

# Serve Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "jwt_auth_app"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))


if __name__ == '__main__':
    with app.app_context():
        create_database()
    app.run(debug=True)
