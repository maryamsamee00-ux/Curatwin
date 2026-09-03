async function renderCycle() {
    const app = document.getElementById('app');
    app.innerHTML = `<div class="px-5 py-6">${renderNav('cycle')}<div class="text-center py-12 text-gray-400">Loading...</div></div>`;

    try {
        const [current, records] = await Promise.all([
            API.get('/api/cycle/current').catch(() => ({})),
            API.get('/api/cycle/records').catch(() => []),
        ]);

        app.innerHTML = `
        <div class="px-5 py-6">
            <h1 class="text-xl font-bold text-gray-900 mb-1">Cycle Tracking</h1>
            <p class="text-sm text-gray-500 mb-4">Personal cycle insights</p>

            ${current.current_phase ? `
            <div class="card bg-gradient-to-r from-pink-50 to-purple-50">
                <div class="flex items-center gap-3 mb-3">
                    <div class="w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center">
                        <svg class="w-6 h-6 text-pink-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                    </div>
                    <div>
                        <p class="text-lg font-semibold text-gray-800">${current.current_phase.charAt(0).toUpperCase() + current.current_phase.slice(1)} Phase</p>
                        <p class="text-xs text-gray-500">Started: ${current.cycle_start?.slice(0,10) || 'N/A'}</p>
                    </div>
                </div>
                ${current.insights ? `
                <div class="bg-white rounded-xl p-3 mt-2">
                    <p class="text-sm font-medium text-gray-700 mb-1">${current.insights.description}</p>
                    <p class="text-xs text-gray-500">Energy: ${current.insights.energy}</p>
                    <p class="text-xs text-teal-600 mt-1">${current.insights.study_suggestion}</p>
                    ${current.insights.mood_note ? `<p class="text-xs text-gray-400 mt-1 italic">${current.insights.mood_note}</p>` : ''}
                </div>` : ''}
            </div>` : `
            <div class="empty-state card">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="w-12 h-12 mx-auto mb-3 text-gray-300"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                <p class="text-gray-500">Add your cycle information to begin personal cycle tracking.</p>
            </div>`}

            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Add Cycle Record</h3>
                <form onsubmit="handleAddCycle(event)" class="space-y-3">
                    <div><label class="label">Cycle Start Date</label><input type="date" name="cycle_start" class="input-field" required></div>
                    <div><label class="label">Cycle Length (days)</label><input type="number" name="cycle_length" class="input-field" value="28" min="20" max="45"></div>
                    <div><label class="label">Symptoms (optional)</label><textarea name="symptoms" class="input-field" rows="2" placeholder="e.g., cramps, headache"></textarea></div>
                    <div><label class="label">Mood Observations (optional)</label><textarea name="mood_observations" class="input-field" rows="2" placeholder="How you've been feeling"></textarea></div>
                    <button type="submit" class="btn-primary">Save Record</button>
                </form>
            </div>

            ${records.length > 0 ? `
            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">History</h3>
                ${records.map(r => `
                    <div class="border-b border-gray-100 py-3 last:border-0">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="text-sm font-medium text-gray-800">${r.cycle_start?.slice(0,10)} — ${r.estimated_phase}</p>
                                <p class="text-xs text-gray-500">${r.cycle_length} day cycle</p>
                            </div>
                            <span class="chip chip-${r.estimated_phase === 'menstrual' ? 'high' : r.estimated_phase === 'follicular' ? 'low' : 'moderate'}">${r.estimated_phase}</span>
                        </div>
                        ${r.symptoms ? `<p class="text-xs text-gray-500 mt-1">${r.symptoms}</p>` : ''}
                    </div>
                `).join('')}
            </div>` : ''}
        </div>
        ${renderNav('cycle')}`;
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p></div></div>${renderNav('cycle')}`;
    }
}

async function handleAddCycle(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
        await API.post('/api/cycle/records', {
            cycle_start: form.get('cycle_start'),
            cycle_length: parseInt(form.get('cycle_length')),
            symptoms: form.get('symptoms') || '',
            mood_observations: form.get('mood_observations') || '',
        });
        showToast('Cycle record saved!', 'success');
        renderCycle();
    } catch (err) {
        showToast(err.message, 'error');
    }
}
