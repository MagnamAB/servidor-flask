from flask import Flask, jsonify
import requests
import os

# Configuración de Flask
app = Flask(__name__)

# Credenciales de WordPress
USUARIO = "RS_admin21"
PASSWORD = "86Uv iN27 RwS7 46sp IJqS d774"

# URL de la API de WordPress
URL = "https://www.renovarser.com/wp-json/wp/v2/pages"

@app.route('/')  # 👈 Nueva ruta raíz para evitar el error 404
def home():
    return jsonify({"status": "success", "message": "El servidor Flask está activo 🚀"})

@app.route('/paginas', methods=['GET'])
def obtener_paginas():
    """
    Endpoint para obtener la lista de páginas publicadas en WordPress.
    """
    try:
        response = requests.get(URL, auth=(USUARIO, PASSWORD))
        if response.status_code == 200:
            paginas = response.json()
            
            # Crear una lista con los títulos e IDs de las páginas
            datos_paginas = [{"id": p["id"], "titulo": p["title"]["rendered"]} for p in paginas]
            
            return jsonify({"status": "success", "paginas": datos_paginas})
        else:
            return jsonify({"status": "error", "message": "No se pudo obtener las páginas"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Ejecutar el servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
