from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde Vercel
CORS(app)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Tablas básicas
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS productos (id INTEGER KEY, codigo TEXT UNIQUE, nombre TEXT, stock INTEGER)')
    # Datos de prueba
    c.execute("INSERT OR IGNORE INTO usuarios (id, username, password) VALUES (1, 'admin', '1234')")
    c.execute("INSERT OR IGNORE INTO productos (id, codigo, nombre, stock) VALUES (1, 'P001', 'Laptop', 10)")
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET'])
def index():
    return jsonify({"mensaje": "El backend de la API está en línea y funcionando correctamente."})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (data['username'], data['password']))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({"status": "success", "message": "Login OK"})
    return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

@app.route('/api/buscar_producto', methods=['POST'])
def buscar_producto():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos WHERE codigo=?", (data['codigo'],))
    prod = c.fetchone()
    conn.close()
    
    if prod:
        return jsonify({"codigo": prod[1], "nombre": prod[2], "stock": prod[3]})
    return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)