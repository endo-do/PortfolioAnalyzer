
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const regionFilter = document.getElementById("regionFilter");
  const sortBtn = document.getElementById("sortBtn");
  const table = document.getElementById("exchangeTable").getElementsByTagName("tbody")[0];
  const noExchangeRow = document.getElementById("noExchangeFoundRow");

  let sortAsc = true; // current sort order

  // Filter rows by search and region
  function filterRows() {
    const searchText = searchInput.value.toLowerCase();
    const selectedRegion = regionFilter.value.toLowerCase();
    const rows = table.rows;

    for (let row of rows) {
      if (row.id === "noExchangeFoundRow") continue; // skip placeholder row

      const symbol = row.cells[0].textContent.toLowerCase();
      const region = row.cells[1].textContent.toLowerCase();

      const matchesSearch = symbol.includes(searchText);
      const matchesRegion = !selectedRegion || region === selectedRegion;

      if (matchesSearch && matchesRegion) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    }
  }

  // Sort rows by exchange symbol (cell 0)
  function sortRows() {
    const rows = Array.from(table.rows).filter(row => row.style.display !== 'none' && row.id !== 'noExchangeFoundRow');
    rows.sort((a, b) => {
      const symbolA = a.cells[0].textContent.trim().toLowerCase();
      const symbolB = b.cells[0].textContent.trim().toLowerCase();

      if (symbolA < symbolB) return sortAsc ? -1 : 1;
      if (symbolA > symbolB) return sortAsc ? 1 : -1;
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
  searchInput.addEventListener("input", updateTable);
  regionFilter.addEventListener("change", updateTable);

  sortBtn.addEventListener('click', () => {
    sortAsc = !sortAsc;
    sortBtn.innerHTML = sortAsc ? '<i class="fas fa-sort-alpha-up me-2"></i>Name ↑' : '<i class="fas fa-sort-alpha-down me-2"></i>Name ↓';
    sortRows();
  });

  // Initial table update on load
  updateTable();
});
