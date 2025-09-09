document.addEventListener('DOMContentLoaded', () => {
  
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortSelect = document.getElementById('sortSelect');
  const baseCurrencySelect = document.getElementById('baseCurrencySelect');
  const table = document.getElementById('bondsTable2');
  const tbody = table.querySelector('tbody');

  // Save original rows to preserve unfiltered data
  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  function normalize(str) {
    return str.toLowerCase();
  }

  function getConvertedValue(row) {
    const exchangeRate = parseFloat(row.dataset.exchangeRate) || 1.0;
    const originalValue = parseFloat(row.dataset.originalValue) || 0;
    return originalValue * exchangeRate;
  }

  function filterAndSort() {
    const searchText = normalize(searchInput.value.trim());
    const category = categoryFilter.value;
    const sortValue = sortSelect.value;

    // Copy original rows
    let rows = originalRows.slice();

    // Filter rows by search and category
    rows = rows.filter(row => {
      const symbol = normalize(row.cells[0].textContent);
      const name = normalize(row.cells[1].textContent);
      const cat = normalize(row.cells[2].textContent);
      const matchesSearch = symbol.includes(searchText) || name.includes(searchText);
      const matchesCategory = category === 'All' || cat === normalize(category);
      return matchesSearch && matchesCategory;
    });

    // Sort rows
    rows.sort((a, b) => {
      if (sortValue.startsWith('value')) {
        // Use converted values for proper currency comparison
        const valA = getConvertedValue(a);
        const valB = getConvertedValue(b);
        return sortValue.endsWith('asc') ? valA - valB : valB - valA;
      } else if (sortValue.startsWith('amount')) {
        // Amount is in column 3
        const amtA = parseFloat(a.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        const amtB = parseFloat(b.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        return sortValue.endsWith('asc') ? amtA - amtB : amtB - amtA;
      } else if (sortValue.startsWith('symbol')) {
        const symA = a.cells[0].textContent.toLowerCase();
        const symB = b.cells[0].textContent.toLowerCase();
        if (symA < symB) return sortValue.endsWith('asc') ? -1 : 1;
        if (symA > symB) return sortValue.endsWith('asc') ? 1 : -1;
        return 0;
      }
      return 0;
    });

    // Clear tbody and re-append sorted and filtered rows
    tbody.innerHTML = '';

    if (rows.length === 0) {
      const noRow = document.createElement('tr');
      const noCell = document.createElement('td');
      noCell.colSpan = 6; // number of columns
      noCell.textContent = 'No bonds found';
      noCell.classList.add('text-center', 'text-muted');
      noRow.appendChild(noCell);
      tbody.appendChild(noRow);
    } else {
      rows.forEach(row => tbody.appendChild(row));
    }
  }

  function changeBaseCurrency() {
    const newBaseCurrency = baseCurrencySelect.value;
    const currentUrl = new URL(window.location);
    currentUrl.searchParams.set('base_currency', newBaseCurrency);
    window.location.href = currentUrl.toString();
  }

  // Event listeners
  searchInput.addEventListener('input', filterAndSort);
  categoryFilter.addEventListener('change', filterAndSort);
  sortSelect.addEventListener('change', filterAndSort);
  baseCurrencySelect.addEventListener('change', changeBaseCurrency);

  // Initial call
  filterAndSort();
});