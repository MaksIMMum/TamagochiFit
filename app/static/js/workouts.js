
const token = localStorage.getItem('access_token');

// ── Split data ────────────────────────────────────────────
const SPLITS = {
    push: {
    label: 'Push Day', icon: '🔴', color: 'var(--push-color)',
    exercises: [
        { name: 'Barbell Bench Press',      muscle: 'Chest',      sets: 4, reps: 8,  weight: 60 },
        { name: 'Incline Dumbbell Press',   muscle: 'Chest',      sets: 3, reps: 10, weight: 22 },
        { name: 'Cable Chest Flyes',        muscle: 'Chest',      sets: 3, reps: 12, weight: 15 },
        { name: 'Overhead Press (Barbell)', muscle: 'Shoulders',  sets: 4, reps: 8,  weight: 40 },
        { name: 'Lateral Raises',           muscle: 'Shoulders',  sets: 3, reps: 15, weight: 10 },
        { name: 'Tricep Pushdowns',         muscle: 'Triceps',    sets: 3, reps: 12, weight: 20 },
    ]
    },
    pull: {
    label: 'Pull Day', icon: '🔵', color: 'var(--pull-color)',
    exercises: [
        { name: 'Deadlift',                  muscle: 'Back',       sets: 4, reps: 5,  weight: 100 },
        { name: 'Pull-Ups',                  muscle: 'Back',       sets: 3, reps: 8,  weight: 0   },
        { name: 'Barbell Row',               muscle: 'Back',       sets: 4, reps: 8,  weight: 60  },
        { name: 'Face Pulls',                muscle: 'Rear Delts', sets: 3, reps: 15, weight: 15  },
        { name: 'Dumbbell Bicep Curls',      muscle: 'Biceps',     sets: 3, reps: 12, weight: 14  },
        { name: 'Hammer Curls',              muscle: 'Biceps',     sets: 3, reps: 12, weight: 14  },
    ]
    },
    legs: {
    label: 'Leg Day', icon: '🟢', color: 'var(--legs-color)',
    exercises: [
        { name: 'Barbell Back Squat',        muscle: 'Quads',      sets: 4, reps: 8,  weight: 80  },
        { name: 'Romanian Deadlift',         muscle: 'Hamstrings', sets: 3, reps: 10, weight: 60  },
        { name: 'Leg Press',                 muscle: 'Quads',      sets: 3, reps: 12, weight: 120 },
        { name: 'Leg Curl Machine',          muscle: 'Hamstrings', sets: 3, reps: 12, weight: 40  },
        { name: 'Hip Thrust',                muscle: 'Glutes',     sets: 3, reps: 12, weight: 60  },
        { name: 'Smith Machine Calf Raises', muscle: 'Calves',     sets: 4, reps: 20, weight: 50  },
    ]
    },
    full: {
    label: 'Full Body', icon: '🟡', color: 'var(--full-color)',
    exercises: [
        { name: 'Barbell Squat',             muscle: 'Quads',      sets: 3, reps: 8,  weight: 60  },
        { name: 'Bench Press',               muscle: 'Chest',      sets: 3, reps: 8,  weight: 55  },
        { name: 'Bent-Over Row',             muscle: 'Back',       sets: 3, reps: 8,  weight: 50  },
        { name: 'Overhead Press',            muscle: 'Shoulders',  sets: 3, reps: 10, weight: 35  },
        { name: 'Romanian Deadlift',         muscle: 'Hamstrings', sets: 3, reps: 10, weight: 55  },
        { name: 'Dips',                      muscle: 'Triceps',    sets: 3, reps: 12, weight: 0   },
        { name: 'Chin-Ups',                  muscle: 'Biceps',     sets: 3, reps: 10, weight: 0   },
        { name: 'Plank',                     muscle: 'Core',       sets: 3, reps: 60, weight: 0   },
    ]
    }
};

let activeSplit = null;

// ── Select a split ────────────────────────────────────────
function selectSplit(el, key) {
    // Deselect all
    document.querySelectorAll('.split-card').forEach(c => c.classList.remove('selected'));
    el.classList.add('selected');
    activeSplit = key;

    const split = SPLITS[key];
    renderSplitRoutine(key, split);

    // Show routine section
    const routineEl = document.getElementById('split-routine');
    routineEl.classList.add('visible');
    routineEl.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Update sidebar
    updateQuestSidebar(split);
}

function renderSplitRoutine(key, split) {
    document.getElementById('routine-icon').textContent = split.icon;
    document.getElementById('routine-name').textContent = split.label + ' Routine';
    document.getElementById('qp-icon').textContent = split.icon;
    document.getElementById('qp-label').textContent = split.label;
    document.getElementById('total-count').textContent = split.exercises.length;
    document.getElementById('done-count').textContent = 0;

    const list = document.getElementById('split-exercise-list');
    list.innerHTML = split.exercises.map((ex, i) => `
    <div class="exercise-row" id="ex-row-${i}" data-index="${i}">
        <div class="ex-num">${String(i + 1).padStart(2, '0')}</div>
        <div>
        <div class="ex-name">${ex.name}</div>
        <div class="ex-muscle">${ex.muscle}</div>
        </div>
        <div class="ex-input-wrap">
        <div class="ex-input-label">Sets</div>
        <input class="ex-input" type="number" name="sets_${i}" value="${ex.sets}" min="1" max="99">
        </div>
        <div class="ex-input-wrap">
        <div class="ex-input-label">Reps</div>
        <input class="ex-input" type="number" name="reps_${i}" value="${ex.reps}" min="1" max="999">
        </div>
        <div class="ex-input-wrap">
        <div class="ex-input-label">Wt</div>
        <input class="ex-input" type="number" name="weight_${i}" value="${ex.weight}" min="0" step="0.5">
        </div>
        <button class="complete-btn" id="cb-${i}" onclick="toggleComplete(${i})" title="Mark complete">✓</button>
    </div>
    `).join('');

    updateProgress();
}

// ── Toggle exercise complete ──────────────────────────────
function toggleComplete(i) {
    const row = document.getElementById('ex-row-' + i);
    const btn = document.getElementById('cb-' + i);
    const wasCompleted = row.classList.contains('completed');
    row.classList.toggle('completed');
    btn.classList.toggle('done');
    btn.textContent = wasCompleted ? '✓' : '✔';
    updateProgress();
}

function updateProgress() {
    if (!activeSplit) return;
    const total = SPLITS[activeSplit].exercises.length;
    const done  = document.querySelectorAll('.exercise-row.completed').length;
    document.getElementById('done-count').textContent = done;
    const pct = total === 0 ? 0 : Math.round((done / total) * 100);
    document.getElementById('progress-fill').style.width = pct + '%';
    document.getElementById('progress-pct').textContent  = pct + '%';

    // XP estimate: 15 per exercise completed
    const xp = done * 15;
    document.getElementById('xp-preview').textContent = '+' + xp + ' XP';
}

// ── Finish Split ──────────────────────────────────────────
// ── Finish Split ──────────────────────────────────────────
async function finishSplit() {
    if (!activeSplit) return;
    const split = SPLITS[activeSplit];
    const rows = document.querySelectorAll('.exercise-row');

    let completedCount = 0;
    let totalReps = 0;
    let totalSets = 0;

    // Count completed exercises and aggregate sets/reps for the log
    rows.forEach((row, i) => {
    if (row.classList.contains('completed')) {
        completedCount++;
        totalSets += parseInt(row.querySelector(`input[name="sets_${i}"]`).value) || 0;
        totalReps += parseInt(row.querySelector(`input[name="reps_${i}"]`).value) || 0;
    }
    });

    if (completedCount === 0) {
    const msgEl = document.getElementById('split-message-container');
    msgEl.innerHTML = `<div class="alert alert-danger" style="display:block;">⚠️ Please complete at least one exercise!</div>`;
    setTimeout(() => { msgEl.innerHTML = ''; }, 3000);
    return;
    }

    // Calculate rewards
    const estimatedDuration = completedCount * 5.0; // Assume 5 mins per exercise
    const coinsEarned = completedCount * 5;
    const targetXp = completedCount * 15.0;

    const msgEl = document.getElementById('split-message-container');
    const btn = document.getElementById('finishBtn');

    btn.disabled = true;
    btn.textContent = '⏳ Submitting...';

    try {
    // 1. Log the workout to the standard endpoint to update streak and history
    const logResponse = await fetch('/api/workout/log', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
        exercise_name: `${split.label} Quest`,
        muscle_group: activeSplit === 'full' ? 'full_body' : activeSplit,
        duration_mins: estimatedDuration,
        sets: totalSets,
        reps: totalReps,
        notes: `Completed ${completedCount} exercises in the ${split.label} quest.`
        })
    });

    if (!logResponse.ok) {
        const err = await logResponse.json();
        throw new Error(err.detail || 'Failed to log workout history');
    }

    // Extract XP awarded from the standard logging to avoid double-awarding XP
    const logResult = await logResponse.json();
    const baseXP = logResult.xp_awarded || 0;
    const remainingXP = Math.max(0, targetXp - baseXP);

    // 2. Call the custom splits endpoint for coins and any remaining XP
    const splitResponse = await fetch('/api/splits/finish', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
        split_name: split.label,
        duration_mins: estimatedDuration,
        coins_earned: coinsEarned,
        xp_earned: remainingXP
        })
    });

    if (!splitResponse.ok) {
        const err = await splitResponse.json();
        throw new Error(err.detail || 'Failed to process split rewards');
    }

    const splitResult = await splitResponse.json();

    // Display success message
    msgEl.innerHTML = `
        <div class="alert alert-success" style="display:block;">
        ✅ Quest Complete!<br>
        You earned <strong>+${targetXp} XP</strong> and <strong>+${coinsEarned} 💰</strong>! 🎉<br>
        <small>Total Coins: ${splitResult.new_coins_total} | Pet Level: ${splitResult.pet_level || logResult.pet_level}</small>
        </div>`;

    showXpFloat('+' + targetXp + ' XP');

    // Reload statistics to instantly reflect the new entry
    loadStats();
    loadRecentWorkouts();

    // Reset the UI tracking
    setTimeout(() => {
        msgEl.innerHTML = '';
        document.querySelectorAll('.split-card').forEach(c => c.classList.remove('selected'));
        document.getElementById('split-routine').classList.remove('visible');
        activeSplit = null;
    }, 6000);

    } catch (err) {
    msgEl.innerHTML = `<div class="alert alert-danger" style="display:block;">✗ ${err.message}</div>`;
    } finally {
    if (activeSplit) {
        btn.disabled = false;
        btn.innerHTML = `🏆 Finish Workout <span class="xp-preview" id="xp-preview">+${targetXp} XP</span>`;
    }
    }
}
function showXpFloat(text) {
    const el = document.createElement('div');
    el.className = 'xp-float';
    el.textContent = text;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1500);
}

// ── Sidebar quest summary ─────────────────────────────────
function updateQuestSidebar(split) {
    const card    = document.getElementById('today-quest-card');
    const summary = document.getElementById('today-quest-summary');
    card.style.display = 'block';
    summary.innerHTML = split.exercises.map(ex => `
    <div class="quest-summary-row">
        <div class="qs-icon">💪</div>
        <div class="qs-info">
        <div class="qs-name">${ex.name}</div>
        <div class="qs-meta">${ex.sets}×${ex.reps} · ${ex.muscle}</div>
        </div>
        <div class="qs-xp">+15 XP</div>
    </div>
    `).join('');
}

// ── Tab switching ─────────────────────────────────────────
function switchTab(tab, btn) {
    document.querySelectorAll('.mode-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('panel-quick').style.display  = tab === 'quick'  ? '' : 'none';
    document.getElementById('panel-manual').style.display = tab === 'manual' ? '' : 'none';
}

// ── Quick log helper ──────────────────────────────────────
function quickLog(name, muscle, duration) {
    switchTab('manual', document.querySelectorAll('.mode-tab')[1]);
    document.getElementById('exerciseName').value = name;
    document.getElementById('muscleGroup').value  = muscle;
    document.getElementById('duration').value     = duration;
    document.getElementById('exerciseName').focus();
    document.getElementById('panel-manual').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Manual form submit ────────────────────────────────────
document.getElementById('workoutForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById('submitBtn');
    const msgEl     = document.getElementById('message-container');

    const workoutData = {
    exercise_name:  document.getElementById('exerciseName').value,
    muscle_group:   document.getElementById('muscleGroup').value  || null,
    duration_mins:  parseFloat(document.getElementById('duration').value),
    sets:           parseInt(document.getElementById('sets').value)     || null,
    reps:           parseInt(document.getElementById('reps').value)     || null,
    calories_burned:parseFloat(document.getElementById('calories').value)|| null,
    notes:          document.getElementById('notes').value              || null
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging...';
    msgEl.innerHTML = '';

    try {
    const response = await fetch('/api/workout/log', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify(workoutData)
    });

    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to log workout');
    }
    const result = await response.json();
    msgEl.innerHTML = `<div class="alert alert-success" style="display:block;">✓ Workout logged! You earned ${result.xp_awarded} XP! 🎉</div>`;
    document.getElementById('workoutForm').reset();
    loadStats();
    loadRecentWorkouts();
    setTimeout(() => { msgEl.innerHTML = ''; }, 5000);
    } catch (err) {
    msgEl.innerHTML = `<div class="alert alert-danger" style="display:block;">✗ ${err.message}</div>`;
    } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Log Workout & Earn XP';
    }
});

// ── Load stats ────────────────────────────────────────────
async function loadStats() {
    try {
    const [streakRes, historyRes] = await Promise.all([
        fetch('/api/workout/streak',         { headers: token ? { 'Authorization': `Bearer ${token}` } : {} }),
        fetch('/api/workout/history?limit=50', { headers: token ? { 'Authorization': `Bearer ${token}` } : {} })
    ]);
    if (streakRes.ok) {
        const s = await streakRes.json();
        document.getElementById('currentStreak').textContent = s.current_streak;
        document.getElementById('longestStreak').textContent = s.longest_streak;
    }
    if (historyRes.ok) {
        const history = await historyRes.json();
        document.getElementById('totalWorkouts').textContent = history.length;
        const oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

        // Append 'Z' to force UTC timezone evaluation
        document.getElementById('thisWeek').textContent = history.filter(w => {
        const dateStr = w.logged_at.endsWith('Z') ? w.logged_at : w.logged_at + 'Z';
        return new Date(dateStr) > oneWeekAgo;
        }).length;
    }
    } catch(e) { console.error('loadStats:', e); }
}async function loadRecentWorkouts() {
    try {
    const response = await fetch('/api/workout/history?limit=5', {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error('Failed to load');
    const workouts  = await response.json();
    const container = document.getElementById('recentWorkouts');
    if (!workouts.length) {
        container.innerHTML = '<p style="text-align:center;color:var(--muted);padding:20px;">No workouts yet. Start logging!</p>';
        return;
    }
    container.innerHTML = workouts.map(w => {
        // Append 'Z' to force UTC timezone evaluation for the "time ago" string
        const dateStr = w.logged_at.endsWith('Z') ? w.logged_at : w.logged_at + 'Z';
        const timeAgo = getTimeAgo(new Date(dateStr));

        return `
        <div class="workout-item">
            <div class="workout-header">
            <div class="workout-name">${w.exercise_name}</div>
            <div class="workout-xp">+${Math.round(w.duration_mins)} XP</div>
            </div>
            <div class="workout-details">
            <span>⏱️ ${w.duration_mins}min</span>
            ${w.sets && w.reps ? `<span>💪 ${w.sets}×${w.reps}</span>` : ''}
            <span>🕐 ${timeAgo}</span>
            </div>
        </div>`;
    }).join('');
    } catch(e) { console.error('loadRecentWorkouts:', e); }
}

function getTimeAgo(date) {
    const s = Math.floor((new Date() - date) / 1000);
    if (s < 60)    return 'just now';
    if (s < 3600)  return `${Math.floor(s / 60)}m ago`;
    if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
    return `${Math.floor(s / 86400)}d ago`;
}

async function loadUserInfo() {
    try {
    const response = await fetch('/api/auth/me', {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (response.ok) {
        const user = await response.json();
        document.getElementById('userName').textContent   = user.username;
        document.getElementById('userAvatar').textContent = user.username.charAt(0).toUpperCase();
    }
    } catch(e) {}
}

window.addEventListener('DOMContentLoaded', () => {
    loadUserInfo();
    loadStats();
    loadRecentWorkouts();
});
