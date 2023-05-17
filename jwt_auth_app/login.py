from flask import Blueprint, request, jsonify
import jwt
from config import SECRET_KEY
from models import User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    print(username)
    # Query the database to find the user
    user = User.query.filter_by(email=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user and user.check_password(password):
        # User is found and password is correct
        # Generate a JWT token
        payload = {'username': username, 'permissions': user.permissions, 'user_id': user.id}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200
    
    # If user is not found or password is incorrect, return an error response
    return jsonify({'message': 'Invalid credentials'}), 401
