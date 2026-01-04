// Function to handle the search logic for a given table class
function handleSearch(tableClass) {
    // Get the search input and table rows for the specified table class
    const searchInput = document.querySelector(`.${tableClass} .input-group input`);
    const tableRows = document.querySelectorAll(`.${tableClass} .table-body tbody tr`);

    // Add an input event listener to the search input
    searchInput.addEventListener('input', searchTable);

    // Function to handle the search logic
    function searchTable() {
        const searchValue = searchInput.value.toLowerCase();

        // Loop through each table row and check if it matches the search value
        tableRows.forEach(row => {
            const rowData = row.textContent.toLowerCase();
            const isVisible = rowData.includes(searchValue);
            row.classList.toggle('hide', !isVisible);
        });
    }
}

// Call the function for each table class
handleSearch('main-table');
handleSearch('main-not-member-table');
handleSearch('score-table');

// Sorting | Ordering data of HTML table

document.addEventListener('DOMContentLoaded', function () {
    const tableHeaders = document.querySelectorAll('.table-body th');

    tableHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const table = header.closest('table');
            const tbody = table.querySelector('tbody');
            const headerIndex = Array.prototype.indexOf.call(header.parentNode.children, header);
            const currentOrder = header.getAttribute('data-order') || 'asc';

            // Remove active class and arrow icon from other headers
            tableHeaders.forEach(th => {
                th.classList.remove('active');
                th.removeAttribute('data-order');

                // Reset arrow styles
                const arrowIcon = th.querySelector('span.icon-arrow');
                if (arrowIcon) {
                    arrowIcon.style.transform = '';
                }
            });

            // Sort the table rows based on the clicked header
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const sortedRows = rows.sort((a, b) => {
                const aValue = a.children[headerIndex].textContent.trim();
                const bValue = b.children[headerIndex].textContent.trim();

                if (isNaN(aValue) || isNaN(bValue)) {
                    return currentOrder === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
                } else {
                    return currentOrder === 'asc' ? aValue - bValue : bValue - aValue;
                }
            });

            // Toggle between ascending and descending order
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            header.setAttribute('data-order', newOrder);

            // Add active class to the clicked header
            header.classList.add('active');

            // Update arrow styles
            const arrowIcon = header.querySelector('span.icon-arrow');
            if (arrowIcon) {
                arrowIcon.style.transform = currentOrder === 'asc' ? 'rotate(180deg)' : '';
            }

            // Append sorted rows back to the table
            tbody.innerHTML = '';
            sortedRows.forEach(row => {
                tbody.appendChild(row);
            });
        });
    });
});

//Converting HTML table to PDF

// Function to export table to PDF
function exportTableToPDF(tableClass) {
    // Mapping object for custom table names
    const customTableNames = {
        'main-table': 'CLAN MEMBERS TABLE',
        'main-not-member-table': 'FORMER CLAN MEMBERS TABLE',
        'score-table': 'TOP CLAN CONTRIBUTORS TABLE'
    };

    // Get the custom name for the table class
    const customName = customTableNames[tableClass];

    // Get the table element
    const table = document.querySelector(`.${tableClass} table`);

    if (!table) {
        console.error('Table element not found.');
        return; // Exit the function if table is null
    }

    // Filter out rows with null values
    const tableRows = Array.from(table.querySelectorAll('tbody tr')).filter(row => {
        return Array.from(row.children).every(cell => cell.textContent.trim() !== '');
    });

    // Get the table header
    const tableHeader = table.querySelector('thead').outerHTML;

    // Get table styles
    const tableStyles = getComputedStyle(table);

    // Create a new PDF document
    const pdfDocument = document.createElement('iframe');
    pdfDocument.style.display = 'none';
    document.body.appendChild(pdfDocument);
    const pdfWindow = pdfDocument.contentWindow;
    const pdfDocumentContent = pdfWindow.document;

    // Create a header for the PDF with the custom table name
    pdfDocumentContent.write('<html><head><title>Table Data</title></head><body>');
    pdfDocumentContent.write('<style>');
    pdfDocumentContent.write(`
      /* Add your custom CSS styles here */
      body { background-color: #f2f2f2; }
      table { width: 100%; border-collapse: collapse; }
      th, td { border: 1px solid #dddddd; text-align: left; padding: 8px; }
      th { background-color: #000000; color: white; } /* Change header background color */
    `);
    pdfDocumentContent.write('</style>');
    pdfDocumentContent.write(`<h1>${customName}</h1>`);

    // Remove specified text content from table headers
    const cleanedTableHeader = tableHeader
        .replace(/↑/g, '') // Remove '↑'
        .replace(/Clan Score >200/g, '') // Remove "Clan Score >200"
        .replace(/Clan Score = War Attack \+ Clan Capital \+ Clan Games \* \(if Clan Games Maxed = 0 return 1 else return Clan Games Maxed\)/g, '') // Remove explanation
        .replace(/\n/g, ''); // Remove line breaks

    // Write cleaned table header and styles to PDF content
    pdfDocumentContent.write('<table style="border-collapse: collapse; width: 100%;">');
    pdfDocumentContent.write(cleanedTableHeader);

    // Convert filtered table rows HTML to PDF content
    const filteredTableRowsHTML = tableRows.map(row => row.outerHTML).join('');
    pdfDocumentContent.write(filteredTableRowsHTML);

    // Close the table tag
    pdfDocumentContent.write('</table>');

    // Close the PDF document
    pdfDocumentContent.write('</body></html>');
    pdfDocumentContent.close();

    // Print the PDF
    pdfWindow.print();

    // Remove the PDF iframe from the DOM after printing
    setTimeout(() => {
        document.body.removeChild(pdfDocument);
    }, 1000); // Adjust the delay as needed
}

// Add event listener to export PDF for "main-member-table"
document.getElementById('toPDFMainMemberTable').addEventListener('click', function() {
    exportTableToPDF('main-table');
});

// Add event listener to export PDF for "main-not-member-table"
document.getElementById('toPDFNotMemberTable').addEventListener('click', function() {
    exportTableToPDF('main-not-member-table');
});

// Add event listener to export PDF for "score-table"
document.getElementById('toPDFClanScore').addEventListener('click', function() {
    exportTableToPDF('score-table');
});

//Converting HTML table to JSON
// Function to convert table data to formatted JSON
function tableToJson(tableId) {
  let table = document.querySelector(tableId);
  let data = [];

  // Remove specified text content from table headers and format headers
  let headers = table.querySelectorAll('th');
  headers.forEach(function(header, index) {
    let headerText = header.textContent
      .replace('↑', '') // Remove '↑'
      .replace('Clan Score >200', '') // Remove "Clan Score >200"
      .replace('Clan Score = War Attack + Clan Capital + Clan Games * (if Clan Games Maxed = 0 return 1 else return Clan Games Maxed)', '') // Remove explanation
      .replace(/\n/g, '') // Remove line breaks
      .trim()
      .toLowerCase()
      .replace(/\s+/g, ''); // Remove spaces and convert to lowercase

    header.textContent = headerText; // Set the cleaned header text
  });

  // Iterate over each row in the table body
  for (let i = 1; i < table.rows.length; i++) { // Start from 1 to skip headers row
    let row = table.rows[i];
    let rowData = {};

    // Check if the row has null values, skip if any null value is found
    let hasNull = false;
    for (let j = 0; j < row.cells.length; j++) {
      let cell = row.cells[j];
      if (cell.textContent.trim() === '') {
        hasNull = true;
        break;
      }
    }
    if (hasNull) {
      continue;
    }

    // Iterate over each cell in the row
    for (let j = 0; j < row.cells.length; j++) {
      let cell = row.cells[j];
      let cellData = cell.textContent.trim();

      // Extract data from cells and add it to the rowData object
      rowData[headers[j].textContent] = cellData;
    }

    // Push rowData object to the data array
    data.push(rowData);
  }

  // Convert data array to formatted JSON format
  let jsonData = JSON.stringify(data, null, 4); // Use 4 spaces for indentation

  return jsonData;
}

// Function to trigger download of JSON file
function downloadJsonFile(jsonData, fileName) {
  let blob = new Blob([jsonData], { type: 'application/json' });
  let url = URL.createObjectURL(blob);
  let a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Event listener to trigger conversion and download for each table
document.querySelector('#toJSONMainMemberTable').addEventListener('click', function() {
    let jsonData = tableToJson('.main-table table');
    downloadJsonFile(jsonData, 'clan_members_table_data.json');
});

document.querySelector('#toJSONNotMemberTable').addEventListener('click', function() {
    let jsonData = tableToJson('.main-not-member-table table');
    downloadJsonFile(jsonData, 'former_clan_members_table_data.json');
});

document.querySelector('#toJSONClanScore').addEventListener('click', function() {
    let jsonData = tableToJson('.score-table table');
    downloadJsonFile(jsonData, 'top_clan_contributors_data.json');
});

//Converting HTML table to CSV File
// Function to convert table data to CSV format
function tableToCsv(tableId) {
    let table = document.querySelector(tableId);
    let csv = [];

    // Remove specified text content from table headers and format headers
    let headers = Array.from(table.querySelectorAll('th')).map(function(header) {
        let cleanedHeader = header.textContent.trim()
            .replace('↑', '') // Remove '↑'
            .replace('Clan Score >200', '') // Remove "Clan Score >200"
            .replace('Clan Score = War Attack + Clan Capital + Clan Games * (if Clan Games Maxed = 0 return 1 else return Clan Games Maxed)', '') // Remove explanation
            .replace(/\n/g, '') // Remove line breaks
            .toLowerCase()
            .replace(/\s+/g, ''); // Remove spaces and convert to lowercase
        return cleanedHeader;
    });
    csv.push(headers.join(','));

    // Add rows to CSV array
    let rows = Array.from(table.querySelectorAll('tbody tr')).map(function(row) {
        return Array.from(row.querySelectorAll('td')).map(function(cell) {
            return cell.textContent.trim();
        }).join(',');
    });
    csv.push(rows.join('\n'));

    return csv.join('\n');
}

// Function to trigger download of CSV file
function downloadCsvFile(csvData, fileName) {
    let blob = new Blob([csvData], { type: 'text/csv' });
    let url = URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Event listener to trigger conversion and download for each CSV label
document.querySelector('#toCSVMainMemberTable').addEventListener('click', function() {
    let csvData = tableToCsv('.main-table table');
    downloadCsvFile(csvData, 'clan_members_table_data.csv');
});

document.querySelector('#toCSVNotMemberTable').addEventListener('click', function() {
    let csvData = tableToCsv('.main-not-member-table table');
    downloadCsvFile(csvData, 'former_clan_members_table_data.csv');
});

document.querySelector('#toCSVClanScore').addEventListener('click', function() {
    let csvData = tableToCsv('.score-table table');
    downloadCsvFile(csvData, 'top_clan_contributors_data.csv');
});

//Converting HTML table to EXCEL File
// Function to include SheetJS library dynamically
function includeSheetJSLibrary() {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.4/xlsx.full.min.js';
    script.onload = function() {
        // SheetJS library has been loaded
        //console.log('SheetJS library has been loaded.');
        // Now you can use SheetJS functions
        setupTableToExcelConversion(); // Call the function to set up table-to-Excel conversion
    };
    document.head.appendChild(script);
}

// Function to convert HTML table to Excel file (XLSX format) using SheetJS
function convertTableToExcel(table) {
    // Remove specified text content from table headers
    const headers = table.querySelectorAll('th');
    headers.forEach(function(header) {
        header.textContent = header.textContent
            .replace('↑', '')
            .replace('Clan Score >200', '')
            .replace('Clan Score = War Attack + Clan Capital + Clan Games * (if Clan Games Maxed = 0 return 1 else return Clan Games Maxed)', '')
            .replace(/\n/g, '');
    });

    // Create a new workbook
    const workbook = XLSX.utils.book_new();

    // Add a worksheet
    const worksheet = XLSX.utils.table_to_sheet(table);

    // Add the worksheet to the workbook
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

    // Convert the workbook to an Excel file (XLSX format)
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });

    // Convert the array buffer to a Blob
    const excelBlob = new Blob([excelBuffer], { type: 'application/octet-stream' });

    return excelBlob;
}

// Function to trigger download of Excel file
function downloadExcel(excelBlob, fileName) {
    const url = window.URL.createObjectURL(excelBlob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

// Function to set up table-to-Excel conversion
function setupTableToExcelConversion() {
    // Event listener to trigger conversion and download
    document.querySelector('#toEXCELMainMemberTable').addEventListener('click', function() {
        const excelBlob = convertTableToExcel(document.querySelector('.main-table table'));
        downloadExcel(excelBlob, 'clan_members_data.xlsx');
    });

    document.querySelector('#toEXCELNotMemberTable').addEventListener('click', function() {
        const excelBlob = convertTableToExcel(document.querySelector('.main-not-member-table table'));
        downloadExcel(excelBlob, 'former_clan_members_data.xlsx');
    });

    document.querySelector('#toEXCELClanScore').addEventListener('click', function() {
        const excelBlob = convertTableToExcel(document.querySelector('.score-table table'));
        downloadExcel(excelBlob, 'top_clan_contributors_data.xlsx');
    });
}

// Call the function to include SheetJS library
includeSheetJSLibrary();
