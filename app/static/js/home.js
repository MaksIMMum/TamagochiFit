
    let petTypesMap = {};

    async function loadPetTypes() {
      try {
        const response = await fetch('/api/pet-types/');
        if (response.ok) {
          const typesArray = await response.json();

          petTypesMap = {};
          typesArray.forEach(t => {
            petTypesMap[t.id] = t;
          });

        }
      } catch (e) {
        console.error('Failed to load pet types:', e);
      }
    }

    async function loadPetData() {
      const token = localStorage.getItem('access_token');
      try {
        const response = await fetch('/api/pet/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to load pet');

        const pet = await response.json();

        document.getElementById('petName').textContent = pet.name;
        document.getElementById('petLevel').textContent = `Level ${pet.level}`;

        let petTypeId = pet.pet_type || 'cherry';
        if (petTypeId === 'blue') petTypeId = 'dark_blue';

        let petImageUrl = '/static/images/characters/main_egg.png';

        if (petTypesMap[petTypeId] && petTypesMap[petTypeId].evolution_chain) {
          const evolutionChain = petTypesMap[petTypeId].evolution_chain;
          let highestValidLevel = 1;

          for (const levelThreshold of Object.keys(evolutionChain)) {
            const thresholdInt = parseInt(levelThreshold);
            if (pet.level >= thresholdInt && thresholdInt >= highestValidLevel) {
              highestValidLevel = thresholdInt;
              petImageUrl = evolutionChain[levelThreshold].image;
            }
          }
        }

        const petImageEl = document.getElementById('petImage');
        if (petImageEl) {
          petImageEl.src = petImageUrl;
          petImageEl.alt = pet.species;
        }

        document.getElementById('petSpecies').textContent = pet.species.replace(/_/g, ' ').toUpperCase();

        // Update stats
        updateStat('health', pet.health);
        updateStat('happiness', pet.happiness);
        updateStat('energy', pet.energy);

        // Update XP Bar
        const neededXP = pet.level * 100;
        const currentXP = Math.round(pet.xp);
        const xpPercent = Math.min(100, Math.max(0, (currentXP / neededXP) * 100));

        document.getElementById('currentXP').textContent = currentXP;
        document.getElementById('neededXP').textContent = neededXP;
        document.getElementById('xpBar').style.width = `${xpPercent}%`;

      } catch(e) {
        console.error('Failed to load pet:', e);
      }
    }
    function updateStat(stat, value) {
      const r = Math.round(value);
      document.getElementById(`${stat}Value`).textContent = r;
      document.getElementById(`${stat}Bar`).style.width = `${r}%`;
    }
    async function loadUserData() {
      const token = localStorage.getItem('access_token');
      try {
        const [userRes, coinsRes, streakRes, rankRes, historyRes] = await Promise.all([
          fetch('/api/auth/me',                    { headers: { 'Authorization': `Bearer ${token}` } }),
          fetch('/api/food/coins',                 { headers: { 'Authorization': `Bearer ${token}` } }),
          fetch('/api/workout/streak',             { headers: { 'Authorization': `Bearer ${token}` } }),
          fetch('/api/social/leaderboard?limit=1', { headers: { 'Authorization': `Bearer ${token}` } }),
          fetch('/api/workout/history?limit=100',  { headers: { 'Authorization': `Bearer ${token}` } })
        ]);

        if (userRes.ok) {
          const user = await userRes.json();
          document.getElementById('userName').textContent = user.username;
          document.getElementById('userAvatar').textContent = user.username.charAt(0).toUpperCase();
        }

        if (coinsRes.ok) {
          const { coins } = await coinsRes.json();
          document.getElementById('userCoins').textContent = coins;
        }

        if (streakRes.ok) {
          const s = await streakRes.json();
          document.getElementById('workoutStreak').textContent = s.current_streak;
        }

        if (rankRes.ok) {
          const rankData = await rankRes.json();
          document.getElementById('userRank').textContent = rankData.current_user_rank ? `#${rankData.current_user_rank}` : '-';
        }

        if (historyRes.ok) {
          const history = await historyRes.json();
          const todayLocalString = new Date().toDateString();

          const workoutsTodayCount = history.filter(w => {
            const dateStr = w.logged_at.endsWith('Z') ? w.logged_at : w.logged_at + 'Z';
            return new Date(dateStr).toDateString() === todayLocalString;
          }).length;

          document.getElementById('todayWorkouts').textContent = workoutsTodayCount;
        }

      } catch(e) {
        console.error('Failed to load user data:', e);
      }
    }
    // ── Feed Modal Functions ──
    async function showFeedModal() {
      document.getElementById('feedModal').classList.add('show');
      await loadFeedShopItems();
    }

    function closeFeedModal() {
      document.getElementById('feedModal').classList.remove('show');
      document.getElementById('feedModalMessage').className = 'feed-message';
      document.getElementById('feedModalMessage').textContent = '';
    }

    async function loadFeedShopItems() {
      try {
        const token = localStorage.getItem('access_token');

        const coinsRes = await fetch('/api/food/coins', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (coinsRes.ok) {
          const { coins } = await coinsRes.json();
          document.getElementById('feedModalCoins').textContent = coins;
        }

        const itemsRes = await fetch('/api/food/shop', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!itemsRes.ok) throw new Error('Failed to load shop items');

        const items = await itemsRes.json();
        const container = document.getElementById('feedShopItems');

        if (!items.length) {
          container.innerHTML = '<p style="text-align: center; color: var(--muted);">No items available</p>';
          return;
        }

        const itemIcons = {
          'Apple': '🍎',
          'Fish': '🐟',
          'Energy Drink': '⚡',
          'Salad': '🥗',
          'Cake': '🍰',
          'Steak': '🥩'
        };

        container.innerHTML = items.map(item => {
          const icon = itemIcons[item.name] || '🍽️';
          const coins = parseInt(document.getElementById('feedModalCoins').textContent);
          const canAfford = coins >= item.price;

          return `
            <div class="feed-item">
              <div class="feed-item-icon">${icon}</div>
              <div class="feed-item-name">${item.name}</div>
              <div class="feed-item-effect">+${item.effect_value} ${item.effect_stat}</div>
              <div class="feed-item-price"><span>💰</span>${item.price}</div>
              <button class="feed-buy-btn"
                ${!canAfford ? 'disabled' : ''}
                onclick="feedPetWithItem(${item.id}, '${item.name}', ${item.price})">
                ${canAfford ? 'Feed' : 'Not Enough'}
              </button>
            </div>
          `;
        }).join('');

      } catch (error) {
        console.error('Error loading feed shop:', error);
        document.getElementById('feedShopItems').innerHTML = '<p style="color: red; text-align: center;">Error loading items</p>';
      }
    }

    async function feedPetWithItem(itemId, itemName, price) {
      try {
        const token = localStorage.getItem('access_token');
        const msgEl = document.getElementById('feedModalMessage');

        const response = await fetch('/api/food/shop/feed', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ item_id: itemId })
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Failed to feed pet');
        }

        const result = await response.json();

        msgEl.className = 'feed-message success';
        msgEl.textContent = `✓ Fed ${itemName}! +${result.effect_value} ${result.effect_stat}`;

        await loadFeedShopItems();
        await loadPetData();
        await loadUserData();

        setTimeout(() => {
          msgEl.className = 'feed-message';
        }, 3000);

      } catch (error) {
        const msgEl = document.getElementById('feedModalMessage');
        msgEl.className = 'feed-message error';
        msgEl.textContent = `✗ ${error.message}`;
      }
    }

    function showMealModal() {
      window.location.href = '/meals';
    }

    function toggleMenu() {
      document.getElementById('mobileMenu').classList.toggle('open');
    }

    window.addEventListener('DOMContentLoaded', async () => {
      await loadPetTypes();
      await loadPetData();

      loadUserData();
      setInterval(loadPetData, 30000);
      setInterval(loadUserData, 30000);
    });
