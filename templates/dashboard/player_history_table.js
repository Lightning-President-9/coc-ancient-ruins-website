/* Sort + Utilities */
const HISTORY_TABLE = ".main-table";

/* SORTING */

function initializeHistorySorting() {

	const table = document.querySelector(
		`${HISTORY_TABLE} table`
	);

	if (!table)
		return;

	const headers = table.querySelectorAll("thead th");

	headers.forEach((header, index) => {

		header.style.cursor = "pointer";

		header.addEventListener("click", () => {

			const tbody = table.tBodies[0];

			const rows =
				Array.from(tbody.querySelectorAll("tr"));

			const ascending = !header.classList.contains("asc");

			headers.forEach(h => {

				h.classList.remove(
					"asc",
					"desc",
					"active"
				);

			});

			header.classList.add("active");

			header.classList.add(
				ascending ? "asc" : "desc"
			);

			rows.sort((a, b) => {

				let x =
					a.cells[index]
					.textContent
					.trim();

				let y =
					b.cells[index]
					.textContent
					.trim();

				let nx = Number(x);

				let ny = Number(y);

				if (
					!isNaN(nx) &&
					!isNaN(ny)
				) {

					return ascending ?
						nx - ny :
						ny - nx;

				}

				return ascending ?
					x.localeCompare(y) :
					y.localeCompare(x);

			});

			tbody.innerHTML = "";

			rows.forEach(row => {

				tbody.appendChild(row);

			});

		});

	});

}

/* COMMON HELPERS */

function getHistoryTable() {

	return document.querySelector(
		`${HISTORY_TABLE} table`
	);

}

function downloadFile(
	data,
	filename,
	mimeType
) {

	const blob =
		new Blob(
			[data], {
				type: mimeType
			}
		);

	const url =
		URL.createObjectURL(blob);

	const link =
		document.createElement("a");

	link.href = url;

	link.download = filename;

	document.body.appendChild(link);

	link.click();

	document.body.removeChild(link);

	URL.revokeObjectURL(url);

}

/* TABLE → JSON */

function tableToJSON() {

	const table =
		getHistoryTable();

	const headers = [...table.querySelectorAll("thead th")]
		.map(th =>
			th.textContent.trim()
		);

	const rows = [];

	table
		.querySelectorAll("tbody tr")
		.forEach(row => {

			const obj = {};

			[...row.cells]
			.forEach((cell, i) => {

				obj[
					headers[i]
				] = cell.textContent.trim();

			});

			rows.push(obj);

		});

	return JSON.stringify(
		rows,
		null,
		4
	);

}

/* TABLE → CSV */

function tableToCSV() {

	const table =
		getHistoryTable();

	const csv = [];

	csv.push(

		[...table.querySelectorAll("thead th")]

		.map(th =>
			`"${th.textContent.trim()}"`
		)

		.join(",")

	);

	table
		.querySelectorAll("tbody tr")

		.forEach(row => {

			csv.push(

				[...row.cells]

				.map(cell =>
					`"${cell.textContent.trim()}"`
				)

				.join(",")

			);

		});

	return csv.join("\n");

}

/* EXPORT TO PDF */

function exportHistoryToPDF() {

	const table = getHistoryTable();

	if (!table) {
		alert("Table not found.");
		return;
	}

	const iframe = document.createElement("iframe");

	iframe.style.display = "none";

	document.body.appendChild(iframe);

	const pdfWindow = iframe.contentWindow;
	const pdfDocument = pdfWindow.document;

	pdfDocument.open();

	pdfDocument.write(`
    <html>

    <head>

    <title>{{ player }}'s Monthly Performance History</title>

    <style>

    body{

        font-family:Arial,Helvetica,sans-serif;

        padding:30px;

        background:white;

    }

    h1{

        text-align:center;

        margin-bottom:25px;

    }

    table{

        width:100%;

        border-collapse:collapse;

    }

    th{

        background:#222;

        color:white;

        padding:10px;

        border:1px solid #888;

    }

    td{

        padding:8px;

        border:1px solid #888;

        text-align:center;

    }

    tr:nth-child(even){

        background:#f2f2f2;

    }

    </style>

    </head>

    <body>

    <h1>{{ player }}'s MONTHLY PERFORMANCE HISTORY</h1>

    ${table.outerHTML}

    </body>

    </html>
    `);

	pdfDocument.close();

	pdfWindow.focus();

	pdfWindow.print();

	setTimeout(() => {

		document.body.removeChild(iframe);

	}, 1000);

}

/* JSON EXPORT */

function exportHistoryJSON() {

	const json = tableToJSON();

	downloadFile(

		json,

		"{{ player }}_monthly_history.json",

		"application/json"

	);

}

/* CSV EXPORT */

function exportHistoryCSV() {

	const csv = tableToCSV();

	downloadFile(

		csv,

		"{{ player }}_monthly_history.csv",

		"text/csv"

	);

}

/* EVENT LISTENERS */

const pdfButton =
	document.getElementById(
		"PerformanceTabletoPDFHistory"
	);

if (pdfButton) {

	pdfButton.addEventListener(

		"click",

		exportHistoryToPDF

	);

}

const jsonButton =
	document.getElementById(
		"PerformanceTabletoJSONHistory"
	);

if (jsonButton) {

	jsonButton.addEventListener(

		"click",

		exportHistoryJSON

	);

}

const csvButton =
	document.getElementById(
		"PerformanceTabletoCSVHistory"
	);

if (csvButton) {

	csvButton.addEventListener(

		"click",

		exportHistoryCSV

	);

}

/* EXCEL EXPORT (SheetJS) */

function loadSheetJS(callback) {

	if (window.XLSX) {
		callback();
		return;
	}

	const script = document.createElement("script");

	script.src =
		"https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js";

	script.onload = callback;

	document.head.appendChild(script);

}

function exportHistoryExcel() {

	loadSheetJS(function() {

		const table = getHistoryTable();

		const workbook =
			XLSX.utils.book_new();

		const worksheet =
			XLSX.utils.table_to_sheet(table);

		XLSX.utils.book_append_sheet(

			workbook,

			worksheet,

			"Monthly History"

		);

		XLSX.writeFile(

			workbook,

			"{{ player }}_monthly_history.xlsx"

		);

	});

}

/* EXCEL BUTTON */

const excelButton =
	document.getElementById(
		"PerformanceTabletoEXCELHistory"
	);

if (excelButton) {

	excelButton.addEventListener(

		"click",

		exportHistoryExcel

	);

}

/* INITIALIZATION */

document.addEventListener("DOMContentLoaded", function() {

	initializeHistorySorting();

	document
		.getElementById("PerformanceTabletoPDFHistory")
		?.addEventListener(
			"click",
			exportHistoryToPDF
		);

	document
		.getElementById("PerformanceTabletoJSONHistory")
		?.addEventListener(
			"click",
			exportHistoryJSON
		);

	document
		.getElementById("PerformanceTabletoCSVHistory")
		?.addEventListener(
			"click",
			exportHistoryCSV
		);

	document
		.getElementById("PerformanceTabletoEXCELHistory")
		?.addEventListener(
			"click",
			exportHistoryExcel
		);

});