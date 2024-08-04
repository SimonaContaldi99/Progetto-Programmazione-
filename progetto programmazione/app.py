import pandas as pd
from flask import Flask, render_template, request
from calcolo_calorico import calcolo_bmr, calcola_tdee, ripartizione_calorica, crea_grafico_ripartizione, crea_grafico_ripartizione_barre
import matplotlib.pyplot as plt

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
        crea_grafico_ripartizione_barre(colazione, pranzo, cena, spuntino, 'static/grafico_ripartizione_barre.png')

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

        # Calcolo delle medie delle calorie
        media_kcal = {}
        for giorno, pasti in menu_settimanale.items():
            media_kcal[giorno] = {}
            for pasto, ricette in pasti.items():
                if ricette:
                    media_kcal[giorno][pasto] = sum([ricetta['Calorie'] for ricetta in ricette]) / len(ricette)
                else:
                    media_kcal[giorno][pasto] = None

        # Creazione dei grafici
        giorni = list(media_kcal.keys())
        dati = [colazione, pranzo, cena, spuntino]
        pasti = ["Colazione", "Pranzo", "Cena", "Spuntino"]

        for giorno in giorni:
            pasti_giornalieri = list(media_kcal[giorno].keys())
            medie_pasti = []
            for pasto in pasti_giornalieri:
                if media_kcal[giorno][pasto] is not None:
                    medie_pasti.append(media_kcal[giorno][pasto])

            fig, ax = plt.subplots()
            ax.plot(pasti_giornalieri, medie_pasti, label="Calorie reali")
            ax.plot(pasti, dati, label="Calorie attese")
            ax.legend()
            ax.set_title(f"Bilancio calorie giornaliere - {giorno}")
            ax.set_xlabel("Pasti del giorno")
            ax.set_ylabel("Calorie calcolate")
            plt.savefig(f"static/grafico_{giorno}.png")

        return render_template('risultato.html', 
                               bmr=bmr, tdee=tdee,
                               colazione=colazione, pranzo=pranzo, cena=cena, spuntino=spuntino,
                               menu_settimanale=menu_settimanale)
    
    except ValueError as e:
        error_message = str(e)
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
