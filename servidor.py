from flask import Flask, jsonify
import requests
import os

# Configuración de Flask
app = Flask(__name__)

# Credenciales de WordPress (Se usan variables de entorno para mayor seguridad)
USUARIO = os.environ.get("WP_USER", "RS_admin21")
PASSWORD = os.environ.get("WP_PASSWORD", "86Uv iN27 RwS7 46sp IJqS d774")
BASE_URL = "https://www.renovarser.com/wp-json"
PAGES_URL = f"{BASE_URL}/wp/v2/pages"
CSS_URL = f"{BASE_URL}/customizer/v1/css"  # ✅ Ruta corregida para obtener el CSS correcto

@app.route("/")
def home():
    return jsonify({"status": "success", "message": "El servidor Flask está activo 🚀"})

@app.route("/paginas", methods=["GET"])
def obtener_paginas():
    """
    Obtiene la lista de páginas de WordPress.
    """
    try:
        response = requests.get(PAGES_URL, auth=(USUARIO, PASSWORD))
        if response.status_code == 200:
            paginas = response.json()
            datos_paginas = [{"id": p["id"], "titulo": p["title"]["rendered"]} for p in paginas]
            return jsonify({"status": "success", "paginas": datos_paginas})
        return jsonify({"status": "error", "message": "No se pudo obtener las páginas"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/pagina/<int:id>", methods=["GET"])
def obtener_contenido_pagina(id):
    """
    Obtiene el contenido de una página específica por ID.
    """
    try:
        response = requests.get(f"{PAGES_URL}/{id}", auth=(USUARIO, PASSWORD))
        if response.status_code == 200:
            pagina = response.json()
            return jsonify({
                "status": "success",
                "id": pagina["id"],
                "titulo": pagina["title"]["rendered"],
                "contenido": pagina["content"]["rendered"]
            })
        return jsonify({"status": "error", "message": "No se pudo obtener la página"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/pagina/nombre/<string:nombre>", methods=["GET"])
def obtener_contenido_por_nombre(nombre):
    """
    Obtiene el contenido de una página específica por su nombre.
    """
    try:
        response = requests.get(PAGES_URL, auth=(USUARIO, PASSWORD))
        if response.status_code == 200:
            paginas = response.json()
            for p in paginas:
                if p["title"]["rendered"].lower() == nombre.lower():
                    return jsonify({
                        "status": "success",
                        "id": p["id"],
                        "titulo": p["title"]["rendered"],
                        "contenido": p["content"]["rendered"]
                    })
        return jsonify({"status": "error", "message": "Página no encontrada"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/css", methods=["GET"])
def obtener_css():
    """
    Obtiene el CSS personalizado desde WordPress.
    """
    try:
        response = requests.get(CSS_URL, auth=(USUARIO, PASSWORD))
        if response.status_code == 200:
            css_data = response.json()
            return jsonify({
                "status": "success",
                "css": css_data.get("custom_css", "No hay CSS personalizado")
            })
        return jsonify({"status": "error", "message": "No se pudo obtener el CSS"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
