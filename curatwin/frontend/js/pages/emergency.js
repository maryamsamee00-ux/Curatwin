async function renderEmergency() {
    const app = document.getElementById('app');
    app.innerHTML = `<div class="px-5 py-6"><div class="text-center py-12 text-gray-400">Loading...</div></div>`;

    try {
        const [guardians, alertHistory] = await Promise.all([
            API.get('/api/guardians/').catch(() => []),
            API.get('/api/alerts/history').catch(() => ({ alerts: [] })),
        ]);

        const verified = guardians.filter(g => g.verification_status === 'verified');

        app.innerHTML = `
        <div class="px-5 py-6">
            <a href="#/profile" class="text-teal-600 text-sm font-medium mb-4 inline-block">&larr; Back</a>
            <h1 class="text-xl font-bold text-gray-900 mb-1">Emergency Support</h1>
            <p class="text-sm text-gray-500 mb-4">Alert your trusted contacts when needed</p>

            <div class="card border-2 border-red-200 bg-red-50">
                <div class="text-center">
                    <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-3">
                        <svg class="w-8 h-8 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    </div>
                    <h3 class="text-lg font-bold text-red-800 mb-2">Need Help Now?</h3>
                    <p class="text-sm text-gray-600 mb-4">This will alert your verified guardians with only the information you have consented to share.</p>

                    ${verified.length === 0 ? `
                    <p class="text-sm text-red-600 font-medium">No verified guardians found.</p>
                    <a href="#/consent" class="text-teal-600 font-semibold text-sm mt-2 inline-block">Add a guardian first &rarr;</a>
                    ` : `
                    <button onclick="triggerEmergency()" class="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-xl w-full transition">
                        Send Emergency Alert
                    </button>
                    <p class="text-xs text-gray-500 mt-2">Guardians notified: ${verified.map(g => g.guardian_name).join(', ')}</p>
                    `}
                </div>
            </div>

            <div class="card mt-4">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Important Reminders</h3>
                <ul class="space-y-2 text-sm text-gray-600">
                    <li class="flex items-start gap-2"><span class="text-teal-500 mt-0.5">•</span> Only consent-granted information is shared</li>
                    <li class="flex items-start gap-2"><span class="text-teal-500 mt-0.5">•</span> You can revoke consent at any time</li>
                    <li class="flex items-start gap-2"><span class="text-teal-500 mt-0.5">•</span> This is not a substitute for emergency services</li>
                    <li class="flex items-start gap-2"><span class="text-teal-500 mt-0.5">•</span> For immediate danger, contact local emergency services</li>
                </ul>
            </div>

            ${alertHistory.alerts?.length > 0 ? `
            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Alert History</h3>
                ${alertHistory.alerts.map(a => `
                    <div class="border-b border-gray-100 py-2 last:border-0">
                        <p class="text-sm font-medium text-gray-700">${a.alert_type}</p>
                        <p class="text-xs text-gray-500">${a.created_at?.slice(0,16).replace('T', ' ')} · ${a.status}</p>
                    </div>
                `).join('')}
            </div>` : ''}
        </div>
        ${renderNav('profile')}`;
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p></div></div>${renderNav('profile')}`;
    }
}

async function triggerEmergency() {
    if (!confirm('Send emergency alert to your verified guardians? Only consent-granted information will be shared.')) return;
    try {
        const result = await API.post('/api/alerts/emergency');
        showToast(result.message || 'Emergency alerts sent.', 'success');
        renderEmergency();
    } catch (err) { showToast(err.message, 'error'); }
}
