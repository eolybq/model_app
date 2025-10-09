export function drawChart(containerId, data, stockName) {
    const dates = data.map(item => item.date)
    const prices = data.map(item => item.adjusted)

    const trace = {
        x: dates,
        y: prices,
        type: 'scatter',
        mode: 'lines',
        // mode: 'lines+markers',
        // marker: { color: 'blue', size: 4 },
        line: { shape: 'linear', color: 'blue', width: 2 },
    }
    const layout = {
        title: {
            text: `${stockName} price over time`,
            font: { size: 20 }
        },
        xaxis: { title: { text: 'Date', font: { size: 12 } } },
        yaxis: { title: { text: 'Price (USD)', font: { size: 12 } } }
    }

    Plotly.newPlot(containerId, [trace], layout)
}