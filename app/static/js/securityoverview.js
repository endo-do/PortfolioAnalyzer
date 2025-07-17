document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortSelect = document.getElementById('sortSelect');
  const table = document.getElementById('bondsTable3');
  const tbody = table.querySelector('tbody');

  // Save original rows to preserve unfiltered data
  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  function normalize(str) {
    return str.toLowerCase();
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
      const cat = row.cells[2].textContent;
      const matchesSearch = symbol.includes(searchText) || name.includes(searchText);
      const matchesCategory = category === 'All' || cat === category;
      return matchesSearch && matchesCategory;
    });

    // Sort rows
    rows.sort((a, b) => {
      if (sortValue.startsWith('value')) {
        const valA = parseFloat(a.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        const valB = parseFloat(b.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        return sortValue.endsWith('asc') ? valA - valB : valB - valA;
      } else if (sortValue.startsWith('symbol')) {
        const symA = a.cells[0].textContent.toLowerCase();
        const symB = b.cells[0].textContent.toLowerCase();
        if (symA < symB) return sortValue.endsWith('asc') ? -1 : 1;
        if (symA > symB) return sortValue.endsWith('asc') ? 1 : -1;
        return 0;
      } else if (sortValue.startsWith('date')) {
        const dateA = new Date(a.cells[4].textContent);
        const dateB = new Date(b.cells[4].textContent);
        return sortValue.endsWith('asc') ? dateA - dateB : dateB - dateA;
      }
      return 0;
    });

    // Clear tbody and re-append sorted and filtered rows
    tbody.innerHTML = '';

    if (rows.length === 0) {
      const noRow = document.createElement('tr');
      const noCell = document.createElement('td');
      noCell.colSpan = 5; // number of columns
      noCell.textContent = 'No bonds found';
      noCell.classList.add('text-center', 'text-muted');
      noRow.appendChild(noCell);
      tbody.appendChild(noRow);
    } else {
      rows.forEach(row => tbody.appendChild(row));
    }
  }

  // Event listeners
  searchInput.addEventListener('input', filterAndSort);
  categoryFilter.addEventListener('change', filterAndSort);
  sortSelect.addEventListener('change', filterAndSort);

  // Initial call
  filterAndSort();
});

const createSecurityModal = document.getElementById('createSecurityModal');
const createSecurityForm = document.getElementById('createSecurityForm');

createSecurityModal.addEventListener('hidden.bs.modal', () => {
  createSecurityForm.reset();
});

document.addEventListener('DOMContentLoaded', () => {
  const quickFillBtn = document.getElementById('quickFillBtn');
  if (!quickFillBtn) {
    console.error('quickFillBtn not found in DOM');
    return;
  }

  quickFillBtn.addEventListener('click', async () => {
    const symbolInput = document.getElementById('tickerSymbol');
    if (!symbolInput) {
      alert('Ticker symbol input not found.');
      return;
    }

    const symbol = symbolInput.value.trim();
    if (!symbol) {
      alert('Please enter a ticker symbol first.');
      return;
    }

    try {
      const response = await fetch(`/api/securityinfo/${encodeURIComponent(symbol)}`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });

      if (!response.ok) {
        throw new Error('Security info not found or API error');
      }

      const data = await response.json();

      // Felder befüllen:
      document.getElementById('name').value = data.name || '';
      document.getElementById('country').value = data.country || '';
      document.getElementById('website').value = data.website || '';
      document.getElementById('industry').value = data.industry || '';
      document.getElementById('sector').value = data.sector || '';
      document.getElementById('description').value = data.description || '';

      const categorySelect = document.getElementById('category');
      console.log('categorySelect:', categorySelect);
      console.log('data.category:', data.category);

      if (categorySelect && data.category) {
        const categoryToMatch = data.category.trim().toLowerCase();
        let foundCat = false;

        for (const option of categorySelect.options) {
          const optionText = option.text.trim().toLowerCase();
          console.log(`Comparing option "${optionText}" with "${categoryToMatch}"`);
          if (optionText === categoryToMatch) {
            categorySelect.value = option.value;
            foundCat = true;
            console.log('✅ Match found:', option.value);
            break;
          }
        }

        if (!foundCat) {
          categorySelect.selectedIndex = 0;
          console.warn('⚠️ No matching category found. Set to default (index 0).');
        }
      } else {
        console.error('❌ categorySelect or data.category is missing.');
      }

      // Currency
      if (data.currency) {
        const currencySelect = document.getElementById('currency');
        console.log('currencySelect:', currencySelect);
        console.log('data.currency:', data.currency);

        let foundCurr = false;
        const currencyToMatch = data.currency.trim().toUpperCase();

        for (const option of currencySelect.options) {
          const optionText = option.text.trim().toUpperCase();
          console.log(`Comparing option "${optionText}" with "${currencyToMatch}"`);
          if (optionText === currencyToMatch) {
            currencySelect.value = option.value;
            foundCurr = true;
            console.log('✅ Currency match found:', option.value);
            break;
          }
        }

        if (!foundCurr) {
          currencySelect.selectedIndex = 0;
          console.warn('⚠️ No matching currency found. Set to default (index 0).');
        }
      } else {
        console.error('❌ data.currency is missing.');
      }

      // Optional: Set the ticker symbol if not already set
      if (!symbolInput.value) {
        symbolInput.value = data.symbol || '';
      }

    } catch (error) {
      alert('Error fetching security info: ' + error.message);
    }
  });
});