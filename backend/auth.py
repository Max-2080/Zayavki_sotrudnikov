from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import Employee
from database import db

jwt = JWTManager()

def init_auth(app):
    jwt.init_app(app)

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

def authenticate_user(username, password):
    user = Employee.query.filter_by(username=username).first()
    if user and verify_password(user.password, password):
        return create_access_token(identity=user.id)
    return None