export function drawChart(containerId, data, stockName) {
    const dates = data.map(item => item.date)
    const prices = data.map(item => item.adjusted)

    const trace = {
        x: dates,
        y: prices,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: 'blue' },
        line: { shape: 'linear' }
    }
    const layout = {
        title: {
            text: `${stockName} price over time`,
            font: { size: 20 }
        }
    }

    Plotly.newPlot(containerId, [trace], layout)
}