document.addEventListener('DOMContentLoaded', function () {
  // Delete confirmation
  document.querySelectorAll('.delete-bond-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to delete this bond from the portfolio?')) {
        e.preventDefault();
      }
    });
  });

  // Unsaved changes detection
  const form = document.getElementById('editSecuritiesForm');
  if (form) {
    let isDirty = false;
    form.querySelectorAll('input').forEach(input => {
      input.addEventListener('input', () => isDirty = true);
    });
    form.addEventListener('submit', () => isDirty = false);
    window.addEventListener('beforeunload', function (e) {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = '';
      }
    });
  }

document.getElementById('cancelChangesBtn').addEventListener('click', () => {
  const form = document.getElementById('editSecuritiesForm');
  if (form) {
    form.reset();       // Setzt alle Eingaben auf den ursprünglichen Wert zurück
  }
});

  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const ownershipFilter = document.getElementById('ownershipFilter');
  const sortSelect = document.getElementById('sortSelect');
  const table = document.getElementById('bondsTable1'); // Updated to match the new table ID
  const tbody = table.querySelector('tbody');
  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  console.log('Original rows:', originalRows.length);

  function normalize(str) {
    return str.trim().toLowerCase();
  }

  function getQuantityFromRow(row) {
    const input = row.cells[3].querySelector('input');
    return input ? parseInt(input.value) || 0 : 0;
  }

  function matchesFilters(row, searchText, category, ownership) {
    const symbol = normalize(row.cells[0].textContent);
    const name = normalize(row.cells[1].textContent);
    const cat = row.cells[2].textContent;
    const quantity = getQuantityFromRow(row);

    const matchSearch = symbol.includes(searchText) || name.includes(searchText);
    const matchCategory = category === 'All' || cat === category;
    const matchOwnership =
      ownership === 'All' ||
      (ownership === 'Only Owned' && quantity > 0) ||
      (ownership === 'Not Owned' && quantity === 0);

    return matchSearch && matchCategory && matchOwnership;
  }

  function sortRows(rows, sortValue) {
    return rows.sort((a, b) => {
      if (sortValue.startsWith('quantity')) {
        const qA = getQuantityFromRow(a);
        const qB = getQuantityFromRow(b);
        return sortValue.endsWith('asc') ? qA - qB : qB - qA;
      }
      if (sortValue.startsWith('symbol')) {
        const sA = normalize(a.cells[0].textContent);
        const sB = normalize(b.cells[0].textContent);
        return sortValue.endsWith('asc') ? sA.localeCompare(sB) : sB.localeCompare(sA);
      }
      if (sortValue.startsWith('name')) {
        const nA = normalize(a.cells[1].textContent);
        const nB = normalize(b.cells[1].textContent);
        return sortValue.endsWith('asc') ? nA.localeCompare(nB) : nB.localeCompare(nA);
      }
      return 0;
    });
  }

  function filterAndSort() {
    const searchText = normalize(searchInput.value);
    const category = categoryFilter.value;
    const ownership = ownershipFilter ? ownershipFilter.value : 'All';
    const sortValue = sortSelect.value;

    let rows = originalRows.filter(row =>
      matchesFilters(row, searchText, category, ownership)
    );

    rows = sortRows(rows, sortValue);
    tbody.innerHTML = '';

    if (rows.length === 0) {
      const emptyRow = document.createElement('tr');
      const emptyCell = document.createElement('td');
      emptyCell.colSpan = 5;
      emptyCell.textContent = 'No bonds found';
      emptyCell.classList.add('text-center', 'text-muted');
      emptyRow.appendChild(emptyCell);
      tbody.appendChild(emptyRow);
    } else {
      rows.forEach(row => tbody.appendChild(row));
    }
  }

  searchInput.addEventListener('input', filterAndSort);
  categoryFilter.addEventListener('change', filterAndSort);
  sortSelect.addEventListener('change', filterAndSort);
  if (ownershipFilter) ownershipFilter.addEventListener('change', filterAndSort);

  filterAndSort();
});

document.querySelectorAll('.add-to-portfolio-btn').forEach(button => {
  button.addEventListener('click', () => {
    const bondId = button.getAttribute('data-bondid');
    const bondSymbol = button.getAttribute('data-bondsymbol');
    
    // Setze bond id im versteckten Input des Modals
    document.getElementById('modalBondId').value = bondId;
    
    // Optional: Modal Titel anpassen, damit man sieht, was man hinzufügt
    document.getElementById('addBondModalLabel').textContent = `Add "${bondSymbol}" to Portfolio`;
    
    // Modal öffnen (Bootstrap 5)
    const modal = new bootstrap.Modal(document.getElementById('addBondModal'));
    modal.show();
  });
});