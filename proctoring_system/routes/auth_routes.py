from flask import Blueprint, request, redirect, session
from models import db
from models.user_model import User
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# ------------------ REGISTER ------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if User.query.filter_by(username=username).first():
        return "Usuario ya existe"

    hashed = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(username=username, password=hashed)
    db.session.add(user)
    db.session.commit()

    return redirect('/')

# ------------------ LOGIN ------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    print("METHOD:", request.method)
    print("FORM:", request.form)

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return "Credenciales inválidas"

    session['user_id'] = user.id
    return redirect('/dashboard')