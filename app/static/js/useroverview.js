document.querySelectorAll('[id^="editUserModal"]').forEach(modalEl => {
  modalEl.addEventListener('hidden.bs.modal', () => {
    const form = modalEl.querySelector('form');
    if (form) form.reset();
  });
});

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