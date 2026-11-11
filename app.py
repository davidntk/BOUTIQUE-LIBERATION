"""Application web Boutique Liberation avec authentification administrateur."""
import hashlib
import hmac
import os
import secrets

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "false").lower() == "true",
    JSON_AS_ASCII=False,
)

# Mot de passe stocké sous forme de hash PBKDF2-SHA256, jamais en clair.
ADMIN_USERNAME = "david"
PASSWORD_HASH = "pbkdf2_sha256$600000$28fbd5d675d4fc03836c9eb91f4fd1d7$a414bd8aa8754f48c94aac857f36e76b242f53a655e7657654647c6b8fe7add2"


def verify_password(password):
    """Compare le mot de passe fourni au hash enregistré."""
    algorithm, iterations, salt, expected = PASSWORD_HASH.split("$")
    if algorithm != "pbkdf2_sha256":
        return False
    actual = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iterations)
    ).hex()
    return hmac.compare_digest(actual, expected)


@app.before_request
def require_login():
    """Protège l'espace de gestion et laisse accessibles login, santé et fichiers statiques."""
    if request.endpoint in {"login", "health", "static"}:
        return None
    if not session.get("authenticated"):
        return redirect(url_for("login", next=request.path))
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    """Authentifie l'administrateur."""
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if hmac.compare_digest(username, ADMIN_USERNAME) and verify_password(password):
            session.clear()
            session["authenticated"] = True
            session["username"] = ADMIN_USERNAME
            return redirect(url_for("index"))
        error = "Nom d'utilisateur ou mot de passe incorrect."
    return render_template("login.html", error=error)


@app.post("/logout")
def logout():
    """Ferme la session administrateur."""
    session.clear()
    return redirect(url_for("login"))


@app.get("/")
def index():
    """Affiche l'interface de gestion et la boutique client."""
    return render_template("index.html")


@app.get("/health")
def health():
    """Vérifie que le serveur répond correctement."""
    return jsonify({"status": "ok", "application": "BOUTIQUE LIBERATION"})


@app.errorhandler(404)
def not_found(_error):
    return render_template("index.html"), 404


if __name__ == "__main__":
    # Pour le développement local uniquement. En production, définir FLASK_SECRET_KEY.
    app.run(host="0.0.0.0", port=5000, debug=False)
