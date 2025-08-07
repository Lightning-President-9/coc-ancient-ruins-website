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
        document.getElementById('fetch-data-form').action = window.location.href;

        document.getElementById('fetch-button').addEventListener('click', function() {

        });
        renderCharts(graphJSON_list);