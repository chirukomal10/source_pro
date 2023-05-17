from flask import request
from models import User
from database import db

def create_admin():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return 'Email and password are required', 400

    admin_user = User(email=email, permissions='admin')
    admin_user.set_password(password)
    admin_user.password = admin_user.password_hash  # Set the hashed password to the password attribute
    admin_user.save()
    db.session.add(admin_user)
    db.session.commit()

    return 'Admin user created successfully', 201