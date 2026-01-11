import random
import json

# --- MODULO SIMULAZIONE SENSORISTICA (IoT) ---
def ottieni_dati_meteo_iot():
    """
    Simulo i dati che verrebbero trasmessi dalla centralina IoT installata nel vigneto.
    In produzione, questa funzione farebbe una chiamata API ai sensori reali (Esame: Reti e Cybersecurity).
    Qui uso una generazione pseudo-casuale (Esame: Calcolo Probabilità) per testare gli algoritmi.
    
    Restituisce: Un dizionario con mm di pioggia, temperatura e livello di rischio calcolato.
    """
    # Genero valori casuali basandomi sulle medie stagionali della mia zona (600m s.l.m.)
    pioggia_mm = random.randint(0, 150)
    temperatura_media = random.uniform(18.0, 35.0) 
    
    # Logica applicativa: definisco il rischio patogeni in base a caldo e umidità
    rischio = "BASSO"
    if pioggia_mm > 80 and temperatura_media > 25:
        # Condizioni ideali per la peronospora
        rischio = "ALTO"
    elif pioggia_mm > 50:
        rischio = "MEDIO"
        
    return {
        "pioggia_mm": pioggia_mm,
        "temp_avg": round(temperatura_media, 1),
        "rischio_patogeni": rischio
    }

# --- CLASSE CORE: DIGITAL TWIN DEL VIGNETO ---
class SimulatoreLottoVigneto:
    def __init__(self, id_lotto, nome_cultivar, numero_piante, ettari):
        """
        Costruttore della classe. Inizializzo lo stato dell'oggetto (Lotto).
        Applicazione dei principi di Programmazione Orientata agli Oggetti (Esame: Programmazione 1).
        """
        # Attributi strutturali fissi
        self.id = id_lotto
        self.cultivar = nome_cultivar
        self.n_piante = numero_piante
        self.ettari = ettari
        
        # Attributi configurabili (verranno settati in base alle decisioni dell'utente)
        self.cap_max_raccolta_q = 0.0
        self.tempo_lavorazione_q = 0.0
        self.concime = "Nessuno"
        self.trattamento = "Nessuno"

    def configura_parametri(self, cap_giornaliera, tempo_unitario, concime, trattamento):
        """
        Configuro i vincoli operativi del processo produttivo.
        Questo metodo mi permette di testare scenari "What-If" (Cosa succede se...?).
        
        Input:
        - cap_giornaliera: Quanti quintali riesco a raccogliere al giorno.
        - tempo_unitario: Ore necessarie per lavorare un quintale in cantina.
        - concime/trattamento: Strategie agronomiche scelte.
        """
        self.cap_max_raccolta_q = cap_giornaliera
        self.tempo_lavorazione_q = tempo_unitario
        self.concime = concime
        self.trattamento = trattamento

    def calcola_resa_quantitativa(self, dati_meteo):
        """
        Algoritmo principale per la stima della produzione.
        Combino le variabili decisionali con quelle ambientali (IoT).
        """
        # Parto da una distribuzione uniforme per simulare la variabilità naturale di ogni pianta
        resa_pianta = random.uniform(2.5, 4.5)
        
        # Applico i modificatori in base alla strategia scelta (Logica condizionale)
        if self.concime == "Urea": 
            resa_pianta *= 1.15 # +15% resa stimata
        elif self.concime == "Zolfato": 
            resa_pianta *= 1.05 # +5% resa stimata
        
        # Gestione del rischio (Analisi dei vincoli ambientali)
        # Se c'è rischio alto e non ho trattato con Poltiglia Bordolese, ho una perdita ingente
        if dati_meteo["rischio_patogeni"] == "ALTO" and self.trattamento != "Poltiglia Bordolese":
             resa_pianta *= 0.60 # Perdita del 40%
             
        # Calcolo totale sul lotto
        totale_kg = resa_pianta * self.n_piante
        return totale_kg

    def calcola_tempi_totali(self, totale_uva_kg):
        """
        Calcola il lead time totale del processo produttivo.
        Fondamentale per la pianificazione aziendale (Esame: Strategia e Organizzazione).
        Restituisce: Float rappresentante le ore totali.
        """
        totale_quintali = totale_uva_kg / 100.0
        
        # 1. Calcolo Tempo Vendemmia
        # Il tempo è limitato dalla capacità giornaliera (Collo di bottiglia)
        giorni_necessari = totale_quintali / self.cap_max_raccolta_q
        if giorni_necessari < 1: 
            giorni_necessari = 1
        ore_vendemmia = giorni_necessari * 8.0 # Assumo giornata lavorativa standard
        
        # 2. Calcolo Tempo Lavorazione (Pigiatura/Torchiatura)
        ore_cantina = totale_quintali * self.tempo_lavorazione_q
        
        # 3. Tempo Gestione (Stimato su base storica: 3 min a pianta + lavori trattore su ettari)
        ore_gestione = (self.n_piante * 0.05) + (self.ettari * 20) 

        return round(ore_vendemmia + ore_cantina + ore_gestione, 1)

    def esegui_simulazione(self, dati_meteo):
        """
        Metodo wrapper che esegue l'intera pipeline di calcolo per l'oggetto corrente.
        Restituisce un dizionario strutturato pronto per la serializzazione JSON.
        """
        kg_uva = self.calcola_resa_quantitativa(dati_meteo)
        litri_vino = kg_uva * 0.70 # Coefficiente di trasformazione medio (da mia esperienza)
        ore_totali = self.calcola_tempi_totali(kg_uva)
        
        return {
            "id": self.id,
            "cultivar": self.cultivar,
            "input_config": {
                "concime": self.concime,
                "trattamento": self.trattamento
            },
            "output": {
                "uva_kg": round(kg_uva, 2),
                "vino_litri": round(litri_vino, 2),
                "ore_totali": ore_totali
            }
        }

# --- CONTROLLER PRINCIPALE (Backend Logic) ---
def main_controller(modalita_input, json_data=None):
    """
    Funzione di ingresso del programma. Gestisce il flusso in base alla sorgente della richiesta.
    
    Parametri:
    - modalita_input: 'manuale' (per test da console) o 'json' (chiamata dal frontend web).
    - json_data: stringa JSON contenente i parametri (solo se modalita_input è 'json').
    """
    
    lista_lotti = []

    # Inizializzo gli oggetti. In un'applicazione reale, questi dati verrebbero
    # istanziati parsando il 'json_data' in ingresso (Deserializzazione).
    # Per questo prototipo, uso i dati reali della mia azienda 'Timpe Smart Vineyard'.
    
    # Configurazione Lotto 1: Barbera
    l1 = SimulatoreLottoVigneto("L01", "Barbera", 1000, 0.5)
    l1.configura_parametri(cap_giornaliera=30.0, tempo_unitario=0.4, concime="Urea", trattamento="Poltiglia Bordolese")
    
    # Configurazione Lotto 2: Aglianico (Varietà tardiva, vincoli diversi)
    l2 = SimulatoreLottoVigneto("L02", "Aglianico", 1000, 0.5)
    l2.configura_parametri(cap_giornaliera=15.0, tempo_unitario=0.6, concime="Nessuno", trattamento="Zolfo")
    
    # Configurazione Lotto 3: Moscato (Più delicato)
    l3 = SimulatoreLottoVigneto("L03", "Moscato", 1000, 0.5)
    l3.configura_parametri(cap_giornaliera=50.0, tempo_unitario=0.3, concime="Zolfato", trattamento="Nessuno")
    
    lista_lotti = [l1, l2, l3]

    # Ottengo i dati ambientali simulati (IoT)
    meteo = ottieni_dati_meteo_iot()
    
    # Colleziono i risultati
    risultati_simulazione = []
    for lotto in lista_lotti:
        risultati_simulazione.append(lotto.esegui_simulazione(meteo))

    # --- GESTIONE OUTPUT (Polimorfismo della risposta) ---
    
    if modalita_input == 'manuale':
        # Output formattato per la visualizzazione immediata su terminale (Report Testuale)
        print("="*42)
        print("📋 REPORT PRODUZIONE TIMPE SMART VINEYARD")
        print("="*42)
        print(f"\n⛅ METEO RILEVATO: Pioggia {meteo['pioggia_mm']}mm | Temp {meteo['temp_avg']}°C | Rischio: {meteo['rischio_patogeni']}")
        
        for res in risultati_simulazione:
            print(f"\n🍇 CULTIVAR: {res['cultivar']} (Lotto {res['id']})")
            print(f"   ⚙️  Config: {res['input_config']['concime']} + {res['input_config']['trattamento']}")
            print(f"   ⚖️  Resa Stimata: {res['output']['uva_kg']} Kg")
            print(f"   🍷 Produzione Vino: {res['output']['vino_litri']} Litri")
            print(f"   🚜 Tempo Ciclo: {res['output']['ore_totali']} Ore")
            print("-" * 30)
            
    elif modalita_input == 'json':
        # Risposta standard API per il frontend (Interfaccia Web)
        # Serializzo la lista di dizionari in una stringa JSON
        return json.dumps(risultati_simulazione, indent=4)

# --- ENTRY POINT ---
if __name__ == "__main__":
    # Esempio 1: Simulazione manuale (Quindi output su console)
    main_controller('manuale')
    
    # Esempio 2: Simulazione richiesta dal sito web (commentata per il test)
    # response = main_controller('json')
    # print(response)