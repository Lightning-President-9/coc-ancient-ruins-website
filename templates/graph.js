let graphJSON_list = {{ graphJSON_list | tojson | safe }};
let container = document.getElementById('charts-container');

function renderCharts(graphJSON_list) {
    container.innerHTML = '';
    graphJSON_list.forEach((graphJSON, index) => {
        let chartDiv = document.createElement('div');
        chartDiv.id = 'chart' + (index + 1);
        chartDiv.classList.add('chart');
        container.appendChild(chartDiv);
        let graph = JSON.parse(graphJSON);
        Plotly.newPlot(chartDiv.id, graph.data, graph.layout, {responsive: true});
    });
}

document.getElementById('fetch-button').addEventListener('click', function(event) {
    event.preventDefault();

    let month = document.getElementById('month-select').value;
    let year = document.getElementById('year-select').value;
    let month_year = month + '_' + year;

    let form = document.getElementById('fetch-data-form');
    let hiddenInput = form.querySelector('input[name="month-year"]');

    if (!hiddenInput) {
        hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'month-year';
        form.appendChild(hiddenInput);
    }

    hiddenInput.value = month_year;

    form.submit();
});

renderCharts(graphJSON_list);