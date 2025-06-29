import os
from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from .config import Config


class SafeSQLAlchemy(SQLAlchemy):
    """Réinitialise proprement l’engine quand la config change (tests)."""

    def _refresh_engine(self):
        real_app = current_app._get_current_object()
        if getattr(real_app, "_got_first_request", False):
            return                     # pas de reset après la 1ʳᵉ requête
        real_app.extensions.pop("sqlalchemy", None)
        if hasattr(self, "_app_engines"):
            self._app_engines.pop(real_app, None)
        self.init_app(real_app)

    def create_all(self):
        self._refresh_engine()
        super().create_all()

    def drop_all(self):
        self._refresh_engine()
        super().drop_all()


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)                                # Autorise les appels depuis :3000

db = SafeSQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_pwd = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "is_admin": self.is_admin}


# ────────────────────────────────────────────────────────────────────────────
@app.before_request
def ensure_tables_exist():
    """Crée les tables si la base vient juste d’être lancée (CI, dev)."""
    try:
        db.create_all()
    except OperationalError:
        pass


# ──────────────── POST /users ───────────────────────────────────────────────
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json() or {}
    if "email" not in data or "password" not in data:
        return jsonify({"error": "email and password required"}), 400

    user = User(
        email=data["email"],
        hashed_pwd=generate_password_hash(data["password"]),
        is_admin=False,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id}), 201


# ──────────────── GET /users ────────────────────────────────────────────────
@app.route("/users", methods=["GET"])
def list_users():
    return jsonify([u.to_dict() for u in User.query.all()]), 200


# ──────────────── DELETE /users/<id> ────────────────────────────────────────
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Suppression protégée par le token admin simple."""
    token = request.headers.get("X-Admin-Token")
    if token != os.getenv("ADMIN_PASSWORD"):
        return jsonify({"error": "unauthorized"}), 401

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        db.drop_all()
        db.create_all()
    except OperationalError:
        pass
    app.run(host="0.0.0.0", port=5000)
