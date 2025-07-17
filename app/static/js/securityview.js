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
        const currencySelect = document.getElementById('editCurrency');
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

const editSecurityModal = document.getElementById('editSecurityModal');
const editSecurityForm = document.getElementById('editSecurityForm');

editSecurityModal.addEventListener('hidden.bs.modal', () => {
// Formular zurücksetzen
editSecurityForm.reset();

// Falls du möchtest, dass die Felder mit ursprünglichen Werten gefüllt bleiben,
// dann brauchst du stattdessen einen anderen Mechanismus (z.B. die Werte nochmal setzen).
});