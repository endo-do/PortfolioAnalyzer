// Pie chart
function renderPieChart(portfolios) {
  const currency = portfolios.length ? portfolios[0].currencycode : "";

  let sorted = portfolios.slice().sort((a, b) => (b.converted_value || b.total_value) - (a.converted_value || a.total_value));
  let labels = [];
  let data = [];
  let percentages = [];
  let othersValue = 0;
  let othersPercent = 0;

  // Calculate total value to check if portfolios have any data
  const totalValue = sorted.reduce((sum, p) => sum + (p.converted_value || p.total_value), 0);
  
  // If no portfolios or all portfolios have zero value, show a placeholder "100%" chart
  if (sorted.length === 0 || totalValue === 0) {
    labels = sorted.length === 0 ? ["No Portfolios"] : ["No Securities"];
    data = [1];
    percentages = [100];
  } else {
    sorted.forEach((p, i) => {
      if (i < 4) {
        labels.push(p.portfolioname);
        data.push(p.converted_value || p.total_value);
        percentages.push(Number(p.percentage));
      } else {
        othersValue += p.converted_value || p.total_value;
        othersPercent += Number(p.percentage);
      }
    });

    if (sorted.length >= 5) {
      labels.push("Other");
      data.push(othersValue);
      percentages.push(othersPercent);
    }
  }

  // Assign colors based on portfolio order (same as table)
  const colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d'];
  const chartColors = labels.map((label, i) => {
    if (label === "No Portfolios" || label === "No Securities") {
      return colors[4]; // grey for empty states
    }
    if (label === "Other") {
      return colors[4]; // grey for "Other"
    }
    // For individual portfolios, use the same color assignment as the table
    // sorted array is already ordered by value descending, so index matches table color assignment
    return colors[i]; // blue, green, yellow, red for top 4
  });
  
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
function assignFixedColors(cards) {
  const colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d'];
  const sorted = Array.from(cards).slice().sort((a, b) => {
    return parseFloat(b.dataset.value) - parseFloat(a.dataset.value);
  });
  sorted.forEach((card, i) => {
    card.dataset.color = i < 4 ? colors[i] : colors[4];
  });
}

function applyColors(cards) {
  cards.forEach(card => {
    const c = card.dataset.color || '#6c757d';
    const bg = hexToRgba(c, 0.1);
    const cardElement = card.querySelector('.card');
    if (cardElement) {
      cardElement.style.setProperty('background-color', bg, 'important');
      cardElement.style.setProperty('border-left', `4px solid ${c}`, 'important');
    }
  });
}

function setupSearchAndSort() {
  const container = document.querySelector('.portfolio-cards-container');
  let cards = Array.from(container.querySelectorAll('.portfolio-card'));
  let sortAsc = false; // Track sort order

  assignFixedColors(cards);
  applyColors(cards);

  // Filter cards by search
  function filterCards() {
    const searchInput = document.getElementById('searchInput');
    const term = searchInput.value.toLowerCase();
    cards.forEach(card => {
      const nameElement = card.querySelector('h6');
      const name = nameElement ? nameElement.textContent.toLowerCase() : '';
      card.style.display = name.includes(term) ? '' : 'none';
    });
  }

  // Sort cards by value
  function sortCards() {
    const visibleCards = cards.filter(card => card.style.display !== 'none');
    visibleCards.sort((a, b) => {
      const valueA = parseFloat(a.dataset.value) || 0;
      const valueB = parseFloat(b.dataset.value) || 0;
      
      return sortAsc ? valueA - valueB : valueB - valueA;
    });

    // Re-append cards in sorted order
    visibleCards.forEach(card => container.appendChild(card));

    // Reassign colors based on new sort order and visible cards only
    assignFixedColors(visibleCards);
    applyColors(visibleCards);
  }

  // Combined update function
  function updateCards() {
    filterCards();
    sortCards();
  }

  // Event listeners
  document.getElementById('searchInput').addEventListener('input', updateCards);

  // Sort toggle button
  const sortBtn = document.getElementById('sortBtn');
  if (sortBtn) {
    sortBtn.addEventListener('click', () => {
      sortAsc = !sortAsc;
      sortBtn.innerHTML = sortAsc ? '<i class="fas fa-sort-amount-up me-2"></i>Value ↑' : '<i class="fas fa-sort-amount-down me-2"></i>Value ↓';
      sortCards();
    });
  }


  // Initial sort
  sortCards();
}

// Call both
function initUI(portfolios) {
  // Always render pie chart if canvas exists (will show "100%" if no portfolios)
  const canvas = document.getElementById("portfolioPieChart");
  if (canvas) {
    renderPieChart(portfolios || []);
  }
  setupSearchAndSort();
}
