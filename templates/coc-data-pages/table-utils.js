// UNIVERSAL TABLE UTILS
// Search | Sort | Export (PDF / JSON / CSV / EXCEL)

// Helpers
function cleanHeader(text) {
	return text.replace(/[↑↓]/g, '').replace(/\n/g, '').trim();
}

function getTableFromButton(btn) {
	return btn.closest('main, .main-table')?.querySelector('table');
}

function visibleRows(table) {
	return Array.from(table.querySelectorAll('tbody tr'))
		.filter(row => !row.classList.contains('hide'));
}

function getCellValue(cell) {
	const img = cell.querySelector('img');
	if (img) {
		// Prefer image URL, not alt text
		return img.getAttribute('src') || img.getAttribute('alt') || '';
	}
	return cell.textContent.trim();
}

// SEARCH (Generic)
document.addEventListener('input', function(e) {
	const input = e.target.closest('.input-group input');
	if (!input) return;

	const tbody = input.closest('main, .main-table')
		?.querySelector('tbody');
	if (!tbody) return;

	const value = input.value.toLowerCase();

	tbody.querySelectorAll('tr').forEach(row => {
		row.classList.toggle(
			'hide',
			!row.textContent.toLowerCase().includes(value)
		);
	});
});

// SORTING (Arrow Click)
document.addEventListener('click', function(e) {
	const th = e.target.closest('th');
	if (!th || !th.closest('table')) return;

	const table = th.closest('table');
	const tbody = table.querySelector('tbody');
	if (!tbody) return;

	const headers = Array.from(th.parentNode.children);
	const index = headers.indexOf(th);
	const order = th.dataset.order || 'asc';

	headers.forEach(h => {
		h.removeAttribute('data-order');
		h.classList.remove('active');
		const arrow = h.querySelector('.icon-arrow');
		if (arrow) arrow.style.transform = '';
	});

	const rows = Array.from(tbody.querySelectorAll('tr'));

	rows.sort((a, b) => {
		let A = a.children[index].textContent.trim();
		let B = b.children[index].textContent.trim();

		const numA = parseFloat(A.replace(/[^0-9.-]/g, ''));
		const numB = parseFloat(B.replace(/[^0-9.-]/g, ''));

		if (!isNaN(numA) && !isNaN(numB)) {
			return order === 'asc' ? numA - numB : numB - numA;
		}
		return order === 'asc' ?
			A.localeCompare(B) :
			B.localeCompare(A);
	});

	th.dataset.order = order === 'asc' ? 'desc' : 'asc';
	th.classList.add('active');

	const arrow = th.querySelector('.icon-arrow');
	if (arrow) arrow.style.transform = order === 'asc' ? 'rotate(180deg)' : '';

	tbody.append(...rows);
});

// EXPORT → JSON
function exportJSON(table) {
	const headers = Array.from(table.querySelectorAll('thead th'))
		.map(th => cleanHeader(th.textContent));

	const data = visibleRows(table).map(row => {
		const obj = {};
		Array.from(row.cells).forEach((cell, i) => {
			obj[headers[i]] = getCellValue(cell);
		});
		return obj;
	});

	download(
		JSON.stringify(data, null, 4),
		'table-data.json',
		'application/json'
	);
}

// EXPORT → CSV
function exportCSV(table) {
	const headers = Array.from(table.querySelectorAll('thead th'))
		.map(th => cleanHeader(th.textContent));

	const rows = visibleRows(table).map(row =>
		Array.from(row.cells)
		.map(cell => `"${getCellValue(cell)}"`)
		.join(',')
	);

	download(
		[headers.join(','), ...rows].join('\n'),
		'table-data.csv',
		'text/csv'
	);
}

// EXPORT → PDF (↑ removed)
function exportPDF(table) {
	const clone = table.cloneNode(true);
	clone.querySelectorAll('th').forEach(th => {
		th.textContent = cleanHeader(th.textContent);
	});

	const iframe = document.createElement('iframe');
	iframe.style.display = 'none';
	document.body.appendChild(iframe);

	const doc = iframe.contentWindow.document;
	doc.open();
	doc.write(`
        <html>
        <head>
            <style>
                body { font-family: Arial; }
                table { width:100%; border-collapse:collapse; }
                th, td { border:1px solid #000; padding:6px; }
                th { background:#000; color:#fff; }
            </style>
        </head>
        <body>${clone.outerHTML}</body>
        </html>
    `);
	doc.close();

	iframe.contentWindow.print();
	setTimeout(() => document.body.removeChild(iframe), 1000);
}

// SHEETJS LOADER
function includeSheetJSLibrary() {
	if (window.XLSX) return; // already loaded

	const script = document.createElement('script');
	script.src = 'https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js';
	script.onload = function() {
		//console.log('SheetJS loaded');
	};
	document.head.appendChild(script);
}
includeSheetJSLibrary();

// EXPORT → EXCEL
function exportExcel(table) {
	if (!window.XLSX) {
		alert('Excel library not loaded');
		return;
	}

	const clone = table.cloneNode(true);

	// Clean headers
	clone.querySelectorAll('th').forEach(th => {
		th.textContent = cleanHeader(th.textContent);
	});

	// Replace images with IMAGE URL
	clone.querySelectorAll('td').forEach(td => {
		const img = td.querySelector('img');
		if (img) {
			td.textContent = img.getAttribute('src') || '';
		}
	});

	const wb = XLSX.utils.book_new();
	const ws = XLSX.utils.table_to_sheet(clone);
	XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
	XLSX.writeFile(wb, 'table-data.xlsx');
}

// DOWNLOAD HELPER
function download(content, filename, type) {
	const blob = new Blob([content], {
		type
	});
	const a = document.createElement('a');
	a.href = URL.createObjectURL(blob);
	a.download = filename;
	a.click();
	URL.revokeObjectURL(a.href);
}

// AUTO-WIRE EXPORT BUTTONS
document.addEventListener('click', function(e) {
	const btn = e.target.closest('[id^="to"]');
	if (!btn) return;

	const table = getTableFromButton(btn);
	if (!table) return;

	if (btn.id.includes('PDF')) exportPDF(table);
	if (btn.id.includes('JSON')) exportJSON(table);
	if (btn.id.includes('CSV')) exportCSV(table);
	if (btn.id.includes('EXCEL')) exportExcel(table);
});