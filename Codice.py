import random
import json

# --- MODULO CONFIGURAZIONE E COSTANTI ---
# Definisco le costanti globali basate sull'esperienza operativa reale (sito 600m s.l.m.)
RESA_UVA_VINO = 0.65  # 100kg uva = 65 litri vino (media tra 60 e 70)
ORE_LAVORO_PER_ETTARO = 40.0  # Tempo medio trattamenti meccanici (trattore)
ORE_LAVORO_PER_PIANTA = 0.05  # Tempo medio manuale (potatura/vendemmia) ~3 min a pianta

def ottieni_previsioni_meteo_stagionali():
    """
    Simula le condizioni meteo stagionali.
    Restituisce un dizionario con i dati pluviometrici e di temperatura.
    Utilizzo un random seed implicito per variare i risultati ad ogni esecuzione.
    """
    # Genero un indice di piovosità da 1 (siccità) a 10 (alluvionale)
    indice_pioggia = random.randint(1, 10)
    
    # Determino la "Pressione Malattia" (Rischio Peronospora)
    # Se piove molto (indice > 7) e fa caldo, il rischio è alto.
    rischio_malattia = "BASSO"
    if indice_pioggia > 6:
        rischio_malattia = "ALTO"
    elif indice_pioggia > 4:
        rischio_malattia = "MEDIO"

    return {
        "indice_pioggia": indice_pioggia,
        "rischio_malattia": rischio_malattia,
        "descrizione": f"Stagione con piovosità livello {indice_pioggia}/10"
    }

class SimulatoreVigneto:
    def __init__(self, nome_cultivar, numero_piante, ettari):
        """
        Inizializza l'oggetto Vigneto (Digital Twin del lotto fisico).
        """
        self.nome_cultivar = nome_cultivar
        self.numero_piante = numero_piante
        self.ettari = ettari
        
        # Stato di configurazione (default: nessun input chimico)
        self.concime_utilizzato = None
        self.trattamento_fito = None

    def configura_processo(self, tipo_concime, trattamento_preventivo):
        """
        Permette di impostare le variabili decisionali agronomiche.
        """
        self.concime_utilizzato = tipo_concime
        self.trattamento_fito = trattamento_preventivo

    def calcola_resa_agronomica(self, meteo):
        """
        Algoritmo core per il calcolo della produzione in kg.
        Considera input chimici e variabili ambientali.
        """
        # Resa base: genero un float casuale tra 3.0 e 4.0 kg per pianta
        resa_per_pianta = random.uniform(3.0, 4.0)

        # 1. Fattore Concimazione (Boost produttivo)
        if self.concime_utilizzato == "Urea":
            # L'azoto spinge la parte vegetativa, aumento la resa del 10%
            resa_per_pianta *= 1.10
        elif self.concime_utilizzato == "Zolfato Ammonico":
            resa_per_pianta *= 1.05

        # 2. Fattore Meteo e Malattie (Malus produttivo)
        # Se il rischio malattia è ALTO e non ho usato la Poltiglia Bordolese (Rame)
        if meteo["rischio_malattia"] == "ALTO":
            if self.trattamento_fito != "Poltiglia Bordolese":
                # Danno grave: perdo il 40% del raccolto per peronospora
                resa_per_pianta *= 0.60
            else:
                # Il trattamento ha funzionato, perdo solo un 5% fisiologico
                resa_per_pianta *= 0.95

        # Calcolo totale uva
        totale_uva_kg = resa_per_pianta * self.numero_piante
        return totale_uva_kg

    def calcola_tempi_produzione(self):
        """
        Stima le ore uomo/macchina necessarie per completare il ciclo.
        """
        # Tempo manuale (dipende dal numero di piante): Potatura, Legatura, Vendemmia
        tempo_manuale = self.numero_piante * ORE_LAVORO_PER_PIANTA
        
        # Tempo meccanico (dipende dagli ettari): Trattamenti, Aratura ("Staddare")
        # Ipotizzo circa 5 passaggi annuali col trattore
        tempo_meccanico = self.ettari * ORE_LAVORO_PER_ETTARO * 5
        
        return tempo_manuale + tempo_meccanico

    def esegui_simulazione(self):
        """
        Orchestra la simulazione richiamando i moduli meteo e calcolo.
        Restituisce un dizionario (JSON-ready).
        """
        # 1. Ottengo dati ambientali esterni
        dati_meteo = ottieni_previsioni_meteo_stagionali()

        # 2. Eseguo calcoli agronomici
        uva_prodotta_kg = self.calcola_resa_agronomica(dati_meteo)
        vino_prodotto_litri = uva_prodotta_kg * RESA_UVA_VINO
        tempo_totale_h = self.calcola_tempi_produzione()

        # 3. Preparo output strutturato
        risultato = {
            "cultivar": self.nome_cultivar,
            "input_setup": {
                "piante": self.numero_piante,
                "ettari": self.ettari,
                "concime": self.concime_utilizzato,
                "trattamento": self.trattamento_fito
            },
            "ambiente": dati_meteo,
            "output_produzione": {
                "uva_kg": round(uva_prodotta_kg, 2),
                "vino_litri": round(vino_prodotto_litri, 2),
                "tempo_ciclo_ore": round(tempo_totale_h, 1)
            }
        }
        return risultato

# --- MAIN CONTROLLER (Simulazione Console) ---
if __name__ == "__main__":
    print("--- AVVIO SIMULATORE TIMPE SMART VINEYARD v0.1 ---\n")

    # Simulazione Lotto 1: Barbera (Scenario Ottimale)
    lotto1 = SimulatoreVigneto("Barbera", 3000, 1.5)
    lotto1.configura_processo("Urea", "Poltiglia Bordolese")
    res1 = lotto1.esegui_simulazione()

    # Simulazione Lotto 2: Moscato (Scenario a Rischio - Niente trattamenti)
    lotto2 = SimulatoreVigneto("Moscato", 1200, 0.6)
    lotto2.configura_processo("Nessuno", "Nessuno")
    res2 = lotto2.esegui_simulazione()
    
    # Simulazione Lotto 3: Aglianico (Scenario Standard)
    lotto3 = SimulatoreVigneto("Aglianico", 2500, 1.2)
    lotto3.configura_processo("Zolfato Ammonico", "Zolfo")
    res3 = lotto3.esegui_simulazione()

    # Output JSON aggregato (come richiesto per il futuro frontend)
    database_produzione = [res1, res2, res3]
    json_output = json.dumps(database_produzione, indent=4)
    
    print(json_output)