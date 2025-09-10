# Dokumentace projektu `model_app`

## 1. Struktura projektu
model_app/
│
├─ data/
│ └─ tsla.csv # CSV soubor s daty akcie
│
├─ static/
│ ├─ index.html # frontend stránka
│ ├─ script.js # JS pro interakci s backendem
│ └─ style.css # CSS styly
│
├─ .env # environmentální proměnné (např. SECRET_KEY)
└─ main.py # hlavní Flask backend



## 2. Instalace

Vytvořit virtuální prostředí:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```
Instalace závislostí:
```
pip install requirements.txt
```
⚠️ Používáme matplotlib.use('Agg') kvůli headless režimu (bez GUI), což je vhodné pro server.

## 3. Spuštění serveru
```
python main.py
```
Backend běží na http://127.0.0.1:5000

Debug mód je zapnutý (debug=True)

## 4. API Endpoints
### 4.1 /api/stock/<stock> [GET]
Vrátí graf ceny akcie jako Base64 obrázek.
Parametry:

stock – název akcie, např. tsla.

### 4.2 /api/get_features/<stock> [GET]
Vrátí seznam dostupných feature (sloupců) v CSV souboru kromě date.

#### Parametry:

stock – název akcie.

#### Odpověď:

{
  "features": ["adjusted", "open", "high", "low", "volume"]
}

### 4.3 /api/stock/<stock>/model [POST]
Aktualizuje parametry modelu.

#### Parametry v těle requestu (JSON):
{
  "model_type": "grad",

  "features": ["adjusted", "rsi", "ema_lag3"],

  "learning_rate": 0.01,

  "epochs": 100,

  "batch_size": 32
}

#### Odpověď:
{
  "message": "Model parameters updated",

  "model_params": {

    "model_type": "grad",
    "features": ["adjusted", "rsi", "ema_lag3"],
    "learning_rate": 0.01,
    "epochs": 100,
    "batch_size": 32
  }
}

## 5. Interní funkce

### 5.1 load_data(stock)
Načte CSV soubor z data/<stock>.csv do pandas.DataFrame.
### 5.2 df_to_base64(df)
Vytvoří graf z dataframe a vrátí jej jako Base64 string.

Používá Matplotlib s backendem Agg.
### 5.3 lag_features(df, features)
Přidá sloupce s lagy podle názvu feature.

Pokud název obsahuje _lagN (např. ema_lag3), vezme základní sloupec (ema) a posune o N řádků.

Odstraní NaN řádky vzniklé posunem.

Výsledek: dataframe připravený pro model.