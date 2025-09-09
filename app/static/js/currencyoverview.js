document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('currencySearch');
  const sortBtn = document.getElementById('sortBtn');
  const table = document.getElementById('currencyTable').getElementsByTagName('tbody')[0];

  let sortAsc = true; // current sort order

  // Filter rows by search
  function filterRows() {
    const search = searchInput.value.trim().toLowerCase();
    const rows = table.rows;
    
    for (let row of rows) {
      if (row.id === 'noCurrencyFoundRow') continue; // Skip the "no results" row
      
      const name = row.cells[0].textContent.toLowerCase();
      const symbol = row.cells[1].textContent.toLowerCase();
      
      if (name.includes(search) || symbol.includes(search)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  }

  // Sort rows by name (cell 0)
  function sortRows() {
    const rows = Array.from(table.rows).filter(row => row.style.display !== 'none' && row.id !== 'noCurrencyFoundRow');
    rows.sort((a, b) => {
      const nameA = a.cells[0].textContent.trim().toLowerCase();
      const nameB = b.cells[0].textContent.trim().toLowerCase();

      if (nameA < nameB) return sortAsc ? -1 : 1;
      if (nameA > nameB) return sortAsc ? 1 : -1;
      return 0;
    });

    // Append sorted rows back to table body
    rows.forEach(row => table.appendChild(row));
  }

  // Combined update function
  function updateTable() {
    filterRows();
    sortRows();
  }

  // Event listeners
  searchInput.addEventListener('input', updateTable);

  sortBtn.addEventListener('click', () => {
    sortAsc = !sortAsc;
    sortBtn.innerHTML = sortAsc ? '<i class="fas fa-sort-alpha-up me-2"></i>Name ↑' : '<i class="fas fa-sort-alpha-down me-2"></i>Name ↓';
    sortRows();
  });

  // Initial table update on load
  updateTable();
});