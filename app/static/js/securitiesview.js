document.addEventListener('DOMContentLoaded', () => {
  
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortBySelect = document.getElementById('sortBySelect');
  const sortOrderRadios = document.querySelectorAll('input[name="sortOrder"]');
  const table = document.getElementById('bondsTable2');
  const tbody = table.querySelector('tbody');

  // Save original rows to preserve unfiltered data
  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  function normalize(str) {
    return str.toLowerCase().trim();
  }

  function getConvertedValue(row) {
    const exchangeRate = parseFloat(row.dataset.exchangeRate) || 1.0;
    const originalValue = parseFloat(row.dataset.originalValue) || 0;
    return originalValue * exchangeRate;
  }

  function getSortOrder() {
    const checkedRadio = document.querySelector('input[name="sortOrder"]:checked');
    return checkedRadio ? checkedRadio.value : 'asc';
  }

  function filterRows() {
    const searchText = normalize(searchInput.value);
    const category = categoryFilter.value;

    originalRows.forEach(row => {
      const symbol = normalize(row.cells[0].textContent);
      const name = normalize(row.cells[1].textContent);
      const cat = normalize(row.cells[2].textContent);
      
      const matchesSearch = symbol.includes(searchText) || name.includes(searchText);
      const matchesCategory = category === 'All' || cat === normalize(category);
      
      row.style.display = (matchesSearch && matchesCategory) ? '' : 'none';
    });
  }

  function sortRows() {
    const sortBy = sortBySelect.value;
    const sortOrder = getSortOrder();
    const visibleRows = originalRows.filter(row => row.style.display !== 'none');

    visibleRows.sort((a, b) => {
      let comparison = 0;
      
      if (sortBy === 'name') {
        const nameA = a.cells[1].textContent.toLowerCase();
        const nameB = b.cells[1].textContent.toLowerCase();
        if (nameA < nameB) comparison = -1;
        if (nameA > nameB) comparison = 1;
      } else if (sortBy === 'amount') {
        const amtA = parseFloat(a.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        const amtB = parseFloat(b.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        comparison = amtA - amtB;
      } else if (sortBy === 'value') {
        const valA = getConvertedValue(a);
        const valB = getConvertedValue(b);
        comparison = valA - valB;
      }
      
      return sortOrder === 'asc' ? comparison : -comparison;
    });

    // Reorder visible rows in the table
    visibleRows.forEach(row => {
      tbody.appendChild(row);
    });
  }

  function updateTable() {
    filterRows();
    sortRows();
    
    // Show/hide no results message
    const visibleRows = originalRows.filter(row => row.style.display !== 'none');
    let noResultsRow = tbody.querySelector('.no-results-row');
    
    if (visibleRows.length === 0) {
      if (!noResultsRow) {
        noResultsRow = document.createElement('tr');
        noResultsRow.className = 'no-results-row';
        const noCell = document.createElement('td');
        noCell.colSpan = 6;
        noCell.innerHTML = '<div class="text-center text-muted py-4"><i class="fas fa-search me-2"></i>No securities found matching your criteria</div>';
        noCell.classList.add('text-center', 'text-muted');
        noResultsRow.appendChild(noCell);
        tbody.appendChild(noResultsRow);
      }
    } else if (noResultsRow) {
      noResultsRow.remove();
    }
  }

  // Event listeners
  searchInput.addEventListener('input', updateTable);
  categoryFilter.addEventListener('change', updateTable);
  sortBySelect.addEventListener('change', updateTable);
  sortOrderRadios.forEach(radio => {
    radio.addEventListener('change', updateTable);
  });

  // Initial call
  updateTable();
});