# 🍇 Timpe Smart Vineyard - Digital Twin Project

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/Viz-Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

> **Project Work:** Sviluppo di un codice python per simulare un processo produttivo nel settore primario.

---

## 🎯 Obiettivo del Progetto Work

Questo lavoro propone una modellazione software della filiera produttiva agroalimentare in un ottica di Agricoltura 4.0, focalizzandosi sul settore vitivinicolo. Ho progettato e sviluppato un Simulatore Digitale (Digital Twin) con l'obiettivo di:
1.  **Gestire 3 Linee di Prodotto:** Barbera, Aglianico e Moscato.
2.  **Simulare 2 Flussi di Lavorazione:** Vinificazione in Rosso (macerazione) e in Bianco (pressatura soffice).
3.  **Calcolare Output e Sottoprodotti:** Stima della produzione di vino finito e della biomassa di scarto (Vinaccia) per l'economia circolare.

Il sistema applica concetti trasversali appresi durante il percorso di studi, come ad esempio: **Programmazione OOP**, **Calcolo, Probabilità e Statistica**, **Reti di calcolatori e Cybersecurity**, **Algoritmi e strutture dati**, **Basi di Dati**, **Ingegneria del Software**, e altri.

---

## ⚙️ Il Cuore del Sistema: `Simulatore.py`

Questo modulo rappresenta il **requisito fondamentale** del Project Work. È uno script Python puro che modella la logica di business dell'azienda vitivinicola.

### Caratteristiche Tecniche:
* **Modellazione OOP:** Utilizzo di classi (`SimulatoreLottoVigneto`) per rappresentare ogni appezzamento di terreno come un oggetto con stato e comportamenti.
* **Simulazione IoT:** Una funzione dedicata genera dati stocastici (meteo, temperatura, rischio patogeni) simulando una rete di sensori in campo.
* **Logica Condizionale:** Algoritmi che adattano la resa in base a variabili input (concimi, trattamenti fitosanitari, meteo).
* **Calcolo Tempi:** Stima delle ore-uomo necessarie per le fasi di *Raccolta*, *Trasformazione* e *Gestione Aziendale*.

---

## 💻 Dashboard Web & Frontend (Extra)

*Questa sezione rappresenta un'implementazione aggiuntiva sviluppata volontariamente per fornire un'interfaccia grafica (GUI) al simulatore.*

Per rendere i dati del simulatore fruibili e leggibili, ho realizzato una **Dashboard Web Interattiva**.
All'interno della cartella `Dashboard Web`:

* **`app.py` (Flask Server):** Agisce da "ponte". Riceve le richieste dal browser, esegue il codice di calcolo `Simulatore.py` e restituisce i risultati in formato JSON.
* **`templates/index.html` (Frontend):** L'interfaccia utente.
    * Permette la configurazione dei parametri (ettari, piante, capacità lavorativa).
    * Visualizza i risultati tramite grafici animati (**Chart.js**) per un'analisi immediata dei KPI.
    * Comunica con il backend tramite chiamate asincrone (Fetch API).

⭐️ La Dashboard è accessibile dal mio dominio: https://projectwork.capozzoli.me

---

## 🌐 Infrastruttura di Rete e Deployment

Il progetto non è stato concepito solo per l'esecuzione locale (o debug), ma è stato deployato anche su un'infrastruttura server reale e personale *(la utilizzo già per altri progetti lavorativi e hobbistici)*.

### Setup "On-Premise":
* **Host:** Server fisico Windows.
* **Virtualizzazione:** Esecuzione isolata tramite Python Virtual Environment (`venv`) per la gestione delle dipendenze.
* **Gestione IP Dinamico (DDNS Custom):**
    * Poiché la connettività del server si basa su un IP pubblico dinamico, ho sviluppato uno **script di automazione** lato server *(pre-sviluppato per i miei progetti)*.
    * Lo script monitora l'IP e interagisce direttamente con le **API del mio provider Hosting** per aggiornare in tempo reale il **Record DNS di tipo "A"**, garantendo la continua raggiungibilità del dominio.
* **Sicurezza e Accesso Esterno:**
    * Utilizzo di **Zoraxy** come Reverse Proxy per filtrare il traffico.
    * Configurazione di **Certificati SSL** per garantire connessioni cifrate (HTTPS).
    * Gestione del routing dal dominio pubblico alla porta locale del servizio Flask.

---

## 📸 Anteprima Dashboard

La dashboard offre un controllo completo sui 3 lotti principali dell'azienda:
1.  **Lotto 1:** Barbera (Rosso)
2.  **Lotto 2:** Aglianico (Rosso Tardivo)
3.  **Lotto 3:** Moscato (Bianco)

*Grafici dinamici mostrano in tempo reale:*
* Produzione in Kg/Litri.
* Percentuali di scarto e biomassa.
* Tempi di lavorazione di tutte le fasi.

---

### 📂 Struttura della Repository
```text
/
├── 📄 Simulatore.py          # Logica Core (Il Project Work)
├── 📂 Dashboard Web
│   ├── 📄 app.py             # Server Web Flask
│   └── 📂 templates
│       └── 📄 index.html     # Dashboard Grafica
└── 📄 README.md              # Documentazione
