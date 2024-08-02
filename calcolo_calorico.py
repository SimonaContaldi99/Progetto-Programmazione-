import matplotlib.pyplot as plt

#calcolo valori corporei
def calcolo_bmr(sesso, peso, altezza, età):
    if sesso.upper() == "M":
        bmr = 10 * peso + 6.25 * altezza - 5 * età + 5
    elif sesso.upper() == "F":
        bmr = 10 * peso + 6.25 * altezza - 5 * età - 161
    else:
        raise ValueError("Sesso non valido.")
    return round(bmr)
#calcolo livello di attività personale
def calcola_tdee(bmr, livello_attività):
    livelli_attività = [1.2, 1.375, 1.55, 1.725, 1.9]
    
    if 1 <= livello_attività <= 5:
        fattore_attività = livelli_attività[livello_attività - 1]
    else:
        raise ValueError("Livello di attività non valido")

    return round(bmr * fattore_attività)
#calcolo ripartizione calorica
def ripartizione_calorica(tdee):
    colazione = round(tdee * 0.25)
    pranzo = round(tdee * 0.35)
    cena = round(tdee * 0.30)
    spuntino = round(tdee * 0.10)
    return colazione, pranzo, cena, spuntino
#creazione grafico ripartizione pasti
def crea_grafico_ripartizione(colazione, pranzo, cena, spuntino, filepath):
    dati = [colazione, pranzo, cena, spuntino]
    etichette = ["Colazione", "Pranzo", "Cena", "Spuntino"]
    colori = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    plt.pie(dati, labels=etichette, colors=colori, autopct='%1.1f%%')
    plt.title("Grafico della ripartizione calorica")
    plt.savefig(filepath)
    plt.close()
