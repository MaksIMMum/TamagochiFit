
    const token = localStorage.getItem('access_token');

    function toggleMenu() { document.getElementById('mobileMenu').classList.toggle('open'); }

    document.getElementById('mealForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = document.getElementById('submitBtn');
      const msgEl = document.getElementById('message-container');
      const mealType = document.querySelector('input[name="meal_type"]:checked')?.value;
      const quality  = document.getElementById('quality').value;
      const notes    = document.getElementById('notes').value;
      if (!mealType || !quality) return;

      submitBtn.disabled = true;
      submitBtn.textContent = 'Logging...';
      msgEl.innerHTML = '';

      try {
        const response = await fetch('/api/food/meal', {
          method: 'POST',
          headers: { 'Content-Type':'application/json', 'Authorization':`Bearer ${token}` },
          body: JSON.stringify({ meal_type: mealType, quality, notes: notes || null })
        });
        if (!response.ok) { const err = await response.json(); throw new Error(err.detail || 'Failed'); }
        const result = await response.json();
        msgEl.innerHTML = `<div class="alert alert-success" style="display:block;">✓ Meal logged! ${result.pet_effect}</div>`;
        document.getElementById('mealForm').reset();
        loadMealHistory();
        setTimeout(() => { msgEl.innerHTML = ''; }, 5000);
      } catch(err) {
        msgEl.innerHTML = `<div class="alert alert-danger" style="display:block;">✗ ${err.message}</div>`;
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Log Meal';
      }
    });

    async function loadMealHistory() {
      try {
        const response = await fetch('/api/food/meal/history?limit=20', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed');
        const meals = await response.json();
        const container = document.getElementById('mealHistory');
        if (!meals.length) {
          container.innerHTML = '<p style="text-align:center;color:var(--muted);padding:40px 20px;">No meals logged yet.</p>';
          return;
        }
        container.innerHTML = meals.map(meal => {

          const dateStr = meal.logged_at.endsWith('Z') ? meal.logged_at : meal.logged_at + 'Z';
          const d = new Date(dateStr);
          const fmt = d.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
          return `
            <div class="meal-item">
              <div class="meal-header">
                <div>
                  <div class="meal-type-text">${getMealIcon(meal.meal_type)} ${meal.meal_type}</div>
                  <div class="meal-time">${fmt} • ${getTimeAgo(d)}</div>
                </div>
                <div class="meal-quality ${meal.quality}">${meal.quality}</div>
              </div>
              ${meal.notes  ? `<div class="meal-notes">${meal.notes}</div>` : ''}
              ${meal.pet_effect ? `<div class="meal-effect">🐾 ${meal.pet_effect}</div>` : ''}
            </div>
          `;
        }).join('');
      } catch(e) { console.error(e); }
    }

    function getMealIcon(t) { return {breakfast:'🌅',lunch:'☀️',dinner:'🌙',snack:'🍪'}[t] || '🍽️'; }
    function getTimeAgo(d) {
      const s = Math.floor((new Date() - d) / 1000);
      if (s < 60)    return 'just now';
      if (s < 3600)  return `${Math.floor(s/60)}m ago`;
      if (s < 86400) return `${Math.floor(s/3600)}h ago`;
      return `${Math.floor(s/86400)}d ago`;
    }

    async function loadUserInfo() {
      try {
        const r = await fetch('/api/auth/me', { headers: { 'Authorization': `Bearer ${token}` } });
        if (r.ok) {
          const u = await r.json();
          document.getElementById('userName').textContent   = u.username;
          document.getElementById('userAvatar').textContent = u.username.charAt(0).toUpperCase();
        }
      } catch(e) {}
    }

    window.addEventListener('DOMContentLoaded', () => { loadUserInfo(); loadMealHistory(); });
