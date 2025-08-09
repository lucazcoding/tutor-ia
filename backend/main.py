from flask import Flask
import sys
import os


# Adiciona o diretório raiz (onde está o frontend/) ao sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "SUA_CHAVE_SECRETA_MUITO_FORTE_AQUI_PARA_SEGURANCA_DAS_SESSOES")




from frontend.routes import configure_routes


configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
