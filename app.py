import os
import sqlite3
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "boutique.db")
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deployment")

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'admin'
    );
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
        category TEXT NOT NULL, color TEXT DEFAULT '', purchase_price REAL NOT NULL DEFAULT 0,
        sale_price REAL NOT NULL DEFAULT 0, image_url TEXT DEFAULT '',
        description TEXT DEFAULT '', created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        size TEXT NOT NULL, quantity INTEGER NOT NULL DEFAULT 0,
        UNIQUE(product_id, size)
    );
    CREATE TABLE IF NOT EXISTS movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id),
        size TEXT NOT NULL, quantity INTEGER NOT NULL, kind TEXT NOT NULL,
        reason TEXT DEFAULT '', created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT NOT NULL,
        phone TEXT DEFAULT '', total REAL NOT NULL, payment_method TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
        product_id INTEGER NOT NULL REFERENCES products(id),
        size TEXT NOT NULL, quantity INTEGER NOT NULL, unit_price REAL NOT NULL
    );
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
        phone TEXT DEFAULT '', email TEXT DEFAULT '', address TEXT DEFAULT ''
    );
    """)
    # Compte de démonstration : à changer avant toute mise en ligne.
    conn.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES(?,?,?)",
                 ("admin", "admin123", "admin"))
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        samples = [
            ("Sneakers Urban", "Homme", "Blanc", 18, 35, "", "Chaussure urbaine"),
            ("Basket Élégance", "Femme", "Noir", 20, 39, "", "Style quotidien"),
            ("Sport Runner", "Sport", "Bleu", 22, 42, "", "Chaussure de sport"),
            ("Mocassin Classic", "Cuir", "Marron", 25, 48, "", "Chaussure classique")
        ]
        for p in samples:
            cur = conn.execute("INSERT INTO products(name,category,color,purchase_price,sale_price,image_url,description) VALUES(?,?,?,?,?,?,?)", p)
            for size in ("38","39","40","41","42","43"):
                conn.execute("INSERT INTO stock(product_id,size,quantity) VALUES(?,?,?)", (cur.lastrowid,size,2))
    conn.commit()
    conn.close()

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper

@app.context_processor
def inject_globals():
    return {"current_year": datetime.now().year}

@app.route("/")
def index():
    term = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    sql = """SELECT p.*, COALESCE(SUM(s.quantity),0) AS total_stock
             FROM products p LEFT JOIN stock s ON s.product_id=p.id WHERE 1=1"""
    args = []
    if term:
        sql += " AND (p.name LIKE ? OR p.category LIKE ? OR p.color LIKE ?)"
        args += [f"%{term}%"] * 3
    if category:
        sql += " AND p.category=?"
        args.append(category)
    sql += " GROUP BY p.id ORDER BY p.id DESC"
    products = db().execute(sql, args).fetchall()
    sizes = db().execute("SELECT product_id,size,quantity FROM stock ORDER BY size").fetchall()
    by_product = {}
    for row in sizes:
        by_product.setdefault(row["product_id"], []).append(row)
    return render_template("index.html", products=products, sizes=by_product, q=term, category=category)


@app.route("/acheter/<int:product_id>", methods=["POST"])
def buy_product(product_id):
    """Permet au client de commander directement depuis le catalogue public."""
    conn = db()
    try:
        size = request.form.get("size", "").strip()
        qty = int(request.form.get("quantity", "1"))
        customer = request.form.get("customer_name", "").strip() or "Client en ligne"
        phone = request.form.get("phone", "").strip()
        payment = request.form.get("payment_method", "Paiement à la livraison")
        allowed_payments = ("Espèces", "Airtel Money", "Orange Money", "M-Pesa", "Paiement à la livraison")
        if qty < 1 or payment not in allowed_payments or not size:
            raise ValueError("Vérifie la pointure, la quantité et le mode de paiement.")
        product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
        stock_row = conn.execute(
            "SELECT quantity FROM stock WHERE product_id=? AND size=?",
            (product_id, size)
        ).fetchone()
        if not product or not stock_row or stock_row["quantity"] < qty:
            raise ValueError("Cette pointure n'est pas disponible en quantité suffisante.")
        total = product["sale_price"] * qty
        cur = conn.execute(
            "INSERT INTO sales(customer_name,phone,total,payment_method) VALUES(?,?,?,?)",
            (customer, phone, total, payment)
        )
        conn.execute(
            "INSERT INTO sale_items(sale_id,product_id,size,quantity,unit_price) VALUES(?,?,?,?,?)",
            (cur.lastrowid, product_id, size, qty, product["sale_price"])
        )
        conn.execute(
            "UPDATE stock SET quantity=quantity-? WHERE product_id=? AND size=?",
            (qty, product_id, size)
        )
        conn.execute(
            "INSERT INTO movements(product_id,size,quantity,kind,reason) VALUES(?,?,?,?,?)",
            (product_id, size, qty, "SORTIE", "Commande client en ligne #" + str(cur.lastrowid))
        )
        conn.commit()
        flash("Commande enregistrée avec succès ! Votre numéro de commande est #" + str(cur.lastrowid), "success")
    except (ValueError, KeyError, sqlite3.Error) as exc:
        conn.rollback()
        flash(str(exc) or "Impossible d'enregistrer la commande.", "error")
    return redirect(url_for("index") + "#catalogue")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = db().execute("SELECT * FROM users WHERE username=? AND password=?",
                            (request.form.get("username",""), request.form.get("password",""))).fetchone()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(request.args.get("next") or url_for("dashboard"))
        flash("Identifiants incorrects.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin")
@login_required
def dashboard():
    conn = db()
    products_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    stock_count = conn.execute("SELECT COALESCE(SUM(quantity),0) FROM stock").fetchone()[0]
    today = datetime.now().strftime("%Y-%m-%d")
    today_sales = conn.execute("SELECT COUNT(*) FROM sales WHERE date(created_at)=?", (today,)).fetchone()[0]
    revenue = conn.execute("SELECT COALESCE(SUM(total),0) FROM sales WHERE date(created_at)=?", (today,)).fetchone()[0]
    low_stock = conn.execute("""SELECT p.name,s.size,s.quantity FROM stock s JOIN products p ON p.id=s.product_id
                                WHERE s.quantity<=2 ORDER BY s.quantity,p.name LIMIT 12""").fetchall()
    recent = conn.execute("SELECT * FROM sales ORDER BY id DESC LIMIT 8").fetchall()
    return render_template("admin.html", products_count=products_count, stock_count=stock_count,
                           today_sales=today_sales, revenue=revenue, low_stock=low_stock, recent=recent)

@app.route("/admin/products", methods=["GET","POST"])
@login_required
def products():
    conn = db()
    if request.method == "POST":
        name = request.form.get("name","").strip()
        category = request.form.get("category","Homme")
        try:
            purchase = float(request.form.get("purchase_price",0))
            price = float(request.form.get("sale_price",0))
            if not name or purchase < 0 or price < 0: raise ValueError()
            cur = conn.execute("""INSERT INTO products(name,category,color,purchase_price,sale_price,image_url,description)
                                  VALUES(?,?,?,?,?,?,?)""",
                               (name,category,request.form.get("color",""),purchase,price,
                                request.form.get("image_url",""),request.form.get("description","")))
            for size in request.form.getlist("sizes"):
                qty = max(0, int(request.form.get("qty_"+size,0) or 0))
                conn.execute("INSERT INTO stock(product_id,size,quantity) VALUES(?,?,?)", (cur.lastrowid,size,qty))
                if qty:
                    conn.execute("INSERT INTO movements(product_id,size,quantity,kind,reason) VALUES(?,?,?,?,?)",
                                 (cur.lastrowid,size,qty,"ENTREE","Stock initial"))
            conn.commit()
            flash("Produit ajouté avec succès.", "success")
            return redirect(url_for("products"))
        except (ValueError, sqlite3.Error):
            conn.rollback()
            flash("Vérifie les informations et les quantités saisies.", "error")
    items = conn.execute("""SELECT p.*,COALESCE(SUM(s.quantity),0) total_stock FROM products p
                            LEFT JOIN stock s ON s.product_id=p.id GROUP BY p.id ORDER BY p.id DESC""").fetchall()
    return render_template("products.html", products=items)

@app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    db().execute("DELETE FROM products WHERE id=?", (product_id,))
    db().commit()
    flash("Produit supprimé.", "success")
    return redirect(url_for("products"))

@app.route("/admin/stock", methods=["GET","POST"])
@login_required
def stock_page():
    conn = db()
    if request.method == "POST":
        try:
            product_id = int(request.form["product_id"])
            size = request.form["size"].strip()
            qty = int(request.form["quantity"])
            kind = request.form["kind"]
            if qty <= 0 or kind not in ("ENTREE","SORTIE"): raise ValueError()
            row = conn.execute("SELECT quantity FROM stock WHERE product_id=? AND size=?", (product_id,size)).fetchone()
            current = row["quantity"] if row else 0
            if kind == "SORTIE" and current < qty:
                flash("Stock insuffisant pour cette sortie.", "error")
            else:
                new_qty = current + qty if kind == "ENTREE" else current - qty
                conn.execute("""INSERT INTO stock(product_id,size,quantity) VALUES(?,?,?)
                                ON CONFLICT(product_id,size) DO UPDATE SET quantity=excluded.quantity""",
                             (product_id,size,new_qty))
                conn.execute("INSERT INTO movements(product_id,size,quantity,kind,reason) VALUES(?,?,?,?,?)",
                             (product_id,size,qty,kind,request.form.get("reason","")))
                conn.commit()
                flash("Mouvement de stock enregistré.", "success")
        except (ValueError, KeyError, sqlite3.Error):
            conn.rollback()
            flash("Données de mouvement invalides.", "error")
        return redirect(url_for("stock_page"))
    rows = conn.execute("""SELECT s.*,p.name,p.category FROM stock s JOIN products p ON p.id=s.product_id
                           ORDER BY p.name,s.size""").fetchall()
    products_list = conn.execute("SELECT id,name FROM products ORDER BY name").fetchall()
    movements = conn.execute("""SELECT m.*,p.name FROM movements m JOIN products p ON p.id=m.product_id
                                ORDER BY m.id DESC LIMIT 20""").fetchall()
    return render_template("stock.html", stock=rows, products=products_list, movements=movements)

@app.route("/admin/sales", methods=["GET","POST"])
@login_required
def sales_page():
    conn = db()
    if request.method == "POST":
        try:
            product_id = int(request.form["product_id"])
            size = request.form["size"]
            qty = int(request.form["quantity"])
            customer = request.form.get("customer_name","").strip() or "Client comptoir"
            phone = request.form.get("phone","")
            payment = request.form["payment_method"]
            product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
            stock_row = conn.execute("SELECT quantity FROM stock WHERE product_id=? AND size=?", (product_id,size)).fetchone()
            if not product or not stock_row or qty <= 0 or stock_row["quantity"] < qty:
                raise ValueError("Stock insuffisant ou produit invalide.")
            total = product["sale_price"] * qty
            cur = conn.execute("INSERT INTO sales(customer_name,phone,total,payment_method) VALUES(?,?,?,?)",
                               (customer,phone,total,payment))
            conn.execute("INSERT INTO sale_items(sale_id,product_id,size,quantity,unit_price) VALUES(?,?,?,?,?)",
                         (cur.lastrowid,product_id,size,qty,product["sale_price"]))
            conn.execute("UPDATE stock SET quantity=quantity-? WHERE product_id=? AND size=?", (qty,product_id,size))
            conn.execute("INSERT INTO movements(product_id,size,quantity,kind,reason) VALUES(?,?,?,?,?)",
                         (product_id,size,qty,"SORTIE","Vente #"+str(cur.lastrowid)))
            conn.commit()
            flash("Vente enregistrée. Le stock a été actualisé.", "success")
            return redirect(url_for("sales_page"))
        except (ValueError, KeyError, sqlite3.Error) as exc:
            conn.rollback()
            flash(str(exc) or "Impossible d'enregistrer cette vente.", "error")
    sales_list = conn.execute("SELECT * FROM sales ORDER BY id DESC LIMIT 30").fetchall()
    products_list = conn.execute("SELECT id,name,sale_price FROM products ORDER BY name").fetchall()
    return render_template("sales.html", sales=sales_list, products=products_list)

@app.route("/admin/invoice/<int:sale_id>")
@login_required
def invoice(sale_id):
    sale = db().execute("SELECT * FROM sales WHERE id=?", (sale_id,)).fetchone()
    if not sale: abort(404)
    items = db().execute("""SELECT si.*,p.name FROM sale_items si JOIN products p ON p.id=si.product_id
                            WHERE si.sale_id=?""", (sale_id,)).fetchall()
    return render_template("invoice.html", sale=sale, items=items)

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=True)
