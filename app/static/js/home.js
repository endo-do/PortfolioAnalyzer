// Pie chart
function renderPieChart(portfolios) {
  const currency = portfolios.length ? portfolios[0].currencycode : "";

  let sorted = portfolios.slice().sort((a, b) => b.total_value - a.total_value);
  let labels = [];
  let data = [];
  let percentages = [];
  let othersValue = 0;
  let othersPercent = 0;

  sorted.forEach((p, i) => {
    if (i < 4) {
      labels.push(p.portfolioname);
      data.push(p.total_value);
      percentages.push(Number(p.percentage));
    } else {
      othersValue += p.total_value;
      othersPercent += Number(p.percentage);
    }
  });

  if (sorted.length >= 5) {
    labels.push("Other");
    data.push(othersValue);
    percentages.push(othersPercent);
  }

  const chartColors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d'];
  const ctx = document.getElementById("portfolioPieChart").getContext("2d");

  // Destroy previous chart if exists
  if (window.portfolioChart) window.portfolioChart.destroy();

  // Create chart
  window.portfolioChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: chartColors
      }]
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }, // hide default legend
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
          font: { weight: 'bold', size: 14 }
        }
      }
    },
    plugins: [ChartDataLabels]
  });

  // --- External Legend ---
  const legendContainer = document.getElementById("portfolioPieChartLegend");
  if (legendContainer) {
    legendContainer.innerHTML = ""; // clear previous legend

    labels.forEach((label, i) => {
      const color = chartColors[i];

      const item = document.createElement("div");
      item.style.display = "flex";
      item.style.alignItems = "center";
      item.style.marginBottom = "4px";

      const box = document.createElement("span");
      box.style.backgroundColor = color;
      box.style.width = "16px";
      box.style.height = "16px";
      box.style.display = "inline-block";
      box.style.marginRight = "8px";

      const text = document.createElement("span");
      text.textContent = label;

      item.appendChild(box);
      item.appendChild(text);
      legendContainer.appendChild(item);
    });
  }
}


// Helper: convert hex color to rgba with alpha
function hexToRgba(hex, alpha=1) {
  const bigint = parseInt(hex.slice(1), 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r},${g},${b},${alpha})`;
}

// Assign fixed colors based on value descending (top 4 get special colors, rest grey)
function assignFixedColors(rows) {
  const colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d'];
  const sorted = Array.from(rows).slice().sort((a, b) => {
    return parseFloat(b.dataset.value) - parseFloat(a.dataset.value);
  });
  sorted.forEach((row, i) => {
    row.dataset.color = i < 4 ? colors[i] : colors[4];
  });
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

function setupSearchAndSort() {
  const table = document.getElementById('portfolioTable');
  const tbody = table.querySelector('tbody');
  let rows = Array.from(tbody.querySelectorAll('tr'));

  assignFixedColors(rows);
  applyColors(rows);

  document.getElementById('searchInput').addEventListener('input', e => {
    const term = e.target.value.toLowerCase();
    rows.forEach(row => {
      const name = row.cells[0].textContent.toLowerCase();
      row.style.display = name.includes(term) ? '' : 'none';
    });
  });

  document.getElementById('sortSelect').addEventListener('change', e => {
    const value = e.target.value;

    // Update rows list after filtering
    rows = Array.from(tbody.querySelectorAll('tr')).filter(row => row.style.display !== 'none');

    const sortedRows = rows.slice().sort((a, b) => {
      if (value === 'value-asc' || value === 'value-desc') {
        const va = parseFloat(a.dataset.value);
        const vb = parseFloat(b.dataset.value);
        return value === 'value-asc' ? va - vb : vb - va;
      } else {
        const na = a.cells[0].textContent.toLowerCase();
        const nb = b.cells[0].textContent.toLowerCase();
        return value === 'name-asc' ? na.localeCompare(nb) : nb.localeCompare(na);
      }
    });

    // Re-append rows in sorted order
    sortedRows.forEach(row => tbody.appendChild(row));

    // Reassign colors based on new sort order and visible rows only
    assignFixedColors(sortedRows);
    applyColors(sortedRows);
  });

  document.getElementById('sortSelect').dispatchEvent(new Event('change'));
}

// Call both
function initUI(portfolios) {
  renderPieChart(portfolios);
  setupSearchAndSort();
}
