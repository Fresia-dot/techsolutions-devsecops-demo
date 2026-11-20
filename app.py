"""Aplicación de demostración (versión VULNERABLE a propósito).

Úsala solo en tu repositorio de práctica. Las demos la corrigen paso a paso.
"""
import os
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
DB = os.environ.get("DB_PATH", "demo.db")


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
    con = sqlite3.connect(DB)
    # VULNERABLE (Demo 2): consulta construida concatenando la entrada del usuario
    fila = con.execute(f"SELECT id, nombre FROM clientes WHERE id = {cid}").fetchone()
    con.close()
    return jsonify(fila)


if __name__ == "__main__":
    init_db()
    # VULNERABLE (Demo 2): modo debug activo y escuchando en todas las interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
