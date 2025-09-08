document.addEventListener("DOMContentLoaded", function () {
  const addButtons = document.querySelectorAll(".add-to-portfolio-btn");
  const addModal = new bootstrap.Modal(document.getElementById("addBondModal"));
  const modalBondIdInput = document.getElementById("modalBondId");

  addButtons.forEach(button => {
    button.addEventListener("click", function () {
      const bondId = this.getAttribute("data-bondid");
      modalBondIdInput.value = bondId;
      addModal.show();
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  // Remove direct getElementById for ownershipFilter
  const ownershipFilterGroup = document.getElementById('ownershipFilter');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortSelect = document.getElementById('sortSelect');
  const searchInput = document.getElementById('searchInput');
  const table = document.getElementById('bondsTable1');
  const tbody = table.querySelector('tbody');

  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  function normalize(str) {
    return str.toLowerCase();
  }

  function getSelectedOwnership() {
    // Get the checked radio button value inside ownershipFilter group
    const checkedRadio = ownershipFilterGroup.querySelector('input[name="ownershipToggle"]:checked');
    return checkedRadio ? checkedRadio.value : 'Only Owned'; // fallback to 'Only Owned'
  }

  function filterAndSort() {
    const ownership = getSelectedOwnership();
    const category = categoryFilter.value;
    const sortValue = sortSelect.value;
    const searchTerm = normalize(searchInput.value);

    let rows = originalRows.slice();

    rows = rows.filter(row => {
      const rowCategory = normalize(row.dataset.category || '');
      const isOwned = row.dataset.owned === 'yes';
      const rowSymbol = normalize(row.dataset.symbol || '');
      const rowName = normalize(row.dataset.name || '');

      const ownershipMatch =
        ownership === 'All' || // If you want to keep this option, otherwise remove it from toggle
        (ownership === 'Only Owned' && isOwned) ||
        (ownership === 'Not Owned' && !isOwned);

      const categoryMatch = category === 'All' || rowCategory === normalize(category);

      const searchMatch = searchTerm === '' || 
        rowSymbol.includes(searchTerm) || 
        rowName.includes(searchTerm);

      return ownershipMatch && categoryMatch && searchMatch;
    });

    rows.sort((a, b) => {
      const [key, direction] = sortValue.split('-');

      let aVal, bVal;

      if (key === 'quantity') {
        aVal = parseFloat(a.cells[3].textContent) || 0;
        bVal = parseFloat(b.cells[3].textContent) || 0;
      } else if (key === 'symbol') {
        aVal = a.cells[0].textContent.toLowerCase();
        bVal = b.cells[0].textContent.toLowerCase();
      }

      if (typeof aVal === 'string') {
        return direction === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
      } else {
        return direction === 'asc' ? aVal - bVal : bVal - aVal;
      }
    });

    // Update the table body
    tbody.innerHTML = '';

    if (rows.length === 0) {
      const noRow = document.createElement('tr');
      const noCell = document.createElement('td');
      noCell.colSpan = 5;
      noCell.textContent = 'No bonds found';
      noCell.classList.add('text-center', 'text-muted');
      noRow.appendChild(noCell);
      tbody.appendChild(noRow);
    } else {
      rows.forEach(row => tbody.appendChild(row));
    }
  }

  // Attach event listeners
  ownershipFilterGroup.querySelectorAll('input[name="ownershipToggle"]').forEach(radio => {
    radio.addEventListener('change', filterAndSort);
  });
  categoryFilter.addEventListener('change', filterAndSort);
  sortSelect.addEventListener('change', filterAndSort);
  searchInput.addEventListener('input', filterAndSort);

  // Initial load
  filterAndSort();
});