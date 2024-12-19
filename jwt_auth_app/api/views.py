from flask_restful import Resource, reqparse
from flask import request, make_response, g
from database import db
from models import User
from auth import auth_required


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str)
    parser.add_argument("password", type=str)

    @auth_required("admin")
    def post(self):
        args = self.parser.parse_args()
        user = User(email=args["email"], permissions="user")
        user.set_password(args["password"])
        user.password = user.password_hash
        user.save()
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

    @auth_required("admin")
    def get(self, user_id):
        user = User.get_by_id(user_id)
        if user:
            return user.to_dict(), 200
        else:
            return make_response({"message": "User not found"}, 404)

    @auth_required("admin", "user")
    def put(self, user_id):
        args = self.parser.parse_args()
        user = User.get_by_id(user_id)

        if not user:
            return make_response({"message": "User not found"}, 404)

        # Check if the authenticated user is an admin or the owner of the user_id
        decoded_token = g.decoded_token
        authenticated_user_id = decoded_token.get("user_id")
        is_admin = "admin" in decoded_token.get("permissions", [])
        is_owner = authenticated_user_id == user_id

        if not is_admin and not is_owner:
            return {"message": "Unauthorized"}, 403

        # Update user details based on the provided arguments
        if args["email"]:
            user.email = args["email"]

        user.save()
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 200
