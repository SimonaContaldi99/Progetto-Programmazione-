import numpy as np
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

#calcolo indice massa corporea 
def calcola_bmi(peso,altezza): 
    if altezza <= 0:
        raise ValueError("L'altezza deve essere maggiore di zero.")
    else:
        bmi = round(peso/((altezza * 0.01) **2),2)
    return bmi

#calcolo esito massa corporea 
def valori_bmi(bmi):
    if bmi < 16.0:
        return "Sottopeso grave" 
    elif 16.0 < bmi < 18.49:
        return "Sottopeso"
    elif 18.5 < bmi < 24.9:
        return "Normopeso"
    elif 25 < bmi < 29.9:
        return "Sovrappeso" 
    elif 30.0 < bmi < 34.9:
        return "Obesità di classe 1"
    else:
        return "Obesità di classe <=2"
    
#funzione per sport consigliato
def esercizio_fisico(bmi):
    if bmi < 16.0:
        return "Si consigliano esercizi di rilassamento come yoga o ginnastica posturale e solo in un secondo momento introdurre anche esercizi di rinforzo in modo graduale." 
    elif 16.0 < bmi < 18.49:
        return "Si consigliano esercizi di forza per aumentare lam massa muscolare."
    elif 18.5 < bmi < 24.9:
        return "Si consigliano esercizi aerobici (camminata, nuoto, corsa) combinati equamente con esercizi con i pesi, due o tre volte a settimana."
    elif 25 < bmi < 29.9:
        return "Si consigliano esercizi con i pesi combinati con una maggiore frequenza di esercizi aerobici (camminata, nuoto, corsa)." 
    elif 30.0 < bmi < 34.9:
        return "Si consigliano esercizi aerobici con una frequenza di cinque volte a settimana ma con intensità ridotta." 
    else:
        return "Per obesità di questo tipo si valuta di solito con il proprio medico di riferimento un trattamento specifico con possibile operazione nei casi più gravi, e solo dopo si valuta per una dieta e una programmazione di attività fisica personalizzate."
    
#calcolo ripartizione calorica
def ripartizione_calorica(tdee):
    colazione = round(tdee * 0.25)
    pranzo = round(tdee * 0.35)
    cena = round(tdee * 0.30)
    spuntino = round(tdee * 0.10)
    return colazione, pranzo, cena, spuntino

#creazione grafico ripartizione pasti
def crea_grafico_ripartizione(colazione, pranzo, spuntino, cena, filepath):
    dati = [colazione, pranzo, spuntino, cena]
    etichette = ["Colazione", "Pranzo", "Cena", "Spuntino"]
    colori = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    plt.pie(dati, labels=etichette, colors=colori, autopct='%1.1f%%')
    plt.title("Grafico della ripartizione calorica")
    plt.savefig(filepath)
    plt.close()

def crea_grafico_ripartizione_barre(colazione, pranzo, cena, spuntino, filepath):
    colori = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    dati = [colazione, pranzo, cena, spuntino]
    pasti = ["Colazione", "Pranzo", "Cena", "Spuntino"]
    
    plt.bar(pasti, dati, color=colori)
    plt.title("Ripartizione calorica per kcal")
    plt.xlabel("Pasto")
    plt.ylabel("Calorie")
    plt.savefig(filepath)
    plt.close()
