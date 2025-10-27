# Project Documentation `model_app`
- ! THIS PROJECT IS CURRENTLY IN-PROGRESS - SOME FEATURES AREN'T IMPLEMENTED YET.
- CSS isn't fully done aswell

- This project creates website, where user can fetch live financial data for pleasured stock ticker, then choose statstical or machine learning model, tune according hyperparameters and watch how model performs in these conditions. 
- User can tweak parametrs of stock data aswell - choose freqency (1 day, 1 week, 1 month, 3 months), start/end time


## Tools used
- Python (Pandas, Numpy, Statsmodels, Tensorflow, Flask, yfinance - Yahoo finance API)
- JS (Chart.js, Tabulator.js)
- HTML, CSS


## Installation

Create Conda environment from `environment.yml`:

```bash
conda env create -f backend/environment.yml
conda activate <environment_name>
```


## Running the python server
```
cd backend/
python main.py
```
Backend runs at http://localhost:5055

Debug mode is currently enabled (debug=True)


## Screenshots
