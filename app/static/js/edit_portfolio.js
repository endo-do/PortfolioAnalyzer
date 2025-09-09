document.addEventListener("DOMContentLoaded", function () {
  const addButtons = document.querySelectorAll(".add-to-portfolio-btn");
  const addModal = new bootstrap.Modal(document.getElementById("addBondModal"));
  const modalBondIdInput = document.getElementById("modalBondId");
  const modalBondSymbol = document.getElementById("modalBondSymbol");
  const modalBondName = document.getElementById("modalBondName");

  addButtons.forEach(button => {
    button.addEventListener("click", function () {
      const bondId = this.getAttribute("data-bondid");
      const bondSymbol = this.getAttribute("data-bondsymbol");
      
      // Find the bond name from the table row
      const row = this.closest('tr');
      const bondName = row.querySelector('td:nth-child(2) .fw-medium').textContent;
      
      modalBondIdInput.value = bondId;
      modalBondSymbol.textContent = bondSymbol;
      modalBondName.textContent = bondName;
      addModal.show();
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const ownershipFilterGroup = document.getElementById('ownershipFilter');
  const categoryFilter = document.getElementById('categoryFilter');
  const regionFilter = document.getElementById('regionFilter');
  const sectorFilter = document.getElementById('sectorFilter');
  const sortBySelect = document.getElementById('sortBySelect');
  const sortOrderRadios = document.querySelectorAll('input[name="sortOrder"]');
  const table = document.getElementById('bondsTable1');
  const tbody = table.querySelector('tbody');

  // Save original rows to preserve unfiltered data
  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  function normalize(str) {
    return str.toLowerCase();
  }

  function getSortOrder() {
    const checkedRadio = document.querySelector('input[name="sortOrder"]:checked');
    return checkedRadio ? checkedRadio.value : 'asc';
  }

  function getSelectedOwnership() {
    const checkedRadio = ownershipFilterGroup.querySelector('input[name="ownershipToggle"]:checked');
    return checkedRadio ? checkedRadio.value : 'Only Owned';
  }

  function filterRows() {
    const searchText = normalize(searchInput.value.trim());
    const ownership = getSelectedOwnership();
    const category = categoryFilter.value;
    const region = regionFilter.value;
    const sector = sectorFilter.value;

    originalRows.forEach(row => {
      const symbol = normalize(row.cells[0].textContent);
      const name = normalize(row.cells[1].textContent);
      // Get category text from the badge span element
      const categoryElement = row.cells[2].querySelector('.badge');
      const cat = categoryElement ? normalize(categoryElement.textContent) : normalize(row.cells[2].textContent);
      const isOwned = row.dataset.owned === 'yes';
      
      const matchesSearch = symbol.includes(searchText) || name.includes(searchText);
      const matchesOwnership = (ownership === 'Only Owned' && isOwned) || (ownership === 'Not Owned' && !isOwned);
      const matchesCategory = category === 'All' || cat === normalize(category);
      const matchesRegion = region === 'All'; // Placeholder - region data not available in current structure
      const matchesSector = sector === 'All'; // Placeholder - sector data not available in current structure
      
      row.style.display = (matchesSearch && matchesOwnership && matchesCategory && matchesRegion && matchesSector) ? '' : 'none';
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
      } else if (sortBy === 'quantity') {
        const qtyA = parseFloat(a.cells[3].textContent) || 0;
        const qtyB = parseFloat(b.cells[3].textContent) || 0;
        comparison = qtyA - qtyB;
      } else if (sortBy === 'date') {
        // Placeholder for date sorting - would need date data
        comparison = 0;
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
        noCell.colSpan = 5;
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
  ownershipFilterGroup.querySelectorAll('input[name="ownershipToggle"]').forEach(radio => {
    radio.addEventListener('change', updateTable);
  });
  categoryFilter.addEventListener('change', updateTable);
  regionFilter.addEventListener('change', updateTable);
  sectorFilter.addEventListener('change', updateTable);
  sortBySelect.addEventListener('change', updateTable);
  sortOrderRadios.forEach(radio => {
    radio.addEventListener('change', updateTable);
  });

  // Initial call
  updateTable();
});