import { drawChart } from './chart.js'

let stockChosen = null
let modelChosen = null
const stockList = document.getElementById('stockList')
const selectBtn = document.getElementById('selectBtn')
const plot = document.getElementById('plot')
const errorMsgStock = document.getElementById('errorMsgStock')
const errorMsgModel = document.getElementById('errorMsgModel')


let availableStocks = []
// ziskani seznamu akcii ze serveru
fetch('http://localhost:5000/api/stocks')
    .then(res => res.json())
    .then(data => {
        if (data.stocks) {
            availableStocks = data.stocks

            stockButtons(availableStocks)
        } else {
            errorMsgStock.textContent = data.error || 'Error while loading data.'
        }
    })
    .catch(err => {
        errorMsgStock.textContent = 'Error while communicating with server:' + ' ' + err.message
    })


let availableModels = []
// ziskani vsechny dostupne modely
fetch('http://localhost:5000/api/models')
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


// Vytvoření seznamu tlačítek pro akcie
function stockButtons(stocks) {
    stocks.forEach(stock => {
        const btn = document.createElement('button')
        btn.textContent = stock.toUpperCase()
        btn.onclick = () => selectStock(stock)
        stockList.appendChild(btn)
    })
}

// Zobrazit/skryt seznam akcií
selectBtn.onclick = () => {
    stockList.style.display = stockList.style.display === 'block' ? 'none' : 'block'
}

function clearCapitalizeFirst(str) {
    clearSr = str.replace(/_/g, ' ').replace(/-/g, ' ') 
    return clearSr.charAt(0).toUpperCase() + clearSr.slice(1)
}






// Vybrat akcii a načíst graf
function selectStock(stock) {
    stockChosen = stock
    availableFeatures = []


    selectBtn.textContent = stock.toUpperCase()
    stockList.style.display = 'none'
    errorMsgStock.textContent = ''
    errorMsgModel.textContent = ''
    plot.style.display = 'none'

    const container = document.getElementById('featuresList')

    container.innerHTML = ""

    modelButtons(availableModels)


    // graf na client side
    fetch(`http://localhost:5000/api/stock/${stock}/data`)
        .then(res => res.json())
        .then(data => {
            if (data.data) {
                plot.style.display = 'block'
                drawChart(plot, data.data, stockChosen.toUpperCase())
            } else {
                errorMsgStock.textContent = data.error || 'Error while loading data.'
            }
        })
        .catch(() => {
            errorMsgStock.textContent = 'Error while communicating with server.'
        })


    
    fetch(`http://localhost:5000/api/get_features/${stock}`)
        .then(res => res.json())
        .then(data => {

            if (data.features) {
                const features = data.features
                availableFeatures = features
            } else {
                errorMsgModel.textContent = data.error || 'Error while loading data.'
            }
        })
        .catch(() => {
            errorMsgModel.textContent = 'Error while communicating with server.'
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
let availableFeatures = []
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



// Learning Rate a epochy
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


function trainModel() {
    let modelParams = {}

    modelParams.model_type = modelChosen
    modelParams.features = lagFeatures
    modelParams.learning_rate = parseFloat(lrNumberInput.value)
    modelParams.epochs = parseInt(eNumberInput.value)


    fetch(`http://localhost:5000/api/${stockChosen}/train`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(modelParams)
    })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                errorMsgModel.style.color = 'green'
                errorMsgModel.textContent = data.message
            } else {
                errorMsgModel.textContent = data.error || 'Error while training model.'
            }
        })
        .catch(() => {
            errorMsgModel.textContent = 'Error while communicating with server.'
        })
}