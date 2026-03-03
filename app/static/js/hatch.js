
    // === Helpers ===
    function getToken() {
      return localStorage.getItem('access_token');
    }

    function showStage(stageId) {
      document.querySelectorAll('.stage').forEach(s => s.classList.add('hidden'));
      document.getElementById(stageId).classList.remove('hidden');
    }

    function createSparkle(x, y) {
      const sparkle = document.createElement('div');
      sparkle.className = 'sparkle';
      sparkle.textContent = ['✨', '⭐', '💫', '🌟'][Math.floor(Math.random() * 4)];
      sparkle.style.left = x + 'px';
      sparkle.style.top = y + 'px';
      document.body.appendChild(sparkle);
      setTimeout(() => sparkle.remove(), 1000);
    }

    // === Egg Clicking ===
    const CLICKS_NEEDED = 5;
    let clickCount = 0;

    const eggImage = document.getElementById('eggImage');
    const clickLabel = document.getElementById('clickCount');

    eggImage.addEventListener('click', function onClick(e) {
      clickCount++;
      clickLabel.textContent = `${clickCount} / ${CLICKS_NEEDED} clicks`;

      // Create sparkles at click position
      createSparkle(e.clientX, e.clientY);

      // Shake animation
      eggImage.style.transform = `scale(1.1) rotate(${clickCount % 2 ? 10 : -10}deg)`;
      setTimeout(() => {
        eggImage.style.transform = '';
      }, 200);

      if (clickCount >= CLICKS_NEEDED) {
        eggImage.removeEventListener('click', onClick);
        setTimeout(showHatchingStage, 300);
      }
    });
    // === Pet Type Selection ===
    let selectedPetType = null;
    let petTypesData = {};

    async function loadPetTypes() {
      try {
        const response = await fetch('/api/pet-types/');
        if (response.ok) {
          const typesArray = await response.json();

          // Map the array into an object using the 'id' (e.g., "cherry") as the key
          petTypesData = {};
          typesArray.forEach(t => {
            petTypesData[t.id] = t;
          });

          // 1. Pre-select the random character immediately upon loading the data
          selectedPetType = getRandomPetType();

          // 2. Set the egg image to match the chosen character's specific egg (Level 1)
          const eggImgEl = document.getElementById('eggImage');
          if (eggImgEl && petTypesData[selectedPetType] && petTypesData[selectedPetType].evolution_chain) {
            eggImgEl.src = petTypesData[selectedPetType].evolution_chain["1"].image;
          }
        }
      } catch (e) {
        console.error('Failed to load pet types:', e);
      }
    }

    function getRandomPetType() {
      // Now this correctly grabs ['cherry', 'cyan', 'dark_blue', 'green', 'purple']
      const types = Object.keys(petTypesData);
      if (types.length === 0) return 'cherry';
      const rand = types[Math.floor(Math.random() * types.length)];
      return rand;
    }

    function getPetTypeImage(petTypeId) {
      if (!petTypesData || !petTypesData[petTypeId] || !petTypesData[petTypeId].evolution_chain) {
        return '/static/images/characters/main_egg.png';
      }
      return petTypesData[petTypeId].evolution_chain["2"].image;
    }
    // === Hatching Stage ===
    function showHatchingStage() {
      showStage('hatchingStage');

      const petImage = getPetTypeImage(selectedPetType);

      const revealImgEl = document.getElementById('characterReveal');
      if (revealImgEl) {
        revealImgEl.src = petImage;
      }

      for (let i = 0; i < 10; i++) {
        setTimeout(() => {
          const x = Math.random() * window.innerWidth;
          const y = Math.random() * window.innerHeight;
          createSparkle(x, y);
        }, i * 200);
      }

      setTimeout(() => showStage('nameStage'), 3000);
    }
    // === Name Form ===
    document.getElementById('nameForm').addEventListener('submit', async (e) => {
      e.preventDefault();

      const petName = document.getElementById('petName').value.trim();
      const submitBtn = document.getElementById('submitBtn');
      const errorDiv = document.getElementById('nameError');

      if (!petName) return;

      const token = getToken();
      if (!token) {
        window.location.href = '/login';
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = 'Creating...';
      errorDiv.style.display = 'none';

      try {
        const response = await fetch('/api/pet/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            name: petName,
            pet_type: selectedPetType.toString() || 'blue'
          })
        });
        console.log(selectedPetType.toString() || 'blue' )
        if (!response.ok) {
          const data = await response.json();

          if (response.status === 400 && data.detail === 'User already has a pet') {
            window.location.href = '/home';
            return;
          }

          throw new Error(data.detail || 'Failed to create pet');
        }

        window.location.href = '/home';

      } catch (err) {
        errorDiv.textContent = err.message;
        errorDiv.style.display = 'block';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Start Journey!';
      }
    });

    loadPetTypes();
