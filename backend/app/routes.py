# backend/app/routes.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# -- Models --

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_pwd = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_admin': self.is_admin,
        }

# -- Create tables juste avant la première requête --
@app.before_first_request
def create_tables():
    db.create_all()

# -- Routes --

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'email and password required'}), 400

    from werkzeug.security import generate_password_hash

    user = User(
        email=data['email'],
        hashed_pwd=generate_password_hash(data['password']),
        is_admin=False
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

# -- Lancement direct (dev) --

if __name__ == '__main__':
    # pour lancer avec python routes.py
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
