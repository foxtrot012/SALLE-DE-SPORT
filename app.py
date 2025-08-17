from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---- Initialisation de la base de données ----
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    telephone TEXT,
                    abonnement TEXT,
                    date_inscription TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# ---- Page d’accueil : liste des clients ----
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    clients = c.fetchall()
    conn.close()
    return render_template("index.html", clients=clients)

# ---- Ajouter un client ----
@app.route("/add", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        telephone = request.form["telephone"]
        abonnement = request.form["abonnement"]
        date_inscription = request.form["date_inscription"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO clients (nom, prenom, telephone, abonnement, date_inscription) VALUES (?, ?, ?, ?, ?)",
                  (nom, prenom, telephone, abonnement, date_inscription))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_client.html")

# ---- Supprimer un client ----
@app.route("/delete/<int:id>")
def delete_client(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM clients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
