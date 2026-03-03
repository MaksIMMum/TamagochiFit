
    const token = localStorage.getItem('access_token');

    async function loadUserInfo() {
      try {
        const response = await fetch('/api/auth/me', {
          headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (response.ok) {
          const user = await response.json();
          document.getElementById('userName').textContent = user.username;
          document.getElementById('userAvatar').textContent = user.username.charAt(0).toUpperCase();
        }
      } catch(e) {
        console.error('Failed to load user info', e);
      }
    }

    async function loadLeaderboard() {
      const tbody = document.getElementById('leaderboardBody');
      try {
        const response = await fetch('/api/social/leaderboard', {
          headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error('Failed to fetch leaderboard data.');

        const result = await response.json();
        let entries = result.entries;

        if (!entries || entries.length === 0) {
          tbody.innerHTML = `<tr><td colspan="4"><div class="loading-state">No trainers found yet. Be the first!</div></td></tr>`;
          return;
        }

        // Sort dynamically by Level (descending), then by XP (descending)
        entries.sort((a, b) => {
          const levelDiff = (b.pet_level || 1) - (a.pet_level || 1);
          if (levelDiff !== 0) return levelDiff;
          return (b.xp || 0) - (a.xp || 0);
        });

        tbody.innerHTML = entries.map((user, index) => {
          // Recalculate rank based on the new level-sorted position
          const visualRank = index + 1;
          const rankClass = visualRank <= 3 ? `rank-${visualRank}` : '';

          const username = user.username || 'Unknown Trainer';
          const petName = user.pet_name || 'Egg';
          const petLevel = user.pet_level || 1;
          const xp = Math.round(user.xp || 0);

          const rowStyle = user.is_current_user ? 'background: #fdfcff; border-left: 4px solid var(--purple);' : '';

          return `
            <tr class="leaderboard-row ${rankClass}" style="${rowStyle}">
              <td class="center">
                <span class="rank-badge">${visualRank}</span>
              </td>
              <td>
                <div class="user-info">
                  <div class="user-avatar">${username.charAt(0).toUpperCase()}</div>
                  <div>
                    <div style="font-size: 16px; font-weight: 700;">
                      ${username} ${user.is_current_user ? '(You)' : ''}
                    </div>
                    <div style="font-size: 12px; color: var(--muted); margin-top: 4px;">Pet: ${petName}</div>
                  </div>
                </div>
              </td>
              <td class="center">
                <span style="font-family: 'Press Start 2P', cursive; font-size: 10px; color: var(--purple);">Lv.${petLevel}</span>
              </td>
              <td class="center">
                <div class="stat-pill xp">✨ ${xp} XP</div>
              </td>
            </tr>
          `;
        }).join('');

      } catch (error) {
        console.error(error);
        tbody.innerHTML = `<tr><td colspan="4"><div class="error-state">⚠️ Unable to load the leaderboard at this time.</div></td></tr>`;
      }
    }
    window.addEventListener('DOMContentLoaded', () => {
      loadUserInfo();
      loadLeaderboard();
    });
