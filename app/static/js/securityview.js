document.addEventListener('DOMContentLoaded', () => {
  const quickFillBtn = document.getElementById('quickFillBtn');
  if (!quickFillBtn) {
    console.error('quickFillBtn not found in DOM');
    return;
  }

  quickFillBtn.addEventListener('click', async () => {
    const symbolInput = document.getElementById('editTickerSymbol');
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
      document.getElementById('editName').value = data.name || '';
      document.getElementById('editCountry').value = data.country || '';
      document.getElementById('editWebsite').value = data.website || '';
      document.getElementById('editIndustry').value = data.industry || '';
      document.getElementById('editSector').value = data.sector || '';
      document.getElementById('editDescription').value = data.description || '';

      const categorySelect = document.getElementById('editCategory');
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
        const currencyHiddenInput = document.getElementById('editCurrency');
        const currencyButton = document.getElementById('editCurrencyDropdownButton');
        console.log('currencyHiddenInput:', currencyHiddenInput);
        console.log('currencyButton:', currencyButton);
        console.log('data.currency:', data.currency);

        if (!currencyHiddenInput) {
          console.error('❌ currencyHiddenInput not found');
          return;
        }
        if (!currencyButton) {
          console.error('❌ currencyButton not found');
          return;
        }

        let foundCurr = false;
        const currencyToMatch = data.currency.trim().toUpperCase();

        // Find matching currency option in the dropdown
        const currencyOptions = document.querySelectorAll('.edit-currency-option');
        console.log('Found currency options:', currencyOptions.length);
        
        for (const option of currencyOptions) {
          const optionText = option.getAttribute('data-code').trim().toUpperCase();
          console.log(`Comparing option "${optionText}" with "${currencyToMatch}"`);
          if (optionText === currencyToMatch) {
            const currencyId = option.getAttribute('data-value');
            const currencyCode = option.getAttribute('data-code');
            
            // Set hidden input value
            currencyHiddenInput.value = currencyId;
            // Update button text
            currencyButton.textContent = currencyCode;
            
            foundCurr = true;
            console.log('✅ Currency match found:', currencyId, currencyCode);
            break;
          }
        }

        if (!foundCurr) {
          console.warn('⚠️ No matching currency found. Keeping current selection.');
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

const editSecurityModal = document.getElementById('editSecurityModal');
const editSecurityForm = document.getElementById('editSecurityForm');

editSecurityModal.addEventListener('hidden.bs.modal', () => {
editSecurityForm.reset();

});