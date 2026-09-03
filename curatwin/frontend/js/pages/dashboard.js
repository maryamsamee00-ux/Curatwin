async function renderDashboard() {
    const app = document.getElementById('app');
    app.innerHTML = `<div class="px-5 py-6">${renderNav('dashboard')}<div class="text-center py-12"><div class="animate-pulse text-gray-400">Loading your wellness data...</div></div></div>`;

    try {
        const [twinData, stressData] = await Promise.all([
            API.get('/api/digital-twin/state').catch(() => null),
            API.get('/api/stress/current').catch(() => null),
        ]);

        const twin = twinData?.digital_twin;
        const affective = twinData?.affective_state;
        const stress = stressData;

        let profile = null;
        try { profile = await API.get('/api/users/profile'); } catch(e) {}

        app.innerHTML = `
        <div class="px-5 py-6">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h1 class="text-xl font-bold text-gray-900">Hello, ${Auth.user?.name?.split(' ')[0] || 'Student'}</h1>
                    <p class="text-sm text-gray-500">Your wellness snapshot</p>
                </div>
                <a href="#/checkin" class="w-10 h-10 bg-teal-100 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                </a>
            </div>

            ${!profile?.onboarding_complete ? `
            <div class="card bg-gradient-to-r from-teal-50 to-plum-50 border border-teal-100 mb-4">
                <p class="text-sm font-medium text-gray-800 mb-2">Complete your wellness profile</p>
                <a href="#/profile" class="text-teal-600 text-sm font-semibold">Set up profile &rarr;</a>
            </div>` : ''}

            <div class="card">
                <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Digital Twin</h2>
                ${renderDigitalTwin(twin)}
            </div>

            <div class="grid grid-cols-2 gap-3 mb-4">
                <div class="card text-center !mb-0">
                    <p class="text-xs text-gray-500 uppercase">Stress</p>
                    <p class="text-lg font-bold text-gray-800">${stress?.stress_level ? stress.stress_level.charAt(0).toUpperCase() + stress.stress_level.slice(1) : '—'}</p>
                    ${stress?.confidence ? `<p class="text-xs text-gray-400">${Math.round(stress.confidence * 100)}% conf.</p>` : ''}
                </div>
                <div class="card text-center !mb-0">
                    <p class="text-xs text-gray-500 uppercase">Mood</p>
                    <p class="text-lg font-bold text-gray-800">${affective?.mood_score ? Math.round(affective.mood_score) + '%' : '—'}</p>
                    <p class="text-xs text-gray-400">${affective?.mood_trend || 'No data'}</p>
                </div>
            </div>

            ${affective ? `
            <div class="card">
                <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Affective State</h2>
                <p class="text-sm text-gray-700">${affective.recommendation}</p>
                <div class="mt-3 grid grid-cols-2 gap-2">
                    <div class="bg-gray-50 rounded-lg p-2 text-center"><p class="text-xs text-gray-500">Energy</p><p class="font-semibold text-sm">${affective.energy_score ? Math.round(affective.energy_score) + '%' : '—'}</p></div>
                    <div class="bg-gray-50 rounded-lg p-2 text-center"><p class="text-xs text-gray-500">Sleep</p><p class="font-semibold text-sm">${affective.sleep_score ? Math.round(affective.sleep_score) + '%' : '—'}</p></div>
                </div>
                <p class="text-xs text-gray-400 mt-2 italic">${affective.disclaimer}</p>
            </div>` : ''}

            <div class="card">
                <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Quick Actions</h2>
                <div class="grid grid-cols-2 gap-3">
                    <a href="#/checkin" class="bg-teal-50 rounded-xl p-3 text-center block"><p class="text-sm font-semibold text-teal-700">Daily Check-in</p><p class="text-xs text-gray-500">Record your mood</p></a>
                    <a href="#/coping" class="bg-plum-50 rounded-xl p-3 text-center block"><p class="text-sm font-semibold text-plum-700">Coping Tools</p><p class="text-xs text-gray-500">Get support</p></a>
                    <a href="#/cycle" class="bg-warm-50 rounded-xl p-3 text-center block"><p class="text-sm font-semibold text-amber-700">Cycle Track</p><p class="text-xs text-gray-500">Personal insights</p></a>
                    <a href="#/emergency" class="bg-red-50 rounded-xl p-3 text-center block"><p class="text-sm font-semibold text-red-700">Emergency</p><p class="text-xs text-gray-500">Alert guardian</p></a>
                </div>
            </div>

            <div class="card">
                <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Simulate Telemetry</h2>
                <p class="text-xs text-gray-500 mb-3">Demo mode: submit simulated sensor data to test the stress classifier.</p>
                <div class="space-y-3">
                    <div><label class="text-xs text-gray-500">PPG HRV: <span id="hrv-val">50</span></label><input type="range" min="10" max="100" value="50" class="range-slider w-full" id="sim-hrv" oninput="document.getElementById('hrv-val').textContent=this.value"></div>
                    <div><label class="text-xs text-gray-500">GSR: <span id="gsr-val">5</span></label><input type="range" min="1" max="10" value="5" step="0.5" class="range-slider w-full" id="sim-gsr" oninput="document.getElementById('gsr-val').textContent=this.value"></div>
                    <div><label class="text-xs text-gray-500">Skin Temp: <span id="temp-val">36.5</span></label><input type="range" min="35" max="38" value="36.5" step="0.1" class="range-slider w-full" id="sim-temp" oninput="document.getElementById('temp-val').textContent=this.value"></div>
                    <button onclick="simulateTelemetry()" class="btn-primary">Send & Predict</button>
                </div>
            </div>
        </div>
        ${renderNav('dashboard')}`;
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p></div></div>${renderNav('dashboard')}`;
    }
}

async function simulateTelemetry() {
    try {
        const data = {
            ppg_hrv: parseFloat(document.getElementById('sim-hrv').value),
            gsr_amplitude: parseFloat(document.getElementById('sim-gsr').value),
            skin_temp: parseFloat(document.getElementById('sim-temp').value),
            imu_activity: 0.3,
            self_report_stress: 0.5
        };
        await API.post('/api/wellness/telemetry', data);
        const pred = await API.post('/api/stress/predict', data);
        showToast(`Stress: ${pred.stress_level} (${Math.round(pred.confidence * 100)}% confidence)`, pred.stress_level === 'low' ? 'success' : 'info');
        renderDashboard();
    } catch (err) {
        showToast(err.message, 'error');
    }
}
