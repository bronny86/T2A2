from flask import Blueprint, jsonify, request, abort
from main import db
from models.user import User
from schemas.user_schema import user_schema, users_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import bcrypt
from controllers.auth_controller import admin_required

# Create a Flask Blueprint for the /users endpoint
users_bp = Blueprint('users', __name__, url_prefix="/users")

# The GET route endpoint for getting list of all users (admin required)
@users_bp.route("/", methods=["GET"])
# Require a valid JWT token to access the endpoint
@jwt_required()
# Check whether the user has admin permissions to access the endpoint
@admin_required
def get_users():
    # Get all the users from the database table
    user_list = User.query.all()
    # Convert the users from the database into a JSON format and store them in result
    result = users_schema.dump(user_list)
    # Return the data in JSON format
    return jsonify(result)


# The GET routes endpoint for getting a single user (admin required)
@users_bp.route("/<int:id>/", methods=["GET"])
# Require a valid JWT token to access the endpoint
@jwt_required()
# Check whether the user has admin permissions to access the endpoint
@admin_required
def get_user(id):
    # Query database for user filtering by id
    user_in_db = User.query.filter_by(id=id).first()
    # Return an error if the user doesn't exist
    if not user_in_db:
        return abort(400, description= "User does not exist")
    # Convert the user from the database into a JSON format and store them in result
    result = user_schema.dump(user_in_db)
    # return the data in JSON format
    return jsonify(result)


# The PUT routes endpoint granting users permission to update their user fields (except admin field). 
@users_bp.route("/<int:id>/", methods=["PUT"])
# Require a valid JWT token to access the endpoint
@jwt_required()
def update_user(id):
    # Get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    # Find the user in the db based on their ID
    user = User.query.filter_by(id=user_id).first()
    # Only allow users to update their own fields
    if user.id != id:
        return abort(401, description="You are not authorized to update this user")
    # Load user data from the request
    body_data = request.get_json()
    # Try to extract the required fields and catch KeyError if any field is missing
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
    # Set the user attributes
        user.username = body_data.get("username") or user.username
        user.email = body_data.get("email") or user.email
        user.password = bcrypt.generate_password_hash("password").decode("utf-8")
    # User not allowed to set admin to True
    user.is_admin = False
    # Add to the database and commit
    db.session.commit()
    # Return the updated user in the response
    return jsonify(user_schema.dump(user))


# The DELETE routes endpoint; allowing only admin to delete users
@users_bp.route("/<int:id>/", methods=["DELETE"])
# Require a valid JWT token to access the endpoint
@jwt_required()
# Check whether the user has admin permissions to access the endpoint
@admin_required
def delete_user(id):
    # Find the user in the database filtering by ID
    find_user = User.query.filter_by(id=id).first()
    # Return an error if the user doesn't exist
    if not find_user:
        return abort(400, description= "User does not exist")
    # Delete the user from the database and commit
    db.session.delete(find_user)
    db.session.commit()
    # Return the user in the response
    return jsonify(user_schema.dump(find_user))