function renderLineChart(canvasId, labels, datasets, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (window['chart_' + canvasId]) window['chart_' + canvasId].destroy();

    window['chart_' + canvasId] = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: { display: !!title, text: title, font: { size: 14 } },
                legend: { display: datasets.length > 1 }
            },
            scales: { y: { beginAtZero: true, max: 100 } },
            elements: { point: { radius: 3 }, line: { tension: 0.3 } }
        }
    });
}

function renderDoughnutChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (window['chart_' + canvasId]) window['chart_' + canvasId].destroy();

    window['chart_' + canvasId] = new Chart(ctx, {
        type: 'doughnut',
        data: { labels, datasets: [{ data, backgroundColor: colors, borderWidth: 0 }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            cutout: '65%'
        }
    });
}
