"""Versión CORREGIDA de app.py (cópiala sobre app.py en la Demo 2)."""
import os
import sqlite3

from flask import Flask, abort, jsonify, request

app = Flask(__name__)
DB = os.environ.get("DB_PATH", "demo.db")
# El secreto se lee del entorno (GitHub Secrets o gestor de secretos), nunca del código
API_KEY = os.environ.get("API_KEY")


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nombre TEXT)")
    con.execute("INSERT OR IGNORE INTO clientes VALUES (1, 'Cliente Demo SAC')")
    con.commit()
    con.close()


@app.route("/")
def index():
    return "TechSolutions demo OK"


@app.route("/cliente")
def cliente():
    cid = request.args.get("id", "1")
    if not cid.isdigit():  # validación de entrada con lista permitida
        abort(400)
    con = sqlite3.connect(DB)
    # SEGURO: consulta parametrizada
    fila = con.execute("SELECT id, nombre FROM clientes WHERE id = ?", (int(cid),)).fetchone()
    con.close()
    return jsonify(fila)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
