# app/routes.py

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# instanciation de l'extension
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # configuration par défaut (remplacez la DATABASE_URL par votre chaîne)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://myuser:my_password@mysql:3306/mydb'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # liaison de l'extension
    db.init_app(app)

    # ---- override dynamique de drop_all/create_all pour pytest ----
    from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
    _orig_drop_all = _BaseSQLAlchemy.drop_all
    _orig_create_all = _BaseSQLAlchemy.create_all

    def _dynamic_drop_all():
        # vide le cache des engines pour forcer la création
        db.engines.clear()
        # recrée l'engine par défaut d'après app.config
        _ = db.engine
        # appelle la méthode d'origine (sans argument)
        return _orig_drop_all(db)

    def _dynamic_create_all():
        db.engines.clear()
        _ = db.engine
        return _orig_create_all(db)

    db.drop_all = _dynamic_drop_all
    db.create_all = _dynamic_create_all
    # ---------------------------------------------------------------

    # import du modèle *après* init_app pour éviter les boucles
    from .models import User  # noqa: F401

    @app.route('/users', methods=['POST'])
    def add_user():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'email and password required'}), 400

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id}), 201

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([{'id': u.id, 'email': u.email} for u in users]), 200

    return app


# création de l'objet app module‐level pour les imports directs
app = create_app()
