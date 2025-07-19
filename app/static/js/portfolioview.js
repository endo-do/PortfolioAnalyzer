document.addEventListener("DOMContentLoaded", function () {
  const json = JSON.parse(document.getElementById("portfolio-data").textContent);
  renderAssetBreakdownChart(json.categories, json.portfolio);
});

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortSelect = document.getElementById('sortSelect');
  const table = document.getElementById('bondsTable2');
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
      const cat = normalize(row.cells[2].textContent);
      const matchesSearch = symbol.includes(searchText) || name.includes(searchText);
      const matchesCategory = category === 'All' || cat === normalize(category);
      return matchesSearch && matchesCategory;
    });

    // Sort rows
    rows.sort((a, b) => {
      if (sortValue.startsWith('value')) {
        // Total Value is in column 4
        const valA = parseFloat(a.cells[4].textContent.replace(/[^\d.-]/g, '')) || 0;
        const valB = parseFloat(b.cells[4].textContent.replace(/[^\d.-]/g, '')) || 0;
        return sortValue.endsWith('asc') ? valA - valB : valB - valA;
      } else if (sortValue.startsWith('amount')) {
        // Amount is in column 3
        const amtA = parseFloat(a.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        const amtB = parseFloat(b.cells[3].textContent.replace(/[^\d.-]/g, '')) || 0;
        return sortValue.endsWith('asc') ? amtA - amtB : amtB - amtA;
      } else if (sortValue.startsWith('symbol')) {
        const symA = a.cells[0].textContent.toLowerCase();
        const symB = b.cells[0].textContent.toLowerCase();
        if (symA < symB) return sortValue.endsWith('asc') ? -1 : 1;
        if (symA > symB) return sortValue.endsWith('asc') ? 1 : -1;
        return 0;
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

function renderAssetBreakdownChart(categories, portfolio) {
  const ctx = document.getElementById("assetBreakdownChart").getContext("2d");
  const currency = portfolio.currencycode || "";

  const labels = categories.map(c => c.bondcategoryname);
  const data = labels.map(label => {
    const key = label.toLowerCase() + "_value";
    return portfolio[key] || 0;
  });
  const percentages = labels.map(label => {
    const key = label.toLowerCase() + "_percent";
    return Number(portfolio[key]) || 0;
  });

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const value = context.raw || 0;
              const percent = percentages[context.dataIndex] || 0;
              return `  ${percent.toFixed(1)}%: ${currency} ${value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
              })}`;
            }
          }
        },
        datalabels: {
          formatter: function (value, context) {
            const percent = percentages[context.dataIndex];
            return percent >= 10 ? percent.toFixed(1) + "%" : "";
          },
          color: '#fff',
          font: {
            weight: 'bold',
            size: 14
          }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
}

function hexToRgba(hex, alpha) {
  hex = hex.replace('#', '');
  const bigint = parseInt(hex, 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function applyColors(rows) {
  rows.forEach(row => {
    const c = row.dataset.color || '#6c757d';
    const bg = hexToRgba(c, 0.4);
    row.querySelectorAll('td').forEach(cell => {
      cell.style.setProperty('background-color', bg, 'important');
      cell.style.setProperty('color', 'black', 'important');
    });
  });
}

// Usage example:
const backgroundColors = [
  '#007bff', // blue
  '#28a745', // green
  '#ffc107', // yellow
  '#dc3545', // red
  '#6c757d' // gray
];

const table = document.getElementById('assetBreakdownTable');
if (table) {
  const rows = table.querySelectorAll('tbody tr');
  rows.forEach((row, index) => {
    row.dataset.color = backgroundColors[index % backgroundColors.length];
  });
  applyColors(rows);
}