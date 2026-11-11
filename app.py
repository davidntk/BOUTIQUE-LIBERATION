"""Application web Boutique Liberation — interface Flask."""
from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


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
    # Pour le développement local uniquement. En production, utiliser un serveur WSGI.
    app.run(host="0.0.0.0", port=5000, debug=True)
