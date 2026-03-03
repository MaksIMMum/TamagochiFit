
    const token = localStorage.getItem('access_token');
    let userCoins = 0;

    function toggleMenu() { document.getElementById('mobileMenu').classList.toggle('open'); }

    const itemIcons = { 'Apple':'🍎','Fish':'🐟','Energy Drink':'⚡','Salad':'🥗','Cake':'🍰','Steak':'🥩' };
    const effectClass = { 'health':'effect-health', 'happiness':'effect-happiness', 'energy':'effect-energy' };

    async function loadCoins() {
      try {
        const r = await fetch('/api/food/coins', { headers:{ 'Authorization':`Bearer ${token}` } });
        if (r.ok) { const d = await r.json(); userCoins = d.coins; document.getElementById('coinBalance').textContent = userCoins; }
      } catch(e) {}
    }

    async function loadShopItems() {
      try {
        const r = await fetch('/api/food/shop', { headers:{ 'Authorization':`Bearer ${token}` } });
        if (!r.ok) return; // silently keep placeholders if API fails
        const items = await r.json();
        if (!items.length) return;

        const container = document.getElementById('shopItems');
        container.innerHTML = items.map(item => {
          const icon = itemIcons[item.name] || '🍽️';
          const canAfford = userCoins >= item.price;
          const ec = effectClass[item.effect_stat] || '';
          return `
            <div class="shop-item ${ec}">
              <div class="item-content">
                <div class="item-icon">${icon}</div>
                <h3 class="item-name">${item.name}</h3>
                <p class="item-description">${item.description || 'A tasty treat for your pet!'}</p>
                <div class="item-effect">
                  <div class="effect-label">Effect</div>
                  <div class="effect-value ${item.effect_stat}">+${item.effect_value} ${item.effect_stat}</div>
                </div>
                <div class="item-footer">
                  <div class="item-price"><span>💰</span><span>${item.price}</span></div>
                  <button class="buy-btn" onclick="buyItem(${item.id},'${item.name}',${item.price})"
                    ${!canAfford ? 'disabled' : ''}>
                    ${canAfford ? 'Buy &amp; Feed' : 'Not Enough'}
                  </button>
                </div>
              </div>
            </div>`;
        }).join('');
      } catch(e) { console.error(e); }
    }

    async function buyItem(itemId, itemName, price) {
      if (userCoins < price) {
        showModal('Not enough coins!', `You need ${price - userCoins} more coins to buy ${itemName}.`);
        return;
      }
      try {
        const r = await fetch('/api/food/shop/feed', {
          method:'POST',
          headers:{ 'Content-Type':'application/json','Authorization':`Bearer ${token}` },
          body: JSON.stringify({ item_id: itemId })
        });
        if (!r.ok) { const err = await r.json(); throw new Error(err.detail || 'Purchase failed'); }
        const result = await r.json();
        showModal('Fed your pet! 🎉', `${result.item_name}: ${result.effect_stat} +${result.effect_value}!\n\nCoins remaining: ${result.coins_remaining} 💰`);
        await loadCoins();
        await loadShopItems();
      } catch(e) { showModal('Purchase failed', e.message); }
    }

    function showModal(title, message) {
      document.getElementById('modalTitle').textContent   = title;
      document.getElementById('modalMessage').textContent = message;
      document.getElementById('successModal').classList.add('show');
    }
    function closeModal() { document.getElementById('successModal').classList.remove('show'); }

    document.getElementById('successModal').addEventListener('click', e => {
      if (e.target.classList.contains('modal')) closeModal();
    });

    async function loadUserInfo() {
      try {
        const r = await fetch('/api/auth/me', { headers:{ 'Authorization':`Bearer ${token}` } });
        if (r.ok) { const u = await r.json(); document.getElementById('userName').textContent = u.username; document.getElementById('userAvatar').textContent = u.username.charAt(0).toUpperCase(); }
      } catch(e) {}
    }

    window.addEventListener('DOMContentLoaded', () => {
      loadUserInfo();
      loadCoins().then(loadShopItems);
    });
