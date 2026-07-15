/* Dashboard Initialization */
document.addEventListener("DOMContentLoaded", () => {

	renderTimeline();

	renderDonut();

	renderComparison();

	renderHeatmap();

});

function renderTimeline() {

	Plotly.newPlot(

		"timeline-chart",

		JSON.parse(
			dashboard.graphs.timeline
		).data,

		JSON.parse(
			dashboard.graphs.timeline
		).layout,

		{
			responsive: true,
			displaylogo: false
		}

	);

}

function renderDonut() {

	Plotly.newPlot(

		"donut-chart",

		JSON.parse(
			dashboard.graphs.donut
		).data,

		JSON.parse(
			dashboard.graphs.donut
		).layout,

		{
			responsive: true,
			displaylogo: false
		}

	);

}

function renderComparison() {

	Plotly.newPlot(

		"comparison-chart",

		JSON.parse(
			dashboard.graphs.comparison
		).data,

		JSON.parse(
			dashboard.graphs.comparison
		).layout,

		{
			responsive: true,
			displaylogo: false
		}

	);

}

function renderHeatmap() {

	Plotly.newPlot(

		"heatmap-chart",

		JSON.parse(
			dashboard.graphs.heatmap
		).data,

		JSON.parse(
			dashboard.graphs.heatmap
		).layout,

		{
			responsive: true,
			displaylogo: false
		}

	);

}