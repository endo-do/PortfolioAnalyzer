document.getElementById('searchInput').addEventListener('input', function() {
  const filter = this.value.toLowerCase();
  const rows = document.querySelectorAll('#userTable tbody tr:not(#noUserFoundRow)');
  let visibleCount = 0;

  rows.forEach(row => {
    const username = row.querySelector('.name-cell').textContent.toLowerCase();
    if (username.includes(filter)) {
      row.style.display = '';
      visibleCount++;
    } else {
      row.style.display = 'none';
    }
  });

  const noUserRow = document.getElementById('noUserFoundRow');
  noUserRow.style.display = visibleCount === 0 ? '' : 'none';
});

document.addEventListener('DOMContentLoaded', () => {
  const adminFilter = document.getElementById('adminFilter');
  const sortBtn = document.getElementById('sortBtn');
  const table = document.getElementById('userTable').getElementsByTagName('tbody')[0];

  let sortAsc = true; // current sort order

  // Filter rows by admin status
  function filterRows() {
    const filter = adminFilter.value;
    const rows = table.rows;
    for (let row of rows) {
      const isAdminText = row.cells[1].textContent.trim(); // 'Yes' or 'No'

      if (
        filter === 'all' ||
        (filter === 'admin' && isAdminText === 'Yes') ||
        (filter === 'nonadmin' && isAdminText === 'No')
      ) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  }

  // Sort rows by name (cell 0)
  function sortRows() {
    const rows = Array.from(table.rows).filter(row => row.style.display !== 'none');
    rows.sort((a, b) => {
      const nameA = a.cells[0].textContent.trim().toLowerCase();
      const nameB = b.cells[0].textContent.trim().toLowerCase();

      if (nameA < nameB) return sortAsc ? -1 : 1;
      if (nameA > nameB) return sortAsc ? 1 : -1;
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
  adminFilter.addEventListener('change', updateTable);

  sortBtn.addEventListener('click', () => {
    sortAsc = !sortAsc;
    sortBtn.textContent = `Sort: Name ${sortAsc ? '↑' : '↓'}`;
    sortRows();
  });

  // Initial table update on load
  updateTable();
});