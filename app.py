from flask import Flask, render_template, request, jsonify
from src.config import AppConfig
from src.rag import PersonalRAG
from src.roles import get_role

app = Flask(__name__)
config = AppConfig()

# Diccionario de respaldo por si get_role espera texto directo
ROLE_MAP = {
    1: "reclutador",
    2: "cliente potencial",
    3: "estudiante",
    4: "colega profesional",
    5: "público general"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    
    # 1. Limpieza estricta de la pregunta para que sea string puro
    pregunta = str(data.get("pregunta", "")).strip()
    if not pregunta:
        return jsonify({"respuesta": "Por favor, escribe una pregunta válida."})
    
    # 2. Manejo seguro del rol (mapeando el número del select a texto o ID según requiera src/roles.py)
    try:
        role_raw = int(data.get("rol", 5))
    except (ValueError, TypeError):
        role_raw = 5
        
    # Intentamos obtener el rol usando la función original o el respaldo
    try:
        role_data = get_role(role_raw)
    except Exception:
        # Si get_role falla con enteros, probamos pasándole el texto del rol
        role_name = ROLE_MAP.get(role_raw, "público general")
        try:
            role_data = get_role(role_name)
        except Exception:
            role_data = {"name": role_name, "description": "Público general"}

    try:
        rag_system = PersonalRAG(config)
        resultado = rag_system.ask(pregunta, role_data)
        rag_system.close()
        
        respuesta_texto = resultado.get("answer", "No se pudo obtener una respuesta.")
    except Exception as e:
        respuesta_texto = f"Error interno en el RAG: {str(e)}"
        
    return jsonify({"respuesta": respuesta_texto})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)