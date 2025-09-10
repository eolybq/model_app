let stockChosen = false
const stockList = document.getElementById('stockList')
const selectBtn = document.getElementById('selectBtn')
const plot = document.getElementById('plot')
const errorMsgStock = document.getElementById('errorMsgStock')
const errorMsgModel = document.getElementById('errorMsgModel')


// ziskani seznamu akcii ze serveru
fetch('http://localhost:5000/api/stocks')
    .then(res => res.json())
    .then(data => {
        if (data.stocks) {
            const stocks = data.stocks
    
            stockButtons(stocks)
        } else {
            errorMsgStock.textContent = data.error || 'Chyba při načítání dat.'
        }
    })
    .catch(err => {
        errorMsgStock.textContent = 'Chyba při komunikaci se serverem:' + ' ' + err.message
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

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1)
}






// Vybrat akcii a načíst graf
function selectStock(stock) {
    stockChosen = true
    availableFeatures = []


    selectBtn.textContent = stock.toUpperCase()
    stockList.style.display = 'none'
    errorMsgStock.textContent = ''
    errorMsgModel.textContent = ''
    plot.style.display = 'none'

    const container = document.getElementById('featuresList')

    modelButtons(models)


    container.innerHTML = ""
    fetch(`http://localhost:5000/api/stock/${stock}`)
        .then(res => res.json())
        .then(data => {
            if (data.image) {
                plot.src = `data:image/png;base64,${data.image}`
                plot.style.display = 'block'
            } else {
                errorMsgStock.textContent = data.error || 'Chyba při načítání dat.'
            }
        })
        .catch(() => {
            errorMsgStock.textContent = 'Chyba při komunikaci se serverem.'
        })
    
    fetch(`http://localhost:5000/api/get_features/${stock}`)
        .then(res => res.json())
        .then(data => {

            if (data.features) {
                const features = data.features
                availableFeatures = features
            } else {
                errorMsgModel.textContent = data.error || 'Chyba při načítání dat.'
            }
        })
        .catch(() => {
            errorMsgModel.textContent = 'Chyba při komunikaci se serverem.'
        })
}




// Výběr modelů
// TODO: mozna dynamicky zas na zaklade souboru s modely?
// TODO: DODELAT MODEL_PARAMS tak aby sedelo s py -> mozna tam pak nacpat i ty features -> zajistit predani model type, a zbytek params a taky feature na server

let model_params = {
    "model_type": "",
    "features": [],
    "learning_rate": 0.01,
    "epochs": 100,
    "batch_size": 32
}

const models = ['Gradient descent LR', 'Gradient descent logit', 'ARIMA', 'RNN']
const modelList = document.getElementById('modelList')
const modelSelectBtn = document.getElementById('modelSelectBtn')

function modelButtons(models) {
    models.forEach(model => {
        const btn = document.createElement('button')
        btn.textContent = model
        btn.onclick = () => selectModel(model)
        modelList.appendChild(btn)
    })
}

// Zobrazit/skryt seznam modelů
modelSelectBtn.onclick = () => {
    modelList.style.display = modelList.style.display === 'block' ? 'none' : 'block'
}

function selectModel(model) {
    modelSelectBtn.textContent = model
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
        label.appendChild(document.createTextNode(' ' + capitalizeFirst(feature)))
        container.appendChild(label)
    })
}

function saveFeatures(lag) {
    const container = document.getElementById('featuresList')
    const checkedFeatures = Array.from(
        container.querySelectorAll('input[type="checkbox"]:checked')
    ).map(cb => cb.value)
    // const laggedFeatures = checkedFeatures.map(f => `${f}_${lag}`)

    lagFeatures[lag] = checkedFeatures
}

const radios = document.querySelectorAll('input[type="radio"][name="lag"]')
radios.forEach(radio => {
    radio.addEventListener('change', function() {
        if (!stockChosen) {
            alert('Nejprve vyberte akcii.')
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
