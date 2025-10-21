import { drawChart } from './charts.js'

let stockChosen = null
let modelChosen = null
const fetchStockBtn = document.getElementById('fetchStockBtn')
const plot = document.getElementById('plot')
const showDataBtn = document.getElementById('showData')
const errorMsgStock = document.getElementById('errorMsgStock')
const errorMsgModel = document.getElementById('errorMsgModel')

const startDate = document.getElementById('startDate')
const endDate = document.getElementById('endDate')


// Nemoznost vybrat end date mensi nez start date a naopak
startDate.addEventListener('change', () => {
  endDate.min = startDate.value
  if (endDate.value && endDate.value < startDate.value) endDate.value = startDate.value
})

endDate.addEventListener('change', () => {
  startDate.max = endDate.value
  if (startDate.value && startDate.value > endDate.value) startDate.value = endDate.value
})



// Uzivatel zada ticker -> poslat ticker na server a vykreslit graf
const stockInput = document.getElementById('stockInput')
stockInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault()
        const stock = stockInput.value.trim()
        if (stock) {
            selectStock(stock)
        } else {
            errorMsgStock.textContent = 'Please enter a stock symbol.'
        }
    }
})

fetchStockBtn.onclick = () => {
    const stock = stockInput.value.trim()
    if (stock) {
        selectStock(stock)
    } else {
        errorMsgStock.textContent = 'Please enter a stock symbol.'
    }
}

// Vybrat akcii a načíst graf
function selectStock(stock) {
    stockChosen = stock

    const stockDataInputs = document.getElementById('stockDataInputs')
    stockDataInputs.style.display = 'block'
    errorMsgStock.textContent = ''
    errorMsgModel.textContent = ''
    plot.style.display = 'none'

    const container = document.getElementById('featuresList')

    container.innerHTML = ""

    modelButtons(availableModels)


    // graf na client side
    fetch(`http://localhost:5055/api/${stockChosen}/ticker`)
        .then(res => res.json())
        .then(data => {
            if (data.data) {
                plot.style.display = 'block'
                drawChart(plot, data.data, stockChosen.toUpperCase())
            } else {
                errorMsgStock.textContent = data.error || 'Error while loading data.'
            }

            // Nastavení rozsahu a výchozích hodnot pro datum z dat ze serveru
            const minDate = data.min_date
            const maxDate = data.max_date

            // nastav rozsahy
            startDate.min = minDate
            startDate.max = maxDate
            endDate.min = minDate
            endDate.max = maxDate

            // výchozí hodnoty (např. start = min, end = max)
            startDate.value = minDate
            endDate.value = maxDate

        })
        .catch(() => {
            errorMsgStock.textContent = 'Error while communicating with server.'
        })
}




const freqList = document.getElementById('freqList')
const freqSelectBtn = document.getElementById('freqSelectBtn')
const buttons = document.querySelectorAll('.freqOption')

buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        selectFreq(btn.textContent, btn.dataset.value)
    })
})

// Zobrazit/skryt seznam frekvencí
freqSelectBtn.onclick = () => {
    if (stockChosen != null) {
        freqList.style.display = freqList.style.display === 'block' ? 'none' : 'block'
    }
}

function selectFreq(displayText, value) {
    freqSelectBtn.textContent = displayText
    freqSelectBtn.dataset.value = value
    freqList.style.display = 'none'
    errorMsgStock.textContent = ''
}




let availableModels = []
// ziskani vsechny dostupne modely
fetch('http://localhost:5055/api/models')
    .then(res => res.json())
    .then(data => {
        if (data.models) {
            availableModels = data.models
        } else {
            errorMsgModel.textContent = data.error || 'Error while loading data.'
        }
    })
    .catch(err => {
        errorMsgModel.textContent = 'Error while communicating with server:' + ' ' + err.message
    })


function clearCapitalizeFirst(str) {
    const clearSr = str.replace(/_/g, ' ').replace(/-/g, ' ') 
    return clearSr.charAt(0).toUpperCase() + clearSr.slice(1)
}




// funkce na zobrazeni dat v tabulatorJS
let table

function showData(columns, rows) {
    if (!table) {
        table = new Tabulator('#dataContent', {
            height: 900,
            data: rows,
            layout: "fitDataStretch",
            autoColumns: true,
            // columns: columns,
            responsiveLayout: false,   // jinak by některé sloupce mizely
        })
    } else {
        table.setData(rows)
    }
}


// zavreni tabulky dat - bud klik vedle nebo esc
function closeTableHandler(e) {
    const dataContent = document.getElementById("dataContent")
    if (!dataContent.contains(e.target)) {
        document.getElementById("dataTable").style.display = "none"
        document.getElementById("dataTable").removeEventListener("mousedown", closeTableHandler)
        document.removeEventListener("keydown", escTableHandler)
    }
}

function escTableHandler(e) {
    if (e.key === "Escape") {
        document.getElementById("dataTable").style.display = "none"
        document.getElementById("dataTable").removeEventListener("mousedown", closeTableHandler)
        document.removeEventListener("keydown", escTableHandler)
    }
}


// Zobrazit/skryt data prohlizec
showDataBtn.onclick = () => {
    errorMsgModel.textContent = ''

    if (freqSelectBtn.textContent === "Choose timeframe") {
        errorMsgModel.textContent = 'Please select a timeframe first.'
        return
    }

    if (window.currentLag) {
        saveFeatures(window.currentLag)
    }

    console.log(lagFeatures)

    document.getElementById("dataTable").style.display = "block"
    document.getElementById("dataTable").addEventListener("mousedown", closeTableHandler)
    document.addEventListener("keydown", escTableHandler)


    fetch(`http://localhost:5055/api/${stockChosen}/df_data`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            features: lagFeatures,
            start_date: startDate.value,
            end_date: endDate.value,
            interval: freqSelectBtn.dataset.value
        }),
    })
    .then(res => res.json())
    .then(data => {
        if (data.df) {
            const columns = data.df.columns.map(col => clearCapitalizeFirst(col))
            const rows = data.df.data.map(row =>
                Object.fromEntries(columns.map((col, i) => [col, row[i]]))
            )
            console.log(rows)
            showData(columns, rows)
        } else {
            errorMsgStock.textContent = data.error || 'Error while loading data.'
        }
    })
    .catch(() => {
        errorMsgStock.textContent = 'Error while communicating with server.'
    })
}





// Výběr modelů
const modelList = document.getElementById('modelList')
const modelSelectBtn = document.getElementById('modelSelectBtn')

function clearModelName(name) {
    return name.replace(/_/g, ' ').replace(/-/g, ' ').toUpperCase()
}


function modelButtons(models) {
    modelList.innerHTML = ""

    models.forEach(model => {
        const btn = document.createElement('button')
        btn.textContent = clearModelName(model)
        btn.onclick = () => selectModel(model)
        modelList.appendChild(btn)
    })
}

// Zobrazit/skryt seznam modelů
modelSelectBtn.onclick = () => {
    if (stockChosen != null) {
        modelList.style.display = modelList.style.display === 'block' ? 'none' : 'block'
    }
}


function selectModel(model) {
    modelChosen = model
    modelSelectBtn.textContent = clearModelName(model)
    modelList.style.display = 'none'
    errorMsgModel.textContent = ''
}




// Dynamický výpis feature checkboxů a lagů
let availableFeatures = ["log_return", "high", "low", "close", "volume", "ema10", "ema50", "rsi", "atr"]
let lagFeatures = {}

function showFeatures(features, lag) {
    const container = document.getElementById('featuresList')
    container.innerHTML = ""

    features.forEach(feature => {
        const label = document.createElement('label')
        label.style.display = 'block'
        const checkbox = document.createElement('input')
        checkbox.type = 'checkbox'
        checkbox.value = feature
        checkbox.name = 'feature'
        // Pokud byl feature pro tento lag zaškrtnut, zaškrtni ho
        if (lagFeatures[lag] && lagFeatures[lag].includes(feature)) {
            checkbox.checked = true
        }
        label.appendChild(checkbox)
        label.appendChild(document.createTextNode(' ' + clearCapitalizeFirst(feature)))
        container.appendChild(label)
    })
}

function saveFeatures(lag) {
    const container = document.getElementById('featuresList')
    const checkedFeatures = Array.from(
        container.querySelectorAll('input[type="checkbox"]:checked')
    ).map(cb => cb.value)

    lagFeatures[lag] = checkedFeatures
}

// zmena lagu a ukladani vybranych features
const radios = document.querySelectorAll('input[type="radio"][name="lag"]')
radios.forEach(radio => {
    radio.addEventListener('change', function() {
        if (stockChosen == null) {
            alert('Choose a stock first.')
            this.checked = false
            return
        } else if (modelChosen == null) {
            alert('Choose a model first.')
            this.checked = false
            return
        } else {
            // Ulož výběr pro předchozí lag
            if (window.currentLag) {
                saveFeatures(window.currentLag)
            }
            window.currentLag = this.value
            // Znovu vykresli checkboxy pro nový lag
            showFeatures(availableFeatures, this.value)
        }
    })
})

radios.forEach(radio => radio.checked = false)



// Learning Rate a epochy ttSplit
const eSlider = document.getElementById('epochsSlider')
const eNumberInput = document.getElementById('epochsNumber')

// Když se posune slider → aktualizuje number input
eSlider.addEventListener('input', () => {
    eNumberInput.value = eSlider.value
})

// Když uživatel změní number input → aktualizuje slider
eNumberInput.addEventListener('input', () => {
    let val = Number(eNumberInput.value)
    if (val < 1) val = 1        // minimum
    if (val > 10000) val = 10000    // maximum
    eNumberInput.value = val
    eSlider.value = val
})


const lrSlider = document.getElementById('learningRateSlider')
const lrNumberInput = document.getElementById('learningRateNumber')

// Když se posune slider → aktualizuje number input
lrSlider.addEventListener('input', () => {
    lrNumberInput.value = lrSlider.value
})

// Když uživatel změní number input → aktualizuje slider
lrNumberInput.addEventListener('input', () => {
    let val = Number(lrNumberInput.value)
    if (val < 0.0001) val = 0.0001        // minimum
    if (val > 1) val = 1    // maximum
    lrNumberInput.value = val
    lrSlider.value = val
})

const ttSplitSlider = document.getElementById('ttSplitSlider')
const ttSplitNumber = document.getElementById('ttSplitNumber')

// Když se posune slider → aktualizuje number input
ttSplitSlider.addEventListener('input', () => {
    ttSplitNumber.value = ttSplitSlider.value
})

// Když uživatel změní number input → aktualizuje slider
ttSplitNumber.addEventListener('input', () => {
    let val = Number(ttSplitNumber.value)
    if (val < 0) val = 0        // minimum
    if (val > 100) val = 100    // maximum
    ttSplitNumber.value = val
    ttSplitSlider.value = val
})


// podminky pro validitu vstupnich parametru do modelu
const trainBtn = document.getElementById('trainBtn')
trainBtn.onclick = () => {
    errorMsgModel.textContent = ''

    if (window.currentLag) {
        saveFeatures(window.currentLag)
    }

    if (stockChosen == null) {
        errorMsgStock.textContent = 'Choose a stock first.'
        return
    } else if (modelChosen == null) {
        errorMsgModel.textContent = 'Choose a model first.'
        return
    } else if (Object.values(lagFeatures).map(arr => !arr.length).every(x => x === true)) {
        errorMsgModel.textContent = 'Select atleast one feature first.'
        return
    } else {
        trainModel()
    }
}


// Odeslání požadavku na trénování modelu
function trainModel() {
    let modelParams = {
        model_type: modelChosen,
        features: lagFeatures,
        learning_rate: parseFloat(lrNumberInput.value),
        epochs: parseInt(eNumberInput.value),
        tt_split: parseInt(ttSplitNumber.value)
    }

    let stockInfo = {
        start_date: startDate.value,
        end_date: endDate.value,
        interval: freqSelectBtn.dataset.value
    }


    fetch(`http://localhost:5055/api/${stockChosen}/train`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "model_params": modelParams, "stock_info": stockInfo })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert(data.message)
            } else {
                errorMsgModel.textContent = data.error || 'Error while training model.'
            }
        })
        .catch(() => {
            errorMsgModel.textContent = 'Error while communicating with server.'
        })
}
