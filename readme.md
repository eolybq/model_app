# Project Documentation `model_app`

## Project Structure
model_app/
├── backend/
│   ├── main.py             # main Python file for the Flask backend server
│   ├── data/
│   │   └── # central folder with global data for each stock, full time series with daily intervals
│   ├── models/
│   │   └── # Python scripts with various prediction models
│   ├── rnn/
│   │   └── # folder for handling larger RNN models, storing checkpoints and trained .keras models
│   └── services/
│       └── # Python scripts for data manipulation – from API fetching, preprocessing, feature calculations, to creating lags
├── frontend/
│   ├── index.html           # main frontend HTML file
│   ├── js/
│       └── # frontend scripts using JavaScript


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


## Tools used
- Python (Pandas, Numpy, Tensorflow, Flask)
- JS (Chart.js, Tabulator.js)
- HTML, CSS