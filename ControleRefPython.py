from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

# Conexão com banco de dados
conn = sqlite3.connect('refeitorio.db', check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela
cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    data TEXT,
    status TEXT
)''')
conn.commit()

# Rota principal para carregar o HTML
@app.route('/')
def home():
    try:
        return render_template('ControleRefeitorio.html')
    except Exception as e:
        return f"Erro ao carregar o template: {str(e)}"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        qr_data = eval(data['qr_data'])
        id_func = qr_data['id']
        nome = qr_data['name']
        data_atual = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('SELECT * FROM registros WHERE id = ? AND data = ?', (id_func, data_atual))
        if cursor.fetchone():
            return jsonify({"message": f"{nome} já registrado hoje."})
        else:
            cursor.execute('INSERT INTO registros (id, nome, data, status) VALUES (?, ?, ?, ?)', 
                           (id_func, nome, data_atual, 'Sim'))
            conn.commit()
            return jsonify({"message": f"{nome} registrado com sucesso."})
    except Exception as e:
        return jsonify({"message": "Erro ao processar QR Code."})

@app.route('/export', methods=['GET'])
def export():
    registros = pd.read_sql_query("SELECT * FROM registros", conn)
    registros.to_excel('registros_refeitorio.xlsx', index=False)
    return jsonify({"message": "Dados exportados para Excel."})

if __name__ == '__main__':
    app.run(debug=True)
