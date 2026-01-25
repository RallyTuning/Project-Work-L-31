import random
import json

# ======================================================================================
#   🎛️ DASHBOARD DI CONFIGURAZIONE
#   Modificare i parametri qui sotto per testare diverse simulazioni.
# ======================================================================================

# --------------------------------------------------------------------------------------
# 🌐 SEZIONE A: SIMULAZIONE CHIAMATA API (WEB)
# Per testare l'ingresso JSON (come se arrivasse dal sito), è sufficiente togliere il
# commento dalla riga sottostante dove viene popolato manualmente JSON_SIMULATO_DAL_WEB.
# # Se attiva, il codice ignorerà i parametri manuali della Sezione B.
# --------------------------------------------------------------------------------------

JSON_SIMULATO_DAL_WEB = None
# JSON_SIMULATO_DAL_WEB = '[ { "id": "L-WEB-01", "cultivar": "Barbera", "tipologia": "Rosso", "n_piante": 1000, "ettari": 0.7, "config": { "capacita_giornaliera": 40.0, "tempo_unitario": 0.5, "concime": "Urea", "trattamento": "Poltiglia Bordolese" } }, { "id": "L-WEB-02", "cultivar": "Aglianico", "tipologia": "Rosso", "n_piante": 1200, "ettari": 0.6, "config": { "capacita_giornaliera": 20.0, "tempo_unitario": 0.6, "concime": "Nessuno", "trattamento": "Zolfo" } }, { "id": "L-WEB-03", "cultivar": "Moscato", "tipologia": "Bianco", "n_piante": 500, "ettari": 0.3, "config": { "capacita_giornaliera": 60.0, "tempo_unitario": 0.3, "concime": "Zolfato", "trattamento": "Nessuno" } } ]'

# --------------------------------------------------------------------------------------
# 🛠️ SEZIONE B: PARAMETRI MANUALI (DEFAULT)
# Questi parametri vengono usati se la variabile JSON sopra è commentata o vuota.
#
# ISTRUZIONI PER LA CONFIGURAZIONE:
# Modificare i valori nei dizionari 'LOTTO_1', 'LOTTO_2', 'LOTTO_3' seguendo la legenda sottoriportata.
#
# 1. PARAMETRI IDENTIFICATIVI
#    - "nome":   (Stringa) Nome etichetta (es. "Barbera", "Merlot").
#    - "tipo":   (Stringa) "Rosso" o "Bianco".
#                > "Rosso": Attiva flusso macerazione [A] (Resa minore, Vinaccia umida, Tempi lunghi).
#                > "Bianco": Attiva flusso pressatura [B] (Resa alta, Vinaccia secca, Tempi brevi).
#
# 2. DIMENSIONI DEL VIGNETO
#    - "piante": (Intero) Numero totale di viti nel lotto.
#    - "ettari": (Float)  Superficie in ettari (usato per calcolo ore gestione/potatura).
#
# 3. PARAMETRI OPERATIVI (MACCHINE E UOMINI)
#    - "capacita_raccolta": (Float) Quintali raccoglibili al giorno dalla squadra.
#                           > Valore basso (es. 8.0) = Raccolta manuale lenta -> Più ore uomo.
#                           > Valore alto (es. 40.0) = Raccolta meccanizzata -> Meno ore uomo.
#    - "tempo_lavorazione": (Float) Ore necessarie per lavorare 1 Quintale in cantina.
#                           > Standard Rosso: 1.4 - 1.6 h/q (Macerazione).
#                           > Standard Bianco: 0.9 - 1.1 h/q (Pressatura).
#
# 4. DECISIONI AGRONOMICHE (INPUT VARIABILI)
#    - "concime": Scegliere strategia di fertilizzazione per aumentare la resa:
#                 > "Nessuno": Resa base naturale.
#                 > "Zolfato": +10% Resa (Spinta moderata).
#                 > "Urea":    +25% Resa (Spinta vegetativa forte).
#
#    - "trattamento": Scegliere protezione contro Meteo Avverso (Pioggia/Funghi):
#                 > "Nessuno": Esposto a rischi. Se Meteo=ALTO rischio -> Perdita 50% raccolto.
#                 > "Zolfo":   Protezione Base. Se Meteo=ALTO rischio -> Perdita 25% raccolto.
#                 > "Poltiglia Bordolese": Protezione Totale (Rame). Perdita massima 5% (ho voluto comuqnue lasciare una perdita minima).
# --------------------------------------------------------------------------------------

# Configurazione Lotto 1: Barbera (Vino Rosso - Flusso A)
LOTTO_1 = {
    "nome": "Barbera",
    "tipo": "Rosso",
    "piante": 1300,
    "ettari": 0.7,
    "capacita_raccolta": 10.0,
    "tempo_lavorazione": 1.4,
    "concime": "Urea",
    "trattamento": "Poltiglia Bordolese"
}

# Configurazione Lotto 2: Aglianico (Vino Rosso - Flusso A)
LOTTO_2 = {
    "nome": "Aglianico",
    "tipo": "Rosso",
    "piante": 1200,
    "ettari": 0.6,
    "capacita_raccolta": 8.0,
    "tempo_lavorazione": 1.5,
    "concime": "Nessuno",
    "trattamento": "Zolfo"
}

# Configurazione Lotto 3: Moscato (Vino Bianco - Flusso B)
LOTTO_3 = {
    "nome": "Moscato",
    "tipo": "Bianco",
    "piante": 500,
    "ettari": 0.2,
    "capacita_raccolta": 12.0,
    "tempo_lavorazione": 1.0,
    "concime": "Zolfato",
    "trattamento": "Nessuno"
}

# ======================================================================================
#   FINE CONFIGURAZIONE - INIZIO LOGICA DEL SISTEMA
# ======================================================================================


# - MODULO SIMULAZIONE SENSORISTICA (IoT) -
# Esami: Calcolo, Probabilità e Statistica (MAT06) - Reti di calcolatori e Cybersecurity (INF01II)
def ottieni_dati_meteo_iot():
    """
    Simulo, attraverso la generazione di numeri casuali, i dati trasmessi dalla centralina IoT nel vigneto.
    NOTA: I valori rappresentano il TREND MEDIO STAGIONALE dell'intero ciclo produttivo,
    non il meteo di un singolo giorno.
    """
    # Genero valori casuali basati sulle medie della mia zona
    pioggia_mm = random.randint(150, 600)
    temperatura_media = random.uniform(18.0, 35.0) 
    
    # Logica applicativa: definisco il rischio patogeni su base stagionale
    rischio = "BASSO"

    if pioggia_mm > 350 and temperatura_media > 25:
        # Caldo + Umido = Condizioni ideali per la maggior parte dei pategeni
        rischio = "ALTO"
    elif pioggia_mm > 200:
        rischio = "MEDIO"
        
    return {
        "pioggia_mm": pioggia_mm,
        "temp_avg": round(temperatura_media, 1),
        "rischio_patogeni": rischio
    }

# - CLASSE CORE: DIGITAL TWIN DEL VIGNETO -
# Applicazione dei principi e paradigmi di Programmazione Orientata agli Oggetti (OOP).
# Esami: Programmazione 1 (INF01) - Programmazione 2 (INF01III)
class SimulatoreLottoVigneto:
    def __init__(self, id_lotto, nome_cultivar, tipologia, numero_piante, ettari):
        """
        Costruttore della classe. Inizializzo lo stato dell'oggetto.
        'tipologia' ('Rosso' o 'Bianco') determina il flusso produttivo.
        """
        self.id = id_lotto
        self.cultivar = nome_cultivar
        self.tipologia = tipologia 
        self.n_piante = numero_piante
        self.ettari = ettari
        
        # Attributi configurabili
        self.cap_max_raccolta_q = 0.0
        self.tempo_lavorazione_q = 0.0
        self.concime = "Nessuno"
        self.trattamento = "Nessuno"

    def configura_parametri(self, capacita_giornaliera, tempo_unitario, concime, trattamento):
        """
        Configuro i vincoli operativi per scenari 'What-If'.
        """
        self.cap_max_raccolta_q = capacita_giornaliera
        self.tempo_lavorazione_q = tempo_unitario
        self.concime = concime
        self.trattamento = trattamento

    def calcola_resa_agronomica(self, dati_meteo):
        """
        Calcola l'uva prodotta in campo (Input industriale) e applico logiche condizionali per
        modificare dinamicamente la resa in base alle variabili agronomiche in input.
        (concimazione e rischio meteo).
        """
        # Parto da una distribuzione uniforme per simulare la variabilità naturale di ogni pianta
        resa_pianta = random.uniform(2.5, 4.5)
        
        # Applico i modificatori in base alla strategia di concimazione scelta (Logica condizionale)
        # Esami: Programmazione 1 (INF01) - Algoritmi e strutture dati (INF01I)

        # Boost Fertilizzanti
        if self.concime == "Urea": resa_pianta *= 1.25 # +25% Resa
        elif self.concime == "Zolfato": resa_pianta *= 1.10 # +10% Resa
        
        # Gestione Rischio Meteo
        if dati_meteo["rischio_patogeni"] == "ALTO":
            if self.trattamento == "Nessuno":
                resa_pianta *= 0.50  # Disastro: Perdita del 50%
            elif self.trattamento == "Zolfo":
                resa_pianta *= 0.75  # Protezione parziale: Perdita del 25%
            elif self.trattamento == "Poltiglia Bordolese":
                resa_pianta *= 0.95  # Protezione eccellente: Perdita fisiologica solo del 5%
                
        elif dati_meteo["rischio_patogeni"] == "MEDIO":
            # Anche con rischio medio, non trattare porta qualche danno
            if self.trattamento == "Nessuno":
                resa_pianta *= 0.85 # Perdita del 15%
             
        return resa_pianta * self.n_piante

    # - FLUSSI PRODUTTIVI DIFFERENZIATI -
    
    def simula_flusso_rosso(self, kg_uva):
        """
        FLUSSO A: Vinificazione in Rosso.
        Prevede macerazione lunga (bucce a contatto col mosto).
        """
        # La resa uva/vino oscilla tra 60% e 70%
        resa_vino = random.uniform(0.60, 0.70)
        # La vinaccia oscilla tra 18% e 25%
        resa_vinaccia = random.uniform(0.18, 0.25)
        
        litri_vino = kg_uva * resa_vino
        kg_vinaccia = kg_uva * resa_vinaccia
        
        # Macerazione allunga i tempi di occupazione tino (+20%)
        tempo_processo = (kg_uva / 100) * self.tempo_lavorazione_q * 1.2
        return litri_vino, kg_vinaccia, tempo_processo

    def simula_flusso_bianco(self, kg_uva):
        """
        FLUSSO B: Vinificazione in Bianco/Spumante.
        Prevede pressatura soffice immediata. Vinaccia esce subito.
        """
        # Resa leggermente più alta per i bianchi che oscilla tra 65% e 75%
        resa_vino = random.uniform(0.65, 0.75)
        # La vinaccia oscilla tra 12% e 18%
        resa_vinaccia = random.uniform(0.12, 0.18)
        
        litri_vino = kg_uva * resa_vino
        kg_vinaccia = kg_uva * resa_vinaccia
        
        tempo_processo = (kg_uva / 100) * self.tempo_lavorazione_q
        return litri_vino, kg_vinaccia, tempo_processo


    def calcola_tempi_dettagliati(self, kg_uva, ore_lavorazione_cantina):
        """
        Restituisce il dettaglio delle ore per ogni fase.
        """
        totale_quintali = kg_uva / 100.0
        
        # Vendemmia (Vincolato da capacità giornaliera)
        giorni_raccolta = totale_quintali / self.cap_max_raccolta_q
        if giorni_raccolta < 1: giorni_raccolta = 1
        ore_vendemmia = giorni_raccolta * 8.0 
        
        # Gestione (Stimato su ettari)
        # Il tempo può variare del +/- 25% in base all'annata
        fattore_imprevisti = random.uniform(0.75, 1.25)
        ore_gestione = ((self.n_piante * 0.05) + (self.ettari * 20)) * fattore_imprevisti

        # Ritorno i 3 valori separati
        return round(ore_vendemmia, 1), round(ore_lavorazione_cantina, 1), round(ore_gestione, 1)

    def esegui_simulazione(self, dati_meteo):
        """
        Metodo Wrapper che esegue l'intera pipeline per il lotto corrente.
        """
        # Fase Campo
        kg_uva = self.calcola_resa_agronomica(dati_meteo)
        
        # Fase Cantina
        if self.tipologia == "Rosso":
            vino, vinaccia, ore_cantina = self.simula_flusso_rosso(kg_uva)
        else: 
            vino, vinaccia, ore_cantina = self.simula_flusso_bianco(kg_uva)

        # Fase Analisi Tempi
        t_vend, t_cant, t_gest = self.calcola_tempi_dettagliati(kg_uva, ore_cantina)
        ore_totali = t_vend + t_cant + t_gest
        
        # Fase Calcolo Bottiglie
        n_bottiglie = int(vino / 1.5) # Arrotondamento per difetto a intero

        # Costruisco il dizionario di risposta
        return {
            "id": self.id,
            "cultivar": self.cultivar,
            "tipologia": self.tipologia,
            "input_config": {
                "concime": self.concime,
                "trattamento": self.trattamento,
                "cap_giornaliera": self.cap_max_raccolta_q,
                "tempo_unitario": self.tempo_lavorazione_q
            },
            "output": {
                "uva_kg": round(kg_uva, 2),
                "vino_litri": round(vino, 2),
                "vinaccia_kg": round(vinaccia, 2),
                "n_bottiglie": n_bottiglie,
                "ore_totali": round(ore_totali, 1),
                "dettaglio_ore": {
                    "vendemmia": t_vend,
                    "cantina": t_cant,
                    "gestione": t_gest
                }
            }
        }

# - CONTROLLER PRINCIPALE -
def main_controller(modalita_input, json_data = None):
    '''
    Controller principale che gestisce l'intero flusso di simulazione.
    modalita_input: 'manuale' o 'json' per scegliere la fonte dei dati.
    json_data: stringa JSON se modalita_input è 'json'.
    '''
    lista_lotti = []

    # - FASE 1: INIZIALIZZAZIONE -
    # Controllo prioritario: Se c'è un JSON valido (e non è None), uso quello (API mode)
    if modalita_input == 'json' and json_data:

        # Gestione delle eccezioni: implemento un meccanismo difensivo per evitare il crash dell'applicazione in caso di dati di input corrotti o malformati.
        # Esame: Ingegneria del Software (INGINF06)
        try:

            # Deserializzazione del payload JSON: trasformo la stringa ricevuta dal frontend in strutture dati manipolabili dal backend Python.
            # Esame: Basi di Dati (INGINF05)
            dati_list = json.loads(json_data)

            for d in dati_list:
                # Nota: il JSON deve contenere il campo 'tipologia' e i nomi completi nel config
                nuovo = SimulatoreLottoVigneto(d['id'], d['cultivar'], d['tipologia'], int(d['n_piante']), float(d['ettari']))
                nuovo.configura_parametri(
                    float(d['config']['capacita_giornaliera']), float(d['config']['tempo_unitario']),
                    d['config']['concime'], d['config']['trattamento']
                )
                lista_lotti.append(nuovo)
        except Exception as e:
            # Fallback di sicurezza: se il JSON è corrotto, restituisco errore nel log
            return json.dumps({"error": f"JSON Error: {str(e)}"}), 500
    
    else:
        # Modalità Manuale: Uso i dati definiti nella Dashboard in alto
        def crea_lotto_da_config(id_l, conf):
            Lotto = SimulatoreLottoVigneto(id_l, conf["nome"], conf["tipo"], conf["piante"], conf["ettari"])
            Lotto.configura_parametri(conf["capacita_raccolta"], conf["tempo_lavorazione"], conf["concime"], conf["trattamento"])
            return Lotto

        lista_lotti.append(crea_lotto_da_config("L01", LOTTO_1))
        lista_lotti.append(crea_lotto_da_config("L02", LOTTO_2))
        lista_lotti.append(crea_lotto_da_config("L03", LOTTO_3))

    # - FASE 2: ESECUZIONE -
    meteo = ottieni_dati_meteo_iot()
    
    risultati = []
    
    # Accumulatori per i totali
    tot_uva, tot_vino, tot_vinaccia, tot_ore, tot_bottiglie = 0, 0, 0, 0, 0 

    # Eseguo la logica su ogni oggetto
    for lotto in lista_lotti:   
        res = lotto.esegui_simulazione(meteo)
        risultati.append(res)
        
        # Aggiorno i contatori globali
        tot_uva += res['output']['uva_kg']
        tot_vino += res['output']['vino_litri']
        tot_vinaccia += res['output']['vinaccia_kg']
        tot_ore += res['output']['ore_totali']
        tot_bottiglie += res['output']['n_bottiglie'] 

    # Costruisco il dizionario finale dei dati
    dati_finali = {
        "meteo_rilevato": meteo,
        "dettaglio_lotti": risultati,
        "totali_azienda": {
            "totale_uva_kg": round(tot_uva, 2),
            "totale_vino_litri": round(tot_vino, 2),
            "totale_vinaccia_biomassa_kg": round(tot_vinaccia, 2),
            "totale_ore_lavoro": round(tot_ore, 1),
            "totale_bottiglie_1_5L": tot_bottiglie
        }
    }

    # - FASE 3: OUTPUT -
    # Sintetizzo i dati operativi per fornire output decisionali utili alla pianificazione delle risorse aziendali (es. stima bottiglie e ore lavoro).
    # Esami: Strategia, organizzazione e marketing (INGIND35) - Corporate planning e valore d'impresa (SECSP07)
    if modalita_input == 'manuale':
        print("\n" + "=" * 42)
        print("📋 REPORT PRODUZIONE TIMPE SMART VINEYARD")
        print("=" * 42 + "\n")
        print(f"⛅ TREND METEO STAGIONALE: Pioggia {meteo['pioggia_mm']}mm | Rischio: {meteo['rischio_patogeni']}")
        
        for res in risultati:
            # Aggiunto ID Lotto nel titolo e rimesse le Emoji come richiesto
            print(f"\n🍇 CULTIVAR: {res['cultivar']} ({res['tipologia']}) - ID: {res['id']}")
            print(f" ├─⚙️  Configurazione:  {res['input_config']['concime']} + {res['input_config']['trattamento']}")
            print(f" ├─⚖️  Resa Uva:        {res['output']['uva_kg']} Kg")
            print(f" ├─🍷 Vino Finale:     {res['output']['vino_litri']} Litri")
            print(f" ├─🍾 Bottiglie:       {res['output']['n_bottiglie']} Pezzi (1.5L)")
            print(f" ├─♻️  Vinaccia:        {res['output']['vinaccia_kg']} Kg")
            print(f" └─⏱️  Tempi lavorazione:")
            print(f"    ├─── Raccolta:     {res['output']['dettaglio_ore']['vendemmia']} h")
            print(f"    ├─── Cantina:      {res['output']['dettaglio_ore']['cantina']} h")
            print(f"    ├─── Gestione:     {res['output']['dettaglio_ore']['gestione']} h")
            print(f"    └─── Totale:       {res['output']['ore_totali']} h")
            print("-" * 35)
        
        print("\n" + "=" * 42)
        print("📊 RIEPILOGO GENERALE AZIENDA")
        print("=" * 42)

        t = dati_finali['totali_azienda']

        print(f"🧺 Totale Uva Raccolta:    {t['totale_uva_kg']} Kg")
        print(f"🛢️  Totale Vino Prodotto:   {t['totale_vino_litri']} Litri")
        print(f"♻️  Totale Vinaccia:        {t['totale_vinaccia_biomassa_kg']} Kg")
        print(f"🍾 Totale Bottiglie:       {t['totale_bottiglie_1_5L']} Pezzi (1.5L)")
        print(f"🚜 Totale Ore Lavoro:      {t['totale_ore_lavoro']} h")
        print("=" * 42 + "\n")
            
    elif modalita_input == 'json':
        return json.dumps(dati_finali, indent = 4)

# - ENTRY POINT -
if __name__ == "__main__":
    # Verifica automatica: Se la variabile JSON è diversa da None, uso quella.
    # Altrimenti uso i dati manuali. Questo evita errori se la variabile è commentata.
    try:
        if JSON_SIMULATO_DAL_WEB:
            # Eseguo in modalità JSON (simulazione API su frontend web)
            # Esame: Tecnologie Web (INF01IV)
            print(main_controller('json', JSON_SIMULATO_DAL_WEB))
        else:
            main_controller('manuale')
    except NameError:
        # Fallback estremo se JSON_SIMULATO_DAL_WEB non fosse stato definito
        main_controller('manuale')
