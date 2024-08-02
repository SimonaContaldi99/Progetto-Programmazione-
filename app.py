import pandas as pd
from flask import Flask, render_template, request
from calcolo_calorico import calcolo_bmr, calcola_tdee, ripartizione_calorica, crea_grafico_ripartizione

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcola', methods=['POST'])
def calcola():
    sesso = request.form['sesso']
    età = int(request.form['età'])
    altezza = float(request.form['altezza'])
    peso = float(request.form['peso'])
    livello_attività = int(request.form['livello_attività'])

    try:
        bmr = calcolo_bmr(sesso, peso, altezza, età)
        tdee = calcola_tdee(bmr, livello_attività)
        colazione, pranzo, cena, spuntino = ripartizione_calorica(tdee)

        # Creazione del grafico a torta
        crea_grafico_ripartizione(colazione, pranzo, cena, spuntino, 'static/grafico_ripartizione.png')

        # Lettura del file CSV
        df = pd.read_csv('ricette_passaggi.csv')

        # Filtrare le ricette per pasto e calorie
        def filtra_ricette(tipo, calorie_max):
            return df[(df['Tipo'] == tipo) & (df['Calorie'] <= calorie_max)].sample(3).to_dict(orient='records')

        # Giorni della settimana
        giorni_settimana = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']

        # Creazione delle ricette per ogni giorno della settimana
        menu_settimanale = {giorno: {
            'Colazione': filtra_ricette('Colazione', colazione),
            'Pranzo': filtra_ricette('Pranzo', pranzo),
            'Cena': filtra_ricette('Cena', cena),
            'Spuntino': filtra_ricette('Spuntino', spuntino)
        } for giorno in giorni_settimana}

        return render_template('risultato.html', 
                               bmr=bmr, tdee=tdee,
                               colazione=colazione, pranzo=pranzo, cena=cena, spuntino=spuntino,
                               menu_settimanale=menu_settimanale)
    
    except ValueError as e:
        error_message = str(e)
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
