
    const token = localStorage.getItem('access_token');
    function toggleMenu() { document.getElementById('mobileMenu').classList.toggle('open'); }

    // Ordered stages for dynamic update
    const STAGES = [
      { rowId: 'row-egg',    minLevel: 1,  badgeId: null,          node: '✓',  completedNode: '✓' },
      { rowId: 'row-cracked',minLevel: 2,  badge: '⚡ Active',      node: '🐣' },
      { rowId: 'row-chick',  minLevel: 3,  badge: '🔒 Level 3',    node: '🐱' },
      { rowId: 'row-kitten', minLevel: 5,  badge: '🔒 Level 5',    node: '😺' },
      { rowId: 'row-cat',    minLevel: 8,  badge: '🔒 Level 8',    node: '😎' },
      { rowId: 'row-cool',   minLevel: 12, badge: '🔒 Level 12',   node: '🌟' },
    ];

    function updateEvolution(level, xp) {
      // Remove all state classes first
      STAGES.forEach(s => {
        const row = document.getElementById(s.rowId);
        row.classList.remove('completed', 'current');
      });

      let currentIdx = 0;
      STAGES.forEach((s, i) => {
        const row  = document.getElementById(s.rowId);
        const node = row.querySelector('.evo-node');
        const badge= row.querySelector('.evo-badge');

        if (level > s.minLevel) {
          // fully passed — mark completed
          row.classList.add('completed');
          node.textContent  = '✓';
          badge.textContent = '✓ Achieved';
        } else if (level >= s.minLevel) {
          // currently at this stage
          row.classList.add('current');
          node.textContent  = s.node;
          badge.textContent = i === 0 ? '✓ Hatched!' : '⚡ Active';
          currentIdx = i;
        } else {
          node.textContent  = s.node;
          badge.textContent = s.badge || `🔒 Level ${s.minLevel}`;
        }
      });

      // XP progress bar towards next stage
      const nextStage = STAGES[currentIdx + 1];
      if (nextStage) {
        const pct = Math.min(100, Math.round(((level) / nextStage.minLevel) * 100));
        document.getElementById('evoXpFill').style.width  = pct + '%';
        document.getElementById('evoXpLabel').textContent = `Lvl ${level} → ${nextStage.minLevel}`;
      }
    }
   async function loadProfile() {
      try {
        const [userRes, petRes, coinsRes, streakRes, historyRes, rankRes] = await Promise.all([
          fetch('/api/auth/me',                    { headers:{ 'Authorization':`Bearer ${token}` } }),
          fetch('/api/pet/me',                     { headers:{ 'Authorization':`Bearer ${token}` } }),
          fetch('/api/food/coins',                 { headers:{ 'Authorization':`Bearer ${token}` } }),
          fetch('/api/workout/streak',             { headers:{ 'Authorization':`Bearer ${token}` } }),
          fetch('/api/workout/history?limit=200',  { headers:{ 'Authorization':`Bearer ${token}` } }),
          fetch('/api/social/leaderboard?limit=1', { headers:{ 'Authorization':`Bearer ${token}` } })
        ]);

        if (userRes.ok) {
          const user = await userRes.json();
          document.getElementById('profileName').textContent   = user.full_name || user.username;
          document.getElementById('profileEmail').textContent  = user.email;
          document.getElementById('profileAvatar').textContent = user.username.charAt(0).toUpperCase();
          document.getElementById('userAvatarNav').textContent = user.username.charAt(0).toUpperCase();
          document.getElementById('userNameNav').textContent   = user.username;

          const joined = new Date(user.created_at);
          document.getElementById('joinDate').textContent = joined.toLocaleDateString('en-US', {month:'short', year:'numeric'});
        }

        if (petRes.ok) {
          const pet = await petRes.json();
          document.getElementById('totalXP').textContent = Math.floor(pet.xp);
          updateEvolution(pet.level, pet.xp);
        }

        if (coinsRes.ok) {
          const {coins} = await coinsRes.json();
          document.getElementById('userCoins').textContent = coins;
        }

        if (streakRes.ok) {
          const s = await streakRes.json();
          document.getElementById('activeStreak').textContent = s.current_streak;
          document.getElementById('longestStreak').textContent = s.longest_streak;
        }

        // historyRes read exactly ONCE here
        if (historyRes.ok) {
          const w = await historyRes.json();
          document.getElementById('totalWorkouts').textContent = w.length;

          const uniqueActiveDates = new Set(w.map(workout => new Date(workout.logged_at).toDateString()));
          document.getElementById('daysActive').textContent = uniqueActiveDates.size;
        }

        if (rankRes.ok) {
          const rankData = await rankRes.json();
          document.getElementById('userRank').textContent = rankData.current_user_rank ? `#${rankData.current_user_rank}` : '-';
        }

        try {
          const mealRes = await fetch('/api/food/meal/history?limit=200', { headers:{ 'Authorization':`Bearer ${token}` } });
          if (mealRes.ok) {
            const meals = await mealRes.json();
            document.getElementById('totalMeals').textContent = meals.length;
          }
        } catch(e) {}

      } catch(e) {
        console.error(e);
      }
    }
    function logout() {
      if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('token_type');
        window.location.href = '/login';
      }
    }

    // ── Profile Edit Modal ──────────────────────────────────
    function showEditModal() {
      const modal = document.getElementById('editModal');
      if (!modal) return;
      // Pre-fill with current values
      document.getElementById('editFullName').value = document.getElementById('profileName').textContent || '';
      document.getElementById('editUsername').value = document.getElementById('userNameNav').textContent || '';
      modal.style.display = 'flex';
    }

    function closeEditModal() {
      const modal = document.getElementById('editModal');
      if (modal) modal.style.display = 'none';
    }

    async function saveProfile(e) {
      e.preventDefault();
      const fullName = document.getElementById('editFullName').value.trim();
      const username = document.getElementById('editUsername').value.trim();
      const msgEl = document.getElementById('editMsg');

      try {
        const r = await fetch('/api/user/me', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ full_name: fullName, username: username || undefined })
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || 'Failed');
        msgEl.innerHTML = '<span style="color:var(--success)">✓ Saved!</span>';
        document.getElementById('profileName').textContent = data.full_name || data.username;
        document.getElementById('userNameNav').textContent = data.username;
        document.getElementById('userAvatarNav').textContent = data.username.charAt(0).toUpperCase();
        setTimeout(() => { closeEditModal(); msgEl.innerHTML = ''; }, 1200);
      } catch(err) {
        msgEl.innerHTML = `<span style="color:var(--pink)">✗ ${err.message}</span>`;
      }
    }

    async function changePassword(e) {
      e.preventDefault();
      const current = document.getElementById('currentPassword').value;
      const newPwd  = document.getElementById('newPassword').value;
      const msgEl   = document.getElementById('pwdMsg');

      try {
        const r = await fetch('/api/user/me/password', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ current_password: current, new_password: newPwd })
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || 'Failed');
        msgEl.innerHTML = '<span style="color:var(--success)">✓ Password changed!</span>';
        document.getElementById('pwdForm').reset();
        setTimeout(() => { msgEl.innerHTML = ''; }, 3000);
      } catch(err) {
        msgEl.innerHTML = `<span style="color:var(--pink)">✗ ${err.message}</span>`;
      }
    }

    window.addEventListener('DOMContentLoaded', () => { loadProfile(); });

    // Close modal on backdrop click
    document.addEventListener('click', e => {
      if (e.target.id === 'editModal') closeEditModal();
    });
