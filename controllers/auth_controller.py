from datetime import timedelta

from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from functools import wraps

from init import bcrypt, db
from models.user import User
from schemas.user_schema import UserSchema, user_schema, users_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# /auth/register - POST - register a new user
@auth_bp.route("/register", methods=["POST"])
def register_user():

    # The request data loaded in a user_schema 
    user_fields = user_schema.load(request.json)
    # Query the User table for the first user with the given email address
    user = User.query.filter_by(email=user_fields["email"]).first()
    # Return an abort message to inform the user is already registered. 
    if user:
        return abort(400, description="Email already registered")\

    try:
        # get the data from the payload body of the request
        body_data = request.get_json()
        # create an instance of the user model
        user = User(
            username=body_data.get("username"),
            email=body_data.get("email")
            )
        # extract the password from the body
        password = body_data.get("password")
        # hash the password as well
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # add and commit to the DB
        db.session.add(user)
        db.session.commit()

        # respond back to the front end
        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        # if a not null field has been left empty null
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation if email address already in use
            return {"error": "Email address is already is use"}, 409
        
# /auth/login - POST - login a user
@auth_bp.route("/login", methods=["POST"])

def login_user():
# get the data from the body of the request
    body_data = request.get_json()
# find the user in DB with that email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
# if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create jwt
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # respond back
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
# else
    else:
        # respond back with an error message
        return {"error": "Invalid email or password"}, 401

# Utilize a decorator in other controllers for checking if a user is an admin to reduce repetitive code
def admin_required(fn):
     # Use the functools.wraps decorator to preserve the original function name and signature
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the user id invoking get_jwt_identity
        user_id = get_jwt_identity()
        # Retrieves a user object from the database based on the provided user ID
        user = User.query.get(user_id)
        # Stop the request if the user is not an admin
        if not user.admin:
            abort(401, description="Unauthorized user")
        return fn(*args, **kwargs)
    # Return the wrapped function
    return wrapper