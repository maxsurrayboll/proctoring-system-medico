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