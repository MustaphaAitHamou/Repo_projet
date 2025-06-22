from flask import Flask, request, jsonify, abort
from .models import db, User
from .config import Config
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

# Créer la BDD si besoin
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data.get('email') or not data.get('password'):
        abort(400)
    u = User(email=data['email'])
    u.set_password(data['password'])
    db.session.add(u)
    db.session.commit()
    return jsonify({'id': u.id}), 201

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.with_entities(User.id, User.email, User.is_admin).all()
    return jsonify([{'id': u.id, 'email': u.email, 'is_admin': u.is_admin} for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return jsonify({'id': u.id, 'email': u.email, 'is_admin': u.is_admin})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Auth simplifiée: header X-Admin-Token == ADMIN_PASSWORD
    token = request.headers.get('X-Admin-Token')
    if token != os.getenv('ADMIN_PASSWORD'):
        abort(403)
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return '', 204