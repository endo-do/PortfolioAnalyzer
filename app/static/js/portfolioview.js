let sectorChart = null; // global variable to hold chart instance
let assetChart = null; // global variable to hold chart instance
let regionalChart = null; // global variable to hold chart instance

document.addEventListener('DOMContentLoaded', () => {

  const json = JSON.parse(document.getElementById("portfolio-data").textContent);
  renderAssetBreakdown(json.categories, json.portfolio);
  renderSectorBreakdown(json.sectors, json.portfolio);
  renderRegionalBreakdown(json.regions, json.portfolio);

});

function formatCurrency(value, currency = "") {
  return `${currency} ${Number(value).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function renderAssetBreakdown(categories, portfolio) {
  const table = document.getElementById('assetBreakdownTable');
  const ctx = document.getElementById("assetBreakdownChart").getContext("2d");
  const legendContainer = document.getElementById("assetBreakdownLegend");
  const currency = portfolio.currencycode || "";

  // --- Prepare and filter data ---
  const rowsData = categories.map(c => {
    const keyValue = c.bondcategoryname.toLowerCase() + "_value";
    const keyPercent = c.bondcategoryname.toLowerCase() + "_percent";
    return {
      name: c.bondcategoryname,
      value: Number(portfolio[keyValue] || 0),
      percent: Number(portfolio[keyPercent] || 0)
    };
  }).filter(r => r.value > 0).sort((a, b) => b.value - a.value);

  const baseColors = ['#007bff', '#28a745', '#ffc107', '#dc3545'];
  const greyColor = '#6c757d';

  // Assign colors for table (top 4 + grey for others)
  rowsData.forEach((r, i) => r.color = i < 4 ? baseColors[i] : greyColor);

  // --- Table ---
  if (table) {
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    rowsData.forEach(r => {
      const tr = document.createElement('tr');
      tr.dataset.color = r.color;
      tr.innerHTML = `<td>${r.name}</td><td>${formatCurrency(r.value, currency)}</td><td>${r.percent.toFixed(1)}%</td>`;
      tbody.appendChild(tr);

      const bg = hexToRgba(r.color, 0.4);
      tr.querySelectorAll('td').forEach(cell => {
        cell.style.setProperty('background-color', bg, 'important');
        cell.style.setProperty('color', 'black', 'important');
      });
    });
  }

  // --- Chart (top 4 + "Other") ---
  const topCategories = rowsData.slice(0, 4);
  const otherCategories = rowsData.slice(4);

  const chartLabels = topCategories.map(c => c.name);
  const chartData = topCategories.map(c => c.value);
  const chartColors = topCategories.map(c => c.color);

  if (otherCategories.length > 0) {
    chartLabels.push("Other");
    chartData.push(otherCategories.reduce((sum, c) => sum + c.value, 0));
    chartColors.push(greyColor);
  }

  // Destroy previous chart if exists
  if (window.assetChart) window.assetChart.destroy();

  // Create chart
  window.assetChart = new Chart(ctx, {
    type: "pie",
    data: { labels: chartLabels, datasets: [{ data: chartData, backgroundColor: chartColors }] },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.raw || 0;
              let percent = 0;
              if (context.dataIndex < topCategories.length) {
                percent = topCategories[context.dataIndex].percent;
              } else {
                percent = otherCategories.reduce((sum, c) => sum + c.percent, 0);
              }
              return ` ${percent.toFixed(1)}%: ${formatCurrency(value, currency)}`;
            }
          }
        },
        datalabels: {
          formatter: function(value, context) {
            let percent = 0;
            if (context.dataIndex < topCategories.length) {
              percent = topCategories[context.dataIndex].percent;
            } else {
              percent = otherCategories.reduce((sum, c) => sum + c.percent, 0);
            }
            return percent >= 10 ? percent.toFixed(1) + "%" : "";
          },
          color: '#fff',
          font: { weight: 'bold', size: 14 }
        }
      },
    },
    plugins: [ChartDataLabels]
  });

  // --- External Legend ---
  if (legendContainer) {
    legendContainer.innerHTML = ""; // Clear previous legend

    chartLabels.forEach((label, i) => {
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

function renderSectorBreakdown(sectors, portfolio) {
  const table = document.getElementById('sectorBreakdownTable');
  const ctx = document.getElementById("sectorBreakdownChart").getContext("2d");
  const legendContainer = document.getElementById("sectorBreakdownLegend");
  const currency = portfolio.currencycode || "";

  // Prepare and filter data
  const rowsData = sectors.map(s => {
    const keyValue = s.sectorname.toLowerCase() + "_value";
    const keyPercent = s.sectorname.toLowerCase() + "_percent";
    return {
      name: s.sectordisplayname,
      value: Number(portfolio[keyValue] || 0),
      percent: Number(portfolio[keyPercent] || 0)
    };
  }).filter(r => r.value > 0).sort((a, b) => b.value - a.value);

  const baseColors = ['#007bff', '#28a745', '#ffc107', '#dc3545'];
  const greyColor = '#6c757d';

  // Assign colors for table (top 4 + grey for others)
  rowsData.forEach((r, i) => r.color = i < 4 ? baseColors[i] : greyColor);

  // --- Table ---
  if (table) {
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    rowsData.forEach(r => {
      const tr = document.createElement('tr');
      tr.dataset.color = r.color;
      tr.innerHTML = `<td>${r.name}</td><td>${formatCurrency(r.value, currency)}</td><td>${r.percent.toFixed(1)}%</td>`;
      tbody.appendChild(tr);

      const bg = hexToRgba(r.color, 0.4);
      tr.querySelectorAll('td').forEach(cell => {
        cell.style.setProperty('background-color', bg, 'important');
        cell.style.setProperty('color', 'black', 'important');
      });
    });
  }

  // --- Chart (top 4 + "Other") ---
  const topSectors = rowsData.slice(0, 4);
  const otherSectors = rowsData.slice(4);

  const chartLabels = topSectors.map(s => s.name);
  const chartData = topSectors.map(s => s.value);
  const chartColors = topSectors.map(s => s.color);

  if (otherSectors.length > 0) {
    chartLabels.push("Other");
    chartData.push(otherSectors.reduce((sum, s) => sum + s.value, 0));
    chartColors.push(greyColor);
  }

  // Destroy previous chart if exists
  if (window.sectorChart) window.sectorChart.destroy();

  // Create chart
  window.sectorChart = new Chart(ctx, {
    type: "pie",
    data: { labels: chartLabels, datasets: [{ data: chartData, backgroundColor: chartColors }] },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.raw || 0;
              let percent = 0;
              if (context.dataIndex < topSectors.length) {
                percent = topSectors[context.dataIndex].percent;
              } else {
                percent = otherSectors.reduce((sum, s) => sum + s.percent, 0);
              }
              return ` ${percent.toFixed(1)}%: ${formatCurrency(value, currency)}`;
            }
          }
        },
        datalabels: {
          formatter: function(value, context) {
            let percent = 0;
            if (context.dataIndex < topSectors.length) {
              percent = topSectors[context.dataIndex].percent;
            } else {
              percent = otherSectors.reduce((sum, s) => sum + s.percent, 0);
            }
            return percent >= 10 ? percent.toFixed(1) + "%" : "";
          },
          color: '#fff',
          font: { weight: 'bold', size: 14 }
        }
      },
    },
    plugins: [ChartDataLabels]
  });

  // --- External Legend ---
  legendContainer.innerHTML = ""; // Clear previous legend
  chartLabels.forEach((label, i) => {
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


function renderRegionalBreakdown(regions, portfolio) {
  const table = document.getElementById('regionalBreakdownTable');
  const ctx = document.getElementById("regionalBreakdownChart").getContext("2d");
  const legendContainer = document.getElementById("regionalBreakdownLegend");
  const currency = portfolio.currencycode || "";

  // --- Prepare rows data ---
  const rowsData = regions
    .map(r => {
      const value = Number(portfolio[r.region + "_value"] || 0);
      const percent = Number(portfolio[r.region + "_percent"] || 0);
      return { name: r.region, value, percent };
    })
    .filter(r => r.value > 0)
    .sort((a, b) => b.value - a.value);

  // Assign base colors
  const baseColors = ['#007bff', '#28a745', '#ffc107', '#dc3545'];
  const greyColor = '#6c757d';
  rowsData.forEach((r, i) => r.color = i < 4 ? baseColors[i] : greyColor);

  // --- Compute total value & percent ---
  const totalValue = rowsData.reduce((sum, r) => sum + r.value, 0);
  rowsData.forEach(r => r.percent = (r.value / totalValue) * 100);

  // --- Table ---
  if (table) {
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    rowsData.forEach(r => {
      const tr = document.createElement('tr');
      tr.dataset.color = r.color;
      tr.innerHTML = `<td>${r.name}</td><td>${formatCurrency(r.value, currency)}</td><td>${r.percent.toFixed(1)}%</td>`;
      tbody.appendChild(tr);

      const bg = hexToRgba(r.color, 0.4);
      tr.querySelectorAll('td').forEach(cell => {
        cell.style.setProperty('background-color', bg, 'important');
        cell.style.setProperty('color', 'black', 'important');
      });
    });
  }

  // --- Chart ---
  const topRegions = rowsData.slice(0, 4);
  const otherRegions = rowsData.slice(4);

  const chartLabels = topRegions.map(r => r.name);
  const chartData = topRegions.map(r => r.value);
  const chartColors = topRegions.map(r => r.color);

  let otherPercent = 0;
  if (otherRegions.length > 0) {
    const otherValue = otherRegions.reduce((sum, r) => sum + r.value, 0);
    otherPercent = (otherValue / totalValue) * 100;

    chartLabels.push("Other");
    chartData.push(otherValue);
    chartColors.push(greyColor);
  }

  // Destroy previous chart if exists
  if (window.regionalChart) window.regionalChart.destroy();

  // Create chart
  window.regionalChart = new Chart(ctx, {
    type: "pie",
    data: { labels: chartLabels, datasets: [{ data: chartData, backgroundColor: chartColors }] },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }, // hide internal legend
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.raw || 0;
              let percent = context.dataIndex < topRegions.length
                ? topRegions[context.dataIndex].percent
                : otherPercent;
              return ` ${percent.toFixed(1)}%: ${formatCurrency(value, currency)}`;
            }
          }
        },
        datalabels: {
          formatter: function(value, context) {
            let percent = context.dataIndex < topRegions.length
              ? topRegions[context.dataIndex].percent
              : otherPercent;
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
  if (legendContainer) {
    legendContainer.innerHTML = "";
    chartLabels.forEach((label, i) => {
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


function hexToRgba(hex, alpha) {
  hex = hex.replace('#', '');
  const bigint = parseInt(hex, 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}