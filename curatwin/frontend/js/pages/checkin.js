function renderCheckin() {
    return `
    <div class="px-5 py-6">
        <a href="#/dashboard" class="text-teal-600 text-sm font-medium mb-4 inline-block">&larr; Back</a>
        <h1 class="text-xl font-bold text-gray-900 mb-1">Daily Check-in</h1>
        <p class="text-sm text-gray-500 mb-4">A private moment to reflect on how you feel</p>

        <form onsubmit="handleCheckin(event)" class="space-y-5">
            <div class="card">
                <label class="label">How is your mood right now?</label>
                <div class="flex justify-between text-xs text-gray-400 mb-1"><span>Low</span><span>Great</span></div>
                <input type="range" min="0" max="1" step="0.1" value="0.5" name="mood" class="range-slider" id="mood-slider" oninput="document.getElementById('mood-display').textContent=Math.round(this.value*100)+'%'">
                <p class="text-center text-sm font-semibold text-teal-600 mt-1" id="mood-display">50%</p>
            </div>

            <div class="card">
                <label class="label">Perceived stress level?</label>
                <div class="flex justify-between text-xs text-gray-400 mb-1"><span>Calm</span><span>Very stressed</span></div>
                <input type="range" min="0" max="1" step="0.1" value="0.5" name="perceived_stress" class="range-slider" oninput="document.getElementById('stress-display').textContent=Math.round(this.value*100)+'%'">
                <p class="text-center text-sm font-semibold text-amber-600 mt-1" id="stress-display">50%</p>
            </div>

            <div class="card">
                <label class="label">Sleep quality last night?</label>
                <div class="flex justify-between text-xs text-gray-400 mb-1"><span>Poor</span><span>Excellent</span></div>
                <input type="range" min="0" max="1" step="0.1" value="0.5" name="sleep_quality" class="range-slider" oninput="document.getElementById('sleep-display').textContent=Math.round(this.value*100)+'%'">
                <p class="text-center text-sm font-semibold text-plum-600 mt-1" id="sleep-display">50%</p>
            </div>

            <div class="card">
                <label class="label">Energy level?</label>
                <div class="flex justify-between text-xs text-gray-400 mb-1"><span>Exhausted</span><span>Energetic</span></div>
                <input type="range" min="0" max="1" step="0.1" value="0.5" name="energy_level" class="range-slider" oninput="document.getElementById('energy-display').textContent=Math.round(this.value*100)+'%'">
                <p class="text-center text-sm font-semibold text-green-600 mt-1" id="energy-display">50%</p>
            </div>

            <div class="card">
                <label class="label">Physical symptoms (optional)</label>
                <input type="text" name="symptoms" class="input-field" placeholder="e.g., headache, fatigue">
            </div>

            <div class="card">
                <label class="label">Menstrual symptoms (optional)</label>
                <input type="text" name="menstrual_symptoms" class="input-field" placeholder="e.g., cramps, bloating">
            </div>

            <div class="card">
                <label class="label">Notes (optional)</label>
                <textarea name="notes" class="input-field" rows="3" placeholder="Anything on your mind..."></textarea>
            </div>

            <button type="submit" class="btn-primary">Save Check-in</button>
        </form>
    </div>
    ${renderNav('dashboard')}`;
}

async function handleCheckin(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
        await API.post('/api/mood/checkin', {
            mood: parseFloat(form.get('mood')),
            perceived_stress: parseFloat(form.get('perceived_stress')),
            sleep_quality: parseFloat(form.get('sleep_quality')),
            energy_level: parseFloat(form.get('energy_level')),
            symptoms: form.get('symptoms') || '',
            menstrual_symptoms: form.get('menstrual_symptoms') || '',
            notes: form.get('notes') || '',
        });
        showToast('Check-in saved! Thank you for reflecting.', 'success');
        navigate('dashboard');
    } catch (err) {
        showToast(err.message, 'error');
    }
}
