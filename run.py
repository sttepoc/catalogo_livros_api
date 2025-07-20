from flask import Flask, send_from_directory
from app import create_app
import os

app = create_app()

# Configura caminho absoluto para o diretório frontend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend_api')

# Rota principal redireciona para login
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# Rota para servir arquivos HTML
@app.route('/<page>.html')
def html_page(page):
    return send_from_directory(FRONTEND_DIR, f'{page}.html')

# Rota para servir arquivos estáticos (JS, CSS, etc)
@app.route('/frontend_api/<path:filename>')
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == '__main__':
    app.run(debug=False)