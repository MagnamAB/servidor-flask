import requests

# Credenciales de WordPress
USUARIO = "RS_admin21"
PASSWORD = "86Uv iN27 RwS7 46sp IJqS d774"

# URL del endpoint de WordPress para obtener páginas
URL = "https://www.renovarser.com/wp-json/wp/v2/pages"

def obtener_paginas():
    """
    Función para obtener la lista de páginas con autenticación en la API de WordPress.
    """
    try:
        response = requests.get(URL, auth=(USUARIO, PASSWORD))  # Petición con autenticación
        if response.status_code == 200:
            paginas = response.json()  # Convertimos la respuesta a JSON
            print(f"🔹 Se encontraron {len(paginas)} páginas publicadas.\n")
            
            # Mostrar los títulos de las páginas
            for pagina in paginas:
                print(f"📄 {pagina['title']['rendered']} - ID: {pagina['id']}")
        
        else:
            print(f"❌ Error al obtener páginas: {response.status_code}")
    
    except Exception as e:
        print(f"⚠️ Ocurrió un error: {str(e)}")

# Llamamos a la función
obtener_paginas()

