# backend/app/routes.py
from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash
from .config import Config

class SafeSQLAlchemy(SQLAlchemy):
    def _refresh_engine(self):
        """
        Supprime l’extension et l’engine existant pour forcer la reconstruction
        avec la config active (utile si on change SQLALCHEMY_DATABASE_URI en TESTING).
        """
        # Retire l’extension sqlalchemy du Flask app pour la ré-init
        current_app.extensions.pop('sqlalchemy', None)
        # Vide le cache des engines
        self.engines.clear()
        # Ré-initialise l’extension (prise en compte de current_app.config)
        self.init_app(current_app)

    def create_all(self, bind=None):
        # Avant de créer les tables, on reconstruit un engine propre
        self._refresh_engine()
        super().create_all(bind=bind)

    def drop_all(self, bind=None):
        # Avant de drop, même mécanique
        self._refresh_engine()
        super().drop_all(bind=bind)

# --- création de l’app et du db handle ---
app = Flask(__name__)
app.config.from_object(Config)
db = SafeSQLAlchemy(app)

# --- définition du modèle utilisateur ---
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_pwd = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'is_admin': self.is_admin}

# --- garantie que la table existe avant chaque requête ---
@app.before_request
def ensure_tables_exist():
    try:
        db.create_all()
    except OperationalError:
        # la base n’est peut-être pas encore prête, on ignore
        pass

# --- routes CRUD simples ---
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'email and password required'}), 400

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

if __name__ == '__main__':
    try:
        db.drop_all()
        db.create_all()
    except OperationalError:
        pass
    app.run(host='0.0.0.0', port=5000)
    