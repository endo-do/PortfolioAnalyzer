
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const regionFilter = document.getElementById("regionFilter");
  const table = document.getElementById("exchangeTable");
  const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
  const noExchangeRow = document.getElementById("noExchangeFoundRow");

  function filterTable() {
    const searchText = searchInput.value.toLowerCase();
    const selectedRegion = regionFilter.value.toLowerCase();
    let visibleCount = 0;

    for (let row of rows) {
      if (row.id === "noExchangeFoundRow") continue; // skip placeholder row

      const symbol = row.cells[0].textContent.toLowerCase();
      const region = row.cells[1].textContent.toLowerCase();

      const matchesSearch = symbol.includes(searchText);
      const matchesRegion = !selectedRegion || region === selectedRegion;

      if (matchesSearch && matchesRegion) {
        row.style.display = "";
        visibleCount++;
      } else {
        row.style.display = "none";
      }
    }

    noExchangeRow.style.display = visibleCount === 0 ? "" : "none";
  }

  searchInput.addEventListener("input", filterTable);
  regionFilter.addEventListener("change", filterTable);
});