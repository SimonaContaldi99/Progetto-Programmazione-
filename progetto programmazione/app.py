import pandas as pd
from flask import Flask, render_template, request
from calcolo_calorico import calcolo_bmr, calcola_tdee, calcola_bmi, valori_bmi, esercizio_fisico, ripartizione_calorica, crea_grafico_ripartizione, crea_grafico_ripartizione_barre
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Creazione directory
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcola', methods=['POST'])
def calcola():
    sesso = request.form['sesso']
    età = request.form.get('età')
    altezza = request.form.get('altezza')
    peso = request.form.get('peso')
    livello_attività = request.form.get('livello_attività')

    try:
        # Validazione inputs
        età = int(età)
        altezza = float(altezza)
        peso = float(peso)
        livello_attività = int(livello_attività)

        bmr = calcolo_bmr(sesso, peso, altezza, età)
        tdee = calcola_tdee(bmr, livello_attività)
        bmi = calcola_bmi(peso,altezza)
        esito = valori_bmi(bmi)
        colazione, pranzo, cena, spuntino = ripartizione_calorica(tdee)
        sport = esercizio_fisico(bmi)

        # Creazione del grafico a torta e barre
        crea_grafico_ripartizione(colazione, pranzo, cena, spuntino, 'static/grafico_ripartizione.png')
        crea_grafico_ripartizione_barre(colazione, pranzo, cena, spuntino, 'static/grafico_ripartizione_barre.png')

        # Lettura del file CSV
        if not os.path.isfile('ricette_passaggi.csv'):
            raise FileNotFoundError("Il file 'ricette_passaggi.csv' non è stato trovato.")
        
        df = pd.read_csv('ricette_passaggi.csv')
        #definizione funzione per filtrare le ricette in base alle calorie
        def filtra_ricette(tipo, calorie_max):
            ricette = df[(df['Tipo'] == tipo) & (df['Calorie'] <= calorie_max)]
            if ricette.empty:
                return []
            return ricette.sample(3).to_dict(orient='records')

        giorni_settimana = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']

        #definizione menù settimanale
        menu_settimanale = {giorno: {
            'Colazione': filtra_ricette('Colazione', colazione),
            'Pranzo': filtra_ricette('Pranzo', pranzo),
            'Cena': filtra_ricette('Cena', cena),
            'Spuntino': filtra_ricette('Spuntino', spuntino)
        } for giorno in giorni_settimana}

        media_kcal = {}
        for giorno, pasti in menu_settimanale.items():
            media_kcal[giorno] = {}
            for pasto, ricette in pasti.items():
                if ricette:
                    media_kcal[giorno][pasto] = sum([ricetta['Calorie'] for ricetta in ricette]) / len(ricette)
                else:
                    media_kcal[giorno][pasto] = None

        ordine_pasti = ["Colazione", "Pranzo", "Spuntino", "Cena"]
        #stabilire i pasti giornalieri in base alle kcal
        giorni = list(media_kcal.keys())
        for giorno in giorni:
            pasti_giornalieri = [pasto for pasto in ordine_pasti if pasto in media_kcal[giorno]]
            medie_pasti = [media_kcal[giorno].get(pasto, None) for pasto in ordine_pasti]
            #creazione grafico
            fig, ax = plt.subplots()
            ax.plot(pasti_giornalieri, medie_pasti, label="Calorie reali")
            ax.plot(ordine_pasti, [colazione, pranzo, spuntino, cena], label="Calorie attese")
            ax.legend()
            ax.set_title(f"Bilancio calorie giornaliere - {giorno}")
            ax.set_xlabel("Pasti del giorno")
            ax.set_ylabel("Calorie calcolate")
            plt.savefig(f"static/grafico_{giorno}.png")
            plt.close(fig)  # Close the figure to free up resources

        return render_template('risultato.html', 
                               bmr=bmr, tdee=tdee,bmi=bmi,
                               colazione=colazione, pranzo=pranzo, cena=cena, spuntino=spuntino, esito=esito, sport=sport,
                               menu_settimanale=menu_settimanale)

    except (ValueError, FileNotFoundError) as e:
        error_message = str(e)
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
