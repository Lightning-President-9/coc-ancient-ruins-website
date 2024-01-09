
  // Check if the visitor count is stored in local storage
  let visitorCount = localStorage.getItem('visitorCount');

  // If not, initialize the count to 0
  if (visitorCount === null) {
    visitorCount = 0;
  } else {
    // If yes, parse the count as an integer
    visitorCount = parseInt(visitorCount);
  }

  // Increment the visitor count
  visitorCount++;

  // Update the local storage and display the count
  localStorage.setItem('visitorCount', visitorCount);
  document.getElementById('visitor-count').textContent = `Total Visitors: ${visitorCount}`;
console.log("Visitor Count:"+visitorCount);



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

