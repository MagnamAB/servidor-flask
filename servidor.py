from flask import Flask, jsonify
import requests
import os

# Configuración de Flask
app = Flask(__name__)

# Credenciales de WordPress (Usar variables de entorno para seguridad)
USUARIO = os.environ.get("WP_USER", "RS_admin21")
PASSWORD = os.environ.get("WP_PASSWORD", "86Uv iN27 RwS7 46sp IJqS d774")
URL = os.environ.get("WP_API_URL", "https://www.renovarser.com/wp-json/wp/v2/pages")

# Ruta raíz para verificar que el servidor está activo
@app.route('/')
def home():
    return jsonify({"status": "success", "message": "El servidor Flask está activo 🚀"})

# Endpoint para obtener la lista de páginas de WordPress
@app.route('/paginas', methods=['GET'])
def obtener_paginas():
    try:
        response = requests.get(URL, auth=(USUARIO, PASSWORD))
        if response.status_code == 200:
            paginas = response.json()
            datos_paginas = [{"id": p["id"], "titulo": p["title"]["rendered"]} for p in paginas]
            return jsonify({"status": "success", "paginas": datos_paginas})
        return jsonify({"status": "error", "message": "No se pudo obtener las páginas"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint para obtener una página específica por su ID
@app.route('/pagina/<int:id>', methods=['GET'])
def obtener_contenido_pagina(id):
    try:
        response = requests.get(f"{URL}/{id}", auth=(USUARIO, PASSWORD))
        if response.status_code == 200:
            pagina = response.json()
            return jsonify({
                "status": "success",
                "id": pagina["id"],
                "titulo": pagina["title"]["rendered"],
                "contenido": pagina["content"]["rendered"]
            })
        return jsonify({"status": "error", "message": "Página no encontrada"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Ejecutar el servidor en Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
