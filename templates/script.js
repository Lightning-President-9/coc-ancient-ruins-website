
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
