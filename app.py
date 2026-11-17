import os
import mysql.connector
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Connexion MySQL locale (XAMPP).
MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "boutique_liberation")
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deployment")

class HybridRow(dict):
    def __getitem__(self, key):
        return list(self.values())[key] if isinstance(key, int) else super().__getitem__(key)

class CursorAdapter:
    def __init__(self, cursor):
        self.cursor = cursor
        self.lastrowid = cursor.lastrowid
    def fetchone(self):
        row = self.cursor.fetchone()
        return HybridRow(row) if row is not None else None
    def fetchall(self):
        return [HybridRow(row) for row in self.cursor.fetchall()]

class MySQLConnectionAdapter:
    def __init__(self, connection):
        self.connection = connection
    def execute(self, sql, params=()):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(sql.replace('?', '%s'), params)
        return CursorAdapter(cursor)
    def commit(self): self.connection.commit()
    def rollback(self): self.connection.rollback()
    def close(self): self.connection.close()

def db():
    if 'db' not in g:
        connection = mysql.connector.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
            password=MYSQL_PASSWORD, database=MYSQL_DATABASE, charset='utf8mb4', autocommit=False)
        g.db = MySQLConnectionAdapter(connection)
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()

def init_db():
    """Vérifie MySQL et ajoute des données de démonstration si la base est vide.
    Importez d'abord database/schema_mysql.sql dans phpMyAdmin.
    """
    conn = db()
    try:
        conn.execute('INSERT IGNORE INTO users(username,password,role) VALUES(?,?,?)',
                     ('admin', 'admin123', 'admin'))
        count = conn.execute('SELECT COUNT(*) AS total FROM products').fetchone()['total']
        if count == 0:
            samples = [
                ('Sneakers Urban', 'Homme', 'Blanc', 18, 35, '', 'Chaussure urbaine'),
                ('Basket Élégance', 'Femme', 'Noir', 20, 39, '', 'Style quotidien'),
                ('Sport Runner', 'Sport', 'Bleu', 22, 42, '', 'Chaussure de sport'),
                ('Mocassin Classic', 'Homme', 'Marron', 25, 48, 'https://acdn-us.mitiendanube.com/stores/001/668/651/products/202206-copy-2-0455f59495a5a18afd17209011273156-1024-1024.webp', 'Chaussure classique')
            ]
            for product in samples:
                cur = conn.execute('INSERT INTO products(name,category,color,purchase_price,sale_price,image_url,description) VALUES(?,?,?,?,?,?,?)', product)
                for size in ('38', '39', '40', '41', '42', '43'):
                    conn.execute('INSERT INTO stock(product_id,size,quantity) VALUES(?,?,?)', (cur.lastrowid, size, 2))

        # Catalogue mode/vêtements repris du fichier index.html de référence.
        # Insertion idempotente : ne remplace jamais les produits déjà gérés.
        catalogue = [
            ("Polo classique premium", "Homme", "Selon modèle", 22, "https://thelondongentlemen.com/cdn/shop/files/ChatGPT_Image_Apr_16_2026_03_41_51_PM_92ee7286-b074-427f-b8d6-07907414a71b.png?v=1776336381&width=1024", "Polo premium pour homme"),
            ("Chemise élégance", "Homme", "Selon modèle", 29, "https://www.principedifirenze.com/cdn/shop/collections/image-copertina-collezioni-camicie_1200x1200.jpg?v=1693488806", "Chemise élégante pour homme"),
            ("Polo signature", "Homme", "Selon modèle", 25, "https://www.charlestyrwhitt.com/dw/image/v2/AAWJ_PRD/on/demandware.static/-/Sites-ctshirts-master/default/dw1dbce53f/hi-res/JEP0398OLV_FOLD_SINGLE.jpg?sh=1200&sw=960", "Polo signature"),
            ("Pantalon coupe droite", "Homme", "Selon modèle", 34, "https://themodernobserver.com/_next/image?q=75&url=https%3A%2F%2Fthe-modern-observer-v2.s3.us-east-1.amazonaws.com%2Fstyle%2Fsmart-casual-outfit-for-men.jpg%3Fauto%3Dformat%26fit%3Dcrop%26w%3D800%26q%3D80&w=3840", "Pantalon coupe droite"),
            ("Jean denim essentiel", "Homme", "Denim", 38, "https://www.andsons.us/cdn/shop/files/Jeans_Brandon_Indigo_Wash_FLATLAY_1.png?v=1770119486&width=640", "Jean denim"),
            ("Tissu imprimé premium", "Homme", "Imprimé", 18, "https://shopbesida.com/cdn/shop/products/KeeyaWrapSkirt6.jpg?v=1669471624", "Tissu imprimé premium"),
            ("Chaussures urbaines", "Chaussures", "Selon modèle", 49, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=85", "Chaussures urbaines pour homme"),
            ("Veste en cuir urbaine", "Cuir", "Noir", 89, "https://img.guess.com/image/upload/f_auto%2Cq_auto%2Cfl_strip_profile%2Cw_800%2Cc_scale/v1/NA/Style/ECOMM/M2YL12L0QN0-JBLK-ALT1", "Veste en cuir"),
            ("Robe chic", "Femme", "Selon modèle", 42, "https://www.shopzuri.com/cdn/shop/files/ZuriMay2023-8648.jpg?v=1694727984&width=1200", "Robe chic pour femme"),
            ("Pagne élégant", "Femme", "Imprimé", 24, "https://i.ebayimg.com/images/g/F3YAAeSwRqFomCTv/s-l1200.jpg", "Pagne élégant"),
            ("Jupe moderne", "Femme", "Selon modèle", 27, "https://i.pinimg.com/originals/2b/cb/13/2bcb137423b0ab7747207d47ab109a63.jpg", "Jupe moderne"),
            ("Polo femme", "Femme", "Selon modèle", 20, "https://img.staticdj.com/114f431c819b1bc0f8c479ec78ccae6d_1080x.jpg", "Polo pour femme"),
            ("Body seconde peau", "Femme", "Selon modèle", 19, "https://static.riachuelo.com.br/RCHLO/12366013001/portrait/body-cache-coeur-12366013_foto4_corpo.jpg", "Body seconde peau"),
            ("Escarpins élégants", "Chaussures", "Selon modèle", 46, "https://iubitoeg.com/public/uploads/all/f4rbd2TRc10zl0aCxMZcGJQe1lwmYYpdFAgJrP1d.jpg", "Escarpins élégants"),
            ("Baskets tendance", "Sport", "Selon modèle", 55, "https://cdn11.bigcommerce.com/s-21x65e8kfn/images/stencil/original/products/42957/192937/NEW694086_1000_6__99743.1688469678.jpg", "Baskets tendance"),
            ("Sneakers New Balance", "Sport", "Selon modèle", 78, "https://cdn11.bigcommerce.com/s-21x65e8kfn/images/stencil/original/products/75255/390406/NEW695842_1000_13__58538.1737390021.jpg", "Sneakers New Balance")
        ]
        for name, category, color, price, image_url, description in catalogue:
            exists = conn.execute("SELECT id FROM products WHERE name=?", (name,)).fetchone()
            if exists:
                continue
            cur = conn.execute(
                """INSERT INTO products(name,category,color,purchase_price,sale_price,image_url,description)
                   VALUES(?,?,?,?,?,?,?)""",
                (name, category, color, 0, price, image_url, description)
            )
            available_sizes = (
                ('36','37','38','39','40','41','42','43','44','45')
                if category in ('Chaussures','Sport') or name == "Chaussures urbaines"
                else ('Unique',) if name == "Tissu imprimé premium" or name == "Pagne élégant"
                else ('XS','S','M','L','XL','XXL')
            )
            for size in available_sizes:
                # Stock à zéro : le gérant saisit les quantités réelles avant la vente.
                conn.execute(
                    "INSERT INTO stock(product_id,size,quantity) VALUES(?,?,0)",
                    (cur.lastrowid, size)
                )
        # Harmonise le genre des articles du catalogue déjà présents en base.
        # Les chaussures spécifiquement féminines apparaissent dans Femme,
        # et les modèles masculins dans Homme.
        genre_corrections = {
            "Tissu imprimé premium": "Femme",
            "Polo femme": "Homme",
            "Chaussures urbaines": "Homme",
            "Veste en cuir urbaine": "Homme",
            "Escarpins élégants": "Femme",
            "Baskets tendance": "Femme",
            "Mocassin Classic": "Homme",
            "Sneakers Urban": "Homme",
            "Basket Élégance": "Femme"
        }
        for product_name, genre in genre_corrections.items():
            conn.execute("UPDATE products SET category=? WHERE name=?", (genre, product_name))

        # Restaure la photo du mocassin même si le produit existe déjà en base.
        conn.execute("""UPDATE products SET image_url=? WHERE name=? AND (image_url IS NULL OR image_url='')""",
                     ('https://acdn-us.mitiendanube.com/stores/001/668/651/products/202206-copy-2-0455f59495a5a18afd17209011273156-1024-1024.webp', 'Mocassin Classic'))

        # Attribue deux photos distinctes aux deux modèles de chaussures.
        # Mise à jour systématique pour corriger aussi les anciennes photos déjà enregistrées.
        conn.execute("UPDATE products SET image_url=? WHERE name=?",
                     ('https://images.unsplash.com/photo-1460353581641-37baddab0fa2?auto=format&fit=crop&w=900&q=85', 'Sport Runner'))
        conn.execute("UPDATE products SET image_url=? WHERE name=?",
                     ('https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=900&q=85', 'Sneakers Urban'))

        conn.commit()
    except mysql.connector.Error:
        conn.rollback()
        raise

def login_required(fn):
    """Accès admin sans mot de passe, à la demande du propriétaire du site."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Ouvre automatiquement une session administrateur.
        session.setdefault("user_id", "admin")
        session.setdefault("username", "admin")
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
    shoe_names = (
        'Chaussures urbaines', 'Escarpins élégants', 'Mocassin Classic',
        'Sneakers Urban', 'Basket Élégance', 'Sport Runner',
        'Baskets tendance', 'Sneakers New Balance'
    )
    sport_names = ('Sneakers Urban', 'Sport Runner', 'Baskets tendance', 'Sneakers New Balance')
    if category == "Chaussures":
        sql += " AND p.name IN ('Chaussures urbaines','Escarpins élégants','Mocassin Classic','Basket Élégance')"
    elif category == "Sport":
        sql += " AND p.name IN ('Sneakers Urban','Sport Runner','Baskets tendance','Sneakers New Balance')"
    elif category == "Cuir":
        sql += " AND (p.category='Cuir' OR p.name LIKE '%cuir%')"
    elif category in ("Homme", "Femme"):
        sql += " AND p.category=? AND p.name NOT IN (" + ",".join(["?"] * len(shoe_names)) + ")"
        args.extend([category, *shoe_names])
    elif category:
        sql += " AND p.category=?"
        args.append(category)
    sql += " GROUP BY p.id ORDER BY p.id DESC"
    products = db().execute(sql, args).fetchall()
    # Catégorie d'affichage dédiée : le champ historique category contient
    # aussi le genre pour certains produits, donc on classe les chaussures ici.
    display_categories = {
        "Chaussures urbaines": "Chaussures",
        "Escarpins élégants": "Chaussures",
        "Mocassin Classic": "Chaussures",
        "Basket Élégance": "Chaussures",
        "Sneakers Urban": "Sport",
        "Sport Runner": "Sport",
        "Baskets tendance": "Sport",
        "Sneakers New Balance": "Sport",
        "Veste en cuir urbaine": "Cuir"
    }
    for product in products:
        product["display_category"] = display_categories.get(product["name"], product["category"])
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
        if not product or not stock_row:
            raise ValueError("Ce produit ou cette taille n'existe pas.")
        # Si le stock est à zéro, enregistrer une commande sur demande sans
        # décrémenter l'inventaire. Si un stock positif existe, le respecter.
        order_on_request = stock_row["quantity"] == 0
        if stock_row["quantity"] > 0 and stock_row["quantity"] < qty:
            raise ValueError("Quantité supérieure au stock disponible.")
        total = product["sale_price"] * qty
        cur = conn.execute(
            "INSERT INTO sales(customer_name,phone,total,payment_method) VALUES(?,?,?,?)",
            (customer, phone, total, payment)
        )
        conn.execute(
            "INSERT INTO sale_items(sale_id,product_id,size,quantity,unit_price) VALUES(?,?,?,?,?)",
            (cur.lastrowid, product_id, size, qty, product["sale_price"])
        )
        if not order_on_request:
            conn.execute(
                "UPDATE stock SET quantity=quantity-? WHERE product_id=? AND size=?",
                (qty, product_id, size)
            )
            conn.execute(
                "INSERT INTO movements(product_id,size,quantity,kind,reason) VALUES(?,?,?,?,?)",
                (product_id, size, qty, "SORTIE", "Commande client en ligne #" + str(cur.lastrowid))
            )
        conn.commit()
        if order_on_request:
            flash("Demande de commande enregistrée ! Cette taille est à confirmer avec la boutique. Référence #" + str(cur.lastrowid), "success")
        else:
            flash("Commande enregistrée avec succès ! Votre numéro de commande est #" + str(cur.lastrowid), "success")
    except (ValueError, KeyError, mysql.connector.Error) as exc:
        conn.rollback()
        flash(str(exc) or "Impossible d'enregistrer la commande.", "error")
    return redirect(url_for("index") + "#catalogue")

@app.route("/login", methods=["GET","POST"])
def login():
    """Ancienne adresse de connexion : redirige désormais vers l'administration."""
    return redirect(url_for("dashboard"))

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
    today_sales = conn.execute("SELECT COUNT(*) FROM sales WHERE DATE(created_at)=?", (today,)).fetchone()[0]
    revenue = conn.execute("SELECT COALESCE(SUM(total),0) FROM sales WHERE DATE(created_at)=?", (today,)).fetchone()[0]
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
        except (ValueError, mysql.connector.Error):
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
                                ON DUPLICATE KEY UPDATE quantity=VALUES(quantity)""",
                             (product_id,size,new_qty))
                conn.execute("INSERT INTO movements(product_id,size,quantity,kind,reason) VALUES(?,?,?,?,?)",
                             (product_id,size,qty,kind,request.form.get("reason","")))
                conn.commit()
                flash("Mouvement de stock enregistré.", "success")
        except (ValueError, KeyError, mysql.connector.Error):
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
        except (ValueError, KeyError, mysql.connector.Error) as exc:
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
    with app.app_context():
        init_db()
    app.run(host="127.0.0.1", port=5001, debug=True)
