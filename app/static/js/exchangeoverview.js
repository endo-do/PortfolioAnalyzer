document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const table = document.getElementById("exchangeTable");
    const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    const noExchangeRow = document.getElementById("noExchangeFoundRow");

    searchInput.addEventListener("input", () => {
        const filter = searchInput.value.toLowerCase();
        let visibleCount = 0;

        for (let row of rows) {
            // Skip the "No exchanges found" row
            if (row.id === "noExchangeFoundRow") continue;

            const symbol = row.cells[0].textContent.toLowerCase();
            const region = row.cells[1].textContent.toLowerCase();

            if (symbol.includes(filter) || region.includes(filter)) {
                row.style.display = "";
                visibleCount++;
            } else {
                row.style.display = "none";
            }
        }

        // Show "No exchanges found" message if nothing matches
        noExchangeRow.style.display = visibleCount === 0 ? "" : "none";
    });
});
