"""Application web Boutique Liberation : vitrine publique et administration protégée."""
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

ADMIN_USERNAME = "david"
PASSWORD_HASH = "pbkdf2_sha256$600000$28fbd5d675d4fc03836c9eb91f4fd1d7$a414bd8aa8754f48c94aac857f36e76b242f53a655e7657654647c6b8fe7add2"


def verify_password(password):
    algorithm, iterations, salt, expected = PASSWORD_HASH.split("$")
    if algorithm != "pbkdf2_sha256":
        return False
    actual = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iterations)
    ).hex()
    return hmac.compare_digest(actual, expected)


@app.before_request
def require_admin_login():
    """La vitrine est publique ; seules les routes d'administration exigent une session."""
    if request.endpoint in {"store", "login", "health", "static"}:
        return None
    if request.endpoint == "admin" and not session.get("authenticated"):
        return redirect(url_for("login", next=request.path))
    return None


@app.get("/")
def store():
    """Vitrine publique accessible sans connexion."""
    return render_template("store.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        access_code = request.form.get("access_code", "")
        if verify_password(access_code):
            session.clear()
            session["authenticated"] = True
            session["username"] = ADMIN_USERNAME
            destination = request.form.get("next", "")
            if not destination.startswith("/admin"):
                destination = url_for("admin")
            return redirect(destination)
        error = "Nom d'utilisateur ou mot de passe incorrect."
    return render_template("login.html", error=error, next=request.args.get("next", ""))


@app.get("/admin")
def admin():
    """Interface de gestion réservée à l'administrateur."""
    return render_template("index.html")


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("store"))


@app.get("/health")
def health():
    return jsonify({"status": "ok", "application": "BOUTIQUE LIBERATION"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
