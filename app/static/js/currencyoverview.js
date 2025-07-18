var createCurrencyModal = document.getElementById('createCurrencyModal')

createCurrencyModal.addEventListener('hidden.bs.modal', function () {
// Formular zurücksetzen
this.querySelector('form').reset()
})

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('currencySearch');
  const sortSelect = document.getElementById('currencySort');
  const tableBody = document.querySelector('#currencyTable tbody');

  // Helper to get rows as array
  const getRows = () => Array.from(tableBody.querySelectorAll('tr'));

  // Filter rows based on search input
  function filterRows() {
    const search = searchInput.value.trim().toLowerCase();
    getRows().forEach(row => {
      const name = row.cells[0].textContent.toLowerCase();
      const symbol = row.cells[1].textContent.toLowerCase();
      if (name.includes(search) || symbol.includes(search)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }

  // Sort rows based on selected option
  function sortRows() {
    const [field, direction] = sortSelect.value.split('-'); // e.g. name-asc
    const rows = getRows();

    rows.sort((a, b) => {
      let valA = '';
      let valB = '';
      if (field === 'name') {
        valA = a.cells[0].textContent.toLowerCase();
        valB = b.cells[0].textContent.toLowerCase();
      } else if (field === 'symbol') {
        valA = a.cells[1].textContent.toLowerCase();
        valB = b.cells[1].textContent.toLowerCase();
      }

      if (valA < valB) return direction === 'asc' ? -1 : 1;
      if (valA > valB) return direction === 'asc' ? 1 : -1;
      return 0;
    });

    // Append sorted rows back to tbody
    rows.forEach(row => tableBody.appendChild(row));
  }

  // Event listeners
  searchInput.addEventListener('input', () => {
    filterRows();
  });

  sortSelect.addEventListener('change', () => {
    sortRows();
  });

  // Initial sort and filter on load
  sortRows();
  filterRows();
});