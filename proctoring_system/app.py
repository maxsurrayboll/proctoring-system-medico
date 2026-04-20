<<<<<<< HEAD
from flask import Flask, render_template, session, redirect
from config import Config
from models import db
from routes.auth_routes import auth_bp, bcrypt
from routes.exam_routes import exam_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(exam_bp, url_prefix='/exam')

if not os.path.exists('frames'):
    os.makedirs('frames')

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')


@app.route('/examen')
def examen():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('examen.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# ------------------ CONFIGURACIÓN ------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ------------------ MODELO ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='student')

    def __repr__(self):
        return f'<User {self.username}>'

# ------------------ CREAR DB + ADMIN ------------------
with app.app_context():
    db.create_all()

    # Crear admin si no existe
    if not User.query.filter_by(username='admin').first():
        admin_pass = bcrypt.generate_password_hash('Admin123*').decode('utf-8')
        admin = User(username='admin', password=admin_pass, role='admin')
        db.session.add(admin)
        db.session.commit()

# ------------------ LOGIN ------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['contraseña']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return "Credenciales incorrectas"

    return render_template('login.html')

# ------------------ REGISTRO ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['contraseña']

        # Verificar si ya existe
        if User.query.filter_by(username=username).first():
            return "El usuario ya existe"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# ------------------ DASHBOARD ------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user=session['user'], role=session['role'])

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------ EXAMEN ------------------
@app.route('/examen')
def examen():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('examen.html')

# ------------------ RUN ------------------
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 01a3daeec870760731c79ef743895bb1ab168f97
