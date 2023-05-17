from functools import wraps
from flask import request, jsonify, g
import jwt
from config import SECRET_KEY

def has_sufficient_permissions(decoded_token, permissions):
    user_permissions = decoded_token.get('permissions', [])
    return any(permission in user_permissions for permission in permissions)

def auth_required(*permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '')
            if not token:
                return {'message': 'Authorization header is missing'}, 401

            parts = token.split(' ')
            if len(parts) != 2 or parts[0] != 'Bearer':
                return {'message': 'Invalid authorization header format'}, 401

            jwt_token = parts[1]

            try:
                secret_key = SECRET_KEY
                
                decoded_token = jwt.decode(jwt_token.encode(), secret_key, algorithms=['HS256'])

                
                if not has_sufficient_permissions(decoded_token, permissions):
                    return {'message': 'Insufficient permissions'}, 403
                
                g.decoded_token = decoded_token
                return func(*args, **kwargs)
                
            except jwt.ExpiredSignatureError:
                return jsonify({'message': str('Token has expired')}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': str('Invalid token')}), 401

        
        return wrapper
    
    return decorator
