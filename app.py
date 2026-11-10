from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"
DB_PATH = Path(__file__).resolve().parent / "boutique_liberation.db"

def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db_conn() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL,
            categorie TEXT NOT NULL, prix REAL NOT NULL, pointure TEXT DEFAULT '',
            quantite INTEGER NOT NULL DEFAULT 0, description TEXT DEFAULT '')""")
        if db.execute("SELECT COUNT(*) FROM produits").fetchone()[0] == 0:
            db.executemany("""INSERT INTO produits(nom,categorie,prix,pointure,quantite,description)
                VALUES(?,?,?,?,?,?)""", [
                ("Sneakers Urban","Homme",45,"40-45",8,"Sneakers confortables pour le quotidien."),
                ("Escarpins Élégance","Femme",38,"36-40",5,"Une touche élégante pour vos sorties."),
                ("Sport Runner","Sport",52,"39-45",2,"Chaussures légères pour vos activités."),
                ("Classique Cuir","Homme",65,"40-44",0,"Chaussures classiques en cuir.")])

@app.route("/")
def index():
    with db_conn() as db:
        produits = db.execute("SELECT * FROM produits ORDER BY id DESC").fetchall()
    return render_template("index.html", produits=produits)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        nom=request.form.get("nom","").strip()
        categorie=request.form.get("categorie","").strip()
        try:
            prix=float(request.form.get("prix","0"))
            quantite=int(request.form.get("quantite","0"))
        except ValueError:
            flash("Prix ou quantité invalide.","error")
            return redirect(url_for("admin"))
        if not nom or not categorie or prix < 0 or quantite < 0:
            flash("Veuillez remplir correctement les champs obligatoires.","error")
            return redirect(url_for("admin"))
        with db_conn() as db:
            db.execute("""INSERT INTO produits(nom,categorie,prix,pointure,quantite,description)
                VALUES(?,?,?,?,?,?)""",(nom,categorie,prix,request.form.get("pointure",""),quantite,request.form.get("description","")))
        flash("Produit ajouté avec succès.","success")
        return redirect(url_for("admin"))
    with db_conn() as db:
        produits=db.execute("SELECT * FROM produits ORDER BY id DESC").fetchall()
        stats={"produits":db.execute("SELECT COUNT(*) FROM produits").fetchone()[0],
               "stock":db.execute("SELECT COALESCE(SUM(quantite),0) FROM produits").fetchone()[0],
               "ruptures":db.execute("SELECT COUNT(*) FROM produits WHERE quantite=0").fetchone()[0]}
    return render_template("admin.html",produits=produits,stats=stats)

@app.post("/admin/produit/<int:produit_id>/supprimer")
def supprimer_produit(produit_id):
    with db_conn() as db:
        db.execute("DELETE FROM produits WHERE id=?",(produit_id,))
    flash("Produit supprimé.","success")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1",port=5001,debug=True)
