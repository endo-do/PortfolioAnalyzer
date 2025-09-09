document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const regionFilter = document.getElementById('regionFilter');
  const sectorFilter = document.getElementById('sectorFilter');
  const sortBySelect = document.getElementById('sortBySelect');
  const sortOrderRadios = document.querySelectorAll('input[name="sortOrder"]');
  const table = document.getElementById('bondsTable3');
  const tbody = table.querySelector('tbody');

  // Save original rows to preserve unfiltered data
  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  function normalize(str) {
    return str.toLowerCase();
  }

  function getSortOrder() {
    const checkedRadio = document.querySelector('input[name="sortOrder"]:checked');
    return checkedRadio ? checkedRadio.value : 'asc';
  }

  function getConvertedValue(row) {
    const exchangeRate = parseFloat(row.dataset.exchangeRate) || 1.0;
    const originalValue = parseFloat(row.dataset.originalValue) || 0;
    return originalValue * exchangeRate;
  }

  function filterAndSort() {
    const searchText = normalize(searchInput.value.trim());
    const category = categoryFilter.value;
    const sortBy = sortBySelect.value;
    const sortOrder = getSortOrder();

    // Copy original rows
    let rows = originalRows.slice();

    // Filter rows by search and category
    rows = rows.filter(row => {
      const symbol = normalize(row.cells[0].textContent);
      const name = normalize(row.cells[1].textContent);
      // Get category text from the badge span element
      const categoryElement = row.cells[2].querySelector('.badge');
      const cat = categoryElement ? normalize(categoryElement.textContent) : normalize(row.cells[2].textContent);
      const matchesSearch = symbol.includes(searchText) || name.includes(searchText);
      const matchesCategory = category === 'All' || cat === normalize(category);
      return matchesSearch && matchesCategory;
    });

    // Sort rows
    rows.sort((a, b) => {
      let comparison = 0;
      
      if (sortBy === 'name') {
        const nameA = a.cells[1].textContent.toLowerCase();
        const nameB = b.cells[1].textContent.toLowerCase();
        if (nameA < nameB) comparison = -1;
        else if (nameA > nameB) comparison = 1;
      } else if (sortBy === 'value') {
        // Use converted values for proper currency comparison
        const valA = getConvertedValue(a);
        const valB = getConvertedValue(b);
        comparison = valA - valB;
      } else if (sortBy === 'date') {
        const dateA = new Date(a.cells[4].textContent);
        const dateB = new Date(b.cells[4].textContent);
        comparison = dateA - dateB;
      }
      
      return sortOrder === 'desc' ? -comparison : comparison;
    });

    // Clear tbody and re-append sorted and filtered rows
    tbody.innerHTML = '';

    if (rows.length === 0) {
      const noRow = document.createElement('tr');
      const noCell = document.createElement('td');
      noCell.colSpan = 6; // number of columns
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
  regionFilter.addEventListener('change', filterAndSort);
  sectorFilter.addEventListener('change', filterAndSort);
  sortBySelect.addEventListener('change', filterAndSort);
  sortOrderRadios.forEach(radio => {
    radio.addEventListener('change', filterAndSort);
  });

  // Initial call
  filterAndSort();
});

const createSecurityModal = document.getElementById('createSecurityModal');
const createSecurityForm = document.getElementById('createSecurityForm');

if (createSecurityModal && createSecurityForm) {
  createSecurityModal.addEventListener('hidden.bs.modal', () => {
    createSecurityForm.reset();
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const quickFillBtn = document.getElementById('quickFillBtn');
  if (!quickFillBtn) {
    console.error('quickFillBtn not found in DOM');
    return;
  }

  quickFillBtn.addEventListener('click', async () => {
    const symbolInput = document.getElementById('tickerSymbol');
    if (!symbolInput) {
      alert('Ticker symbol input not found.');
      return;
    }

    const symbol = symbolInput.value.trim();
    if (!symbol) {
      alert('Please enter a ticker symbol first.');
      return;
    }

    try {
      const response = await fetch(`/api/securityinfo/${encodeURIComponent(symbol)}`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });

      if (!response.ok) {
        throw new Error('Security info not found or API error');
      }

      const data = await response.json();

      // Felder befüllen:
      document.getElementById('name').value = data.name || '';
      document.getElementById('country').value = data.country || '';
      document.getElementById('website').value = data.website || '';
      document.getElementById('industry').value = data.industry || '';
      document.getElementById('sector').value = data.sector || '';
      document.getElementById('description').value = data.description || '';

      const categorySelect = document.getElementById('category');
      console.log('categorySelect:', categorySelect);
      console.log('data.category:', data.category);

      if (categorySelect && data.category) {
        const categoryToMatch = data.category.trim().toLowerCase();
        let foundCat = false;

        for (const option of categorySelect.options) {
          const optionText = option.text.trim().toLowerCase();
          console.log(`Comparing option "${optionText}" with "${categoryToMatch}"`);
          if (optionText === categoryToMatch) {
            categorySelect.value = option.value;
            foundCat = true;
            console.log('✅ Match found:', option.value);
            break;
          }
        }

        if (!foundCat) {
          categorySelect.selectedIndex = 0;
          console.warn('⚠️ No matching category found. Set to default (index 0).');
        }
      } else {
        console.error('❌ categorySelect or data.category is missing.');
      }

      // Currency
      if (data.currency) {
        const currencySelect = document.getElementById('currency');
        console.log('currencySelect:', currencySelect);
        console.log('data.currency:', data.currency);

        let foundCurr = false;
        const currencyToMatch = data.currency.trim().toUpperCase();

        for (const option of currencySelect.options) {
          const optionText = option.text.trim().toUpperCase();
          console.log(`Comparing option "${optionText}" with "${currencyToMatch}"`);
          if (optionText === currencyToMatch) {
            currencySelect.value = option.value;
            foundCurr = true;
            console.log('✅ Currency match found:', option.value);
            break;
          }
        }

        if (!foundCurr) {
          currencySelect.selectedIndex = 0;
          console.warn('⚠️ No matching currency found. Set to default (index 0).');
        }
      } else {
        console.error('❌ data.currency is missing.');
      }

      // Optional: Set the ticker symbol if not already set
      if (!symbolInput.value) {
        symbolInput.value = data.symbol || '';
      }

    } catch (error) {
      alert('Error fetching security info: ' + error.message);
    }
  });
});

// Function to show custom notifications
function showNotification(message, type = 'info') {
  const notificationContainer = document.getElementById('notificationContainer');
  if (!notificationContainer) {
    // Create notification container if it doesn't exist
    const container = document.createElement('div');
    container.id = 'notificationContainer';
    container.className = 'position-fixed';
    container.style.cssText = 'top: 20px; right: 20px; z-index: 1050; max-width: 400px;';
    document.body.appendChild(container);
  }
  
  const notification = document.createElement('div');
  notification.className = `notification alert-${type} mb-3`;
  notification.setAttribute('role', 'alert');
  
  const iconClass = type === 'success' ? 'fas fa-check-circle' : 
                   type === 'danger' ? 'fas fa-exclamation-circle' :
                   type === 'warning' ? 'fas fa-exclamation-triangle' :
                   'fas fa-info-circle';
  
  notification.innerHTML = `
    <div class="d-flex align-items-center">
      <div class="notification-icon me-3">
        <i class="${iconClass}"></i>
      </div>
      <div class="flex-grow-1">
        <div class="notification-message">${message}</div>
      </div>
      <button type="button" class="btn-close-notification" aria-label="Close">
        <i class="fas fa-times"></i>
      </button>
    </div>
    <div class="notification-progress"></div>
  `;
  
  document.getElementById('notificationContainer').appendChild(notification);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 5000);
  
  // Add close button functionality
  notification.querySelector('.btn-close-notification').addEventListener('click', () => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  });
}

// Handle create security form submission with modals
document.addEventListener('DOMContentLoaded', () => {
  const createSecurityForm = document.getElementById('createSecurityForm');
  const createSecurityModal = new bootstrap.Modal(document.getElementById('createSecurityModal'));

  if (createSecurityForm) {
    createSecurityForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const formData = new FormData(createSecurityForm);
      const currencyValue = formData.get('bondcurrencyid');
      const bondSymbol = formData.get('bondsymbol');
      
      // Basic client-side validation
      if (!bondSymbol || bondSymbol.trim() === '') {
        alert('Security symbol is required');
        return;
      }
      
      // Check if security symbol already exists
      try {
        const checkResponse = await fetch('/admin/check_security_exists', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `bondsymbol=${encodeURIComponent(bondSymbol.trim())}&csrf_token=${document.querySelector('input[name="csrf_token"]').value}`
        });
        
        if (checkResponse.ok) {
          const checkResult = await checkResponse.json();
          if (checkResult.exists) {
            alert(`Security '${bondSymbol}' already exists. Please use a different symbol or check if the security is already in the system.`);
            return;
          }
        }
      } catch (error) {
        console.warn('Could not check if security exists:', error);
        // Continue with form submission if check fails
      }
      
      // Proceed with normal submission
        await submitSecurityForm(formData);
    });
  }






  // Function to submit security form
  async function submitSecurityForm(formData) {
    try {
      console.log('Submitting form data:', Object.fromEntries(formData.entries()));
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout for main form
      
      const response = await fetch('/admin/create_security', {
        method: 'POST',
        body: formData,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);
      
      if (response.ok) {
      // Try to parse JSON response
      let result;
      try {
        const responseText = await response.text();
        console.log('Response text:', responseText);
        result = JSON.parse(responseText);
      } catch (parseError) {
        console.error('JSON parse error:', parseError);
        throw new Error('Invalid response format from server');
      }
      
      console.log('Response result:', result);
      
      if (result.status === 'success') {
        createSecurityModal.hide();
          // Show success message using custom notification
          showNotification(result.message, 'success');
          // Reload the page to show updated data
          setTimeout(() => {
        window.location.reload();
          }, 1500);
        } else {
          showNotification(result.message || 'Unknown error', 'danger');
        }
      } else {
        // Handle error response
        const errorText = await response.text();
        console.error('Error response:', errorText);
        showNotification('Error creating security: ' + errorText, 'danger');
      }
    } catch (error) {
      console.error('Error:', error);
      if (error.name === 'AbortError') {
        alert('Request timed out. Please try again.');
      } else {
        alert('An error occurred while creating the security: ' + error.message);
      }
    }
  }
  
});

// Currency creation functionality
document.addEventListener('DOMContentLoaded', () => {
  const addCurrencyBtn = document.getElementById('addCurrencyBtn');
  const currencyCreationRow = document.getElementById('currencyCreationRow');
  const createCurrencyBtn = document.getElementById('createCurrencyBtn');
  const newCurrencyNameInput = document.getElementById('newCurrencyName');
  const newCurrencyCodeInput = document.getElementById('newCurrencyCode');
  const currencySelect = document.getElementById('currency');

  // Show/hide currency creation form
  if (addCurrencyBtn) {
    addCurrencyBtn.addEventListener('click', () => {
      const isVisible = currencyCreationRow.style.display !== 'none';
      
      if (isVisible) {
        // Hide the form
        currencyCreationRow.style.display = 'none';
        currencyCreationRow.classList.remove('show');
        // Clear inputs when hiding the form
        newCurrencyNameInput.value = '';
        newCurrencyCodeInput.value = '';
      } else {
        // Show the form with animation
        currencyCreationRow.style.display = 'block';
        // Trigger animation after a small delay to ensure display is set
        setTimeout(() => {
          currencyCreationRow.classList.add('show');
          // Focus on the first input when showing the form
          newCurrencyNameInput.focus();
        }, 10);
      }
    });
  }

  // Auto-uppercase currency code input
  if (newCurrencyCodeInput) {
    newCurrencyCodeInput.addEventListener('input', (e) => {
      e.target.value = e.target.value.toUpperCase();
    });
  }

  // Create currency functionality
  if (createCurrencyBtn) {
    createCurrencyBtn.addEventListener('click', async () => {
      const currencyName = newCurrencyNameInput.value.trim();
      const currencyCode = newCurrencyCodeInput.value.trim();

      // Validation
      if (!currencyName) {
        showNotification('Please enter a currency name', 'warning');
        newCurrencyNameInput.focus();
        return;
      }

      if (!currencyCode || currencyCode.length !== 3) {
        showNotification('Please enter a valid 3-character currency code', 'warning');
        newCurrencyCodeInput.focus();
        return;
      }

      // Check if currency already exists in dropdown
      const existingOption = Array.from(currencySelect.options).find(option => 
        option.textContent.toUpperCase() === currencyCode.toUpperCase()
      );
      
      if (existingOption) {
        showNotification('Currency already exists in the system', 'warning');
        return;
      }

      try {
        // Show loading state
        createCurrencyBtn.disabled = true;
        createCurrencyBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Creating...';

        // Create form data
        const formData = new FormData();
        formData.append('currencyname', currencyName);
        formData.append('currencycode', currencyCode);
        formData.append('csrf_token', document.querySelector('input[name="csrf_token"]').value);

        // Send request to create currency
        const response = await fetch('/admin/create_currency_ajax', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();

        if (result.status === 'success') {
          // Add new option to dropdown
          const newOption = document.createElement('option');
          newOption.value = result.currency_id;
          newOption.textContent = result.currency_code;
          currencySelect.appendChild(newOption);
          
          // Select the newly created currency
          currencySelect.value = result.currency_id;
          
          // Hide the creation form
          currencyCreationRow.style.display = 'none';
          newCurrencyNameInput.value = '';
          newCurrencyCodeInput.value = '';
          
          showNotification(`Currency ${result.currency_code} created successfully! 🎉`, 'success');
        } else {
          showNotification(result.message || 'Error creating currency', 'danger');
        }
      } catch (error) {
        console.error('Error creating currency:', error);
        showNotification('Error creating currency: ' + error.message, 'danger');
      } finally {
        // Reset button state
        createCurrencyBtn.disabled = false;
        createCurrencyBtn.innerHTML = '<i class="fas fa-check me-1"></i>Create';
      }
    });
  }

  // Hide currency creation form when modal is closed
  const createSecurityModal = document.getElementById('createSecurityModal');
  if (createSecurityModal) {
    createSecurityModal.addEventListener('hidden.bs.modal', () => {
      currencyCreationRow.style.display = 'none';
      currencyCreationRow.classList.remove('show');
      newCurrencyNameInput.value = '';
      newCurrencyCodeInput.value = '';
    });
  }
});

// Exchange creation functionality
document.addEventListener('DOMContentLoaded', () => {
  const addExchangeBtn = document.getElementById('addExchangeBtn');
  const exchangeCreationRow = document.getElementById('exchangeCreationRow');
  const createExchangeBtn = document.getElementById('createExchangeBtn');
  const newExchangeNameInput = document.getElementById('newExchangeName');
  const newExchangeRegionSelect = document.getElementById('newExchangeRegion');
  const exchangeSelect = document.getElementById('exchange');

  // Show/hide exchange creation form
  if (addExchangeBtn) {
    addExchangeBtn.addEventListener('click', () => {
      const isVisible = exchangeCreationRow.style.display !== 'none';
      
      if (isVisible) {
        // Hide the form
        exchangeCreationRow.style.display = 'none';
        exchangeCreationRow.classList.remove('show');
        // Clear inputs when hiding the form
        newExchangeNameInput.value = '';
        newExchangeRegionSelect.selectedIndex = 0;
      } else {
        // Show the form with animation
        exchangeCreationRow.style.display = 'block';
        // Trigger animation after a small delay to ensure display is set
        setTimeout(() => {
          exchangeCreationRow.classList.add('show');
          // Focus on the first input when showing the form
          newExchangeNameInput.focus();
        }, 10);
      }
    });
  }

  // Auto-uppercase exchange name input
  if (newExchangeNameInput) {
    newExchangeNameInput.addEventListener('input', (e) => {
      e.target.value = e.target.value.toUpperCase();
    });
  }

  // Create exchange functionality
  if (createExchangeBtn) {
    createExchangeBtn.addEventListener('click', async () => {
      const exchangeName = newExchangeNameInput.value.trim();
      const regionId = newExchangeRegionSelect.value;

      // Validation
      if (!exchangeName) {
        showNotification('Please enter an exchange name', 'warning');
        newExchangeNameInput.focus();
        return;
      }

      if (!regionId) {
        showNotification('Please select a region', 'warning');
        newExchangeRegionSelect.focus();
        return;
      }

      // Check if exchange already exists in dropdown
      const existingOption = Array.from(exchangeSelect.options).find(option => 
        option.textContent.toUpperCase().includes(exchangeName.toUpperCase())
      );
      
      if (existingOption) {
        showNotification('Exchange already exists in the system', 'warning');
        return;
      }

      try {
        // Show loading state
        createExchangeBtn.disabled = true;
        createExchangeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Creating...';

        // Create form data
        const formData = new FormData();
        formData.append('exchangename', exchangeName);
        formData.append('regionid', regionId);
        formData.append('csrf_token', document.querySelector('input[name="csrf_token"]').value);

        // Send request to create exchange
        const response = await fetch('/admin/create_exchange_ajax', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();

        if (result.status === 'success') {
          // Add new option to dropdown
          const newOption = document.createElement('option');
          newOption.value = result.exchange_id;
          newOption.textContent = result.exchange_name;
          exchangeSelect.appendChild(newOption);
          
          // Select the newly created exchange
          exchangeSelect.value = result.exchange_id;
          
          // Hide the creation form
          exchangeCreationRow.style.display = 'none';
          exchangeCreationRow.classList.remove('show');
          newExchangeNameInput.value = '';
          newExchangeRegionSelect.selectedIndex = 0;
          
          showNotification(`Exchange ${result.exchange_name} created successfully! 🎉`, 'success');
        } else {
          showNotification(result.message || 'Error creating exchange', 'danger');
        }
      } catch (error) {
        console.error('Error creating exchange:', error);
        showNotification('Error creating exchange: ' + error.message, 'danger');
      } finally {
        // Reset button state
        createExchangeBtn.disabled = false;
        createExchangeBtn.innerHTML = '<i class="fas fa-check me-1"></i>Create';
      }
    });
  }

  // Hide exchange creation form when modal is closed
  const createSecurityModal = document.getElementById('createSecurityModal');
  if (createSecurityModal) {
    createSecurityModal.addEventListener('hidden.bs.modal', () => {
      exchangeCreationRow.style.display = 'none';
      exchangeCreationRow.classList.remove('show');
      newExchangeNameInput.value = '';
      newExchangeRegionSelect.selectedIndex = 0;
    });
  }
});