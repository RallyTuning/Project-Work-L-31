from flask import Flask, render_template, request, jsonify
# File con la logica (il Project Work) chiamato "simulatore.py"
from simulatore import main_controller 
import json

app = Flask(__name__)

# | ROTTA 1: LA HOMEPAGE (Il Sito Web) |
@app.route('/')
def home():
    # Cerca il file index.html nella cartella 'templates'
    return render_template('index.html')

# | ROTTA 2: L'API (Il Cervello) |
@app.route('/api/simula', methods=['POST'])
def api_simula():
    try:
        # 1. Ricevo i dati dal sito web (in formato JSON)
        dati_dal_frontend = request.get_json()
        
        # 2. Converto l'oggetto in stringa
        json_string = json.dumps(dati_dal_frontend)
        
        # 3. Chiamo la funzione di simulazione e passo il "json" come modalità e la stringa dati
        risposta_json_str = main_controller('json', json_string)
        
        # 4. Restituisco il risultato al sito web
        return jsonify(json.loads(risposta_json_str))
        
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == '__main__':
    # Avvia il server in locale sulla porta 5000
    print("// SERVER TIMPE SMART VINEYARD AVVIATO //")
    print("Apri il browser su: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
