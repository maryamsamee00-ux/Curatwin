async function renderConsent() {
    const app = document.getElementById('app');
    app.innerHTML = `<div class="px-5 py-6"><div class="text-center py-12 text-gray-400">Loading...</div></div>`;

    try {
        const [guardians, consents] = await Promise.all([
            API.get('/api/guardians/').catch(() => []),
            API.get('/api/consent/').catch(() => []),
        ]);

        app.innerHTML = `
        <div class="px-5 py-6">
            <a href="#/profile" class="text-teal-600 text-sm font-medium mb-4 inline-block">&larr; Back</a>
            <h1 class="text-xl font-bold text-gray-900 mb-1">Consent & Guardians</h1>
            <p class="text-sm text-gray-500 mb-4">You control who can see what</p>

            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Add Guardian</h3>
                <form onsubmit="handleAddGuardian(event)" class="space-y-3">
                    <div><label class="label">Guardian Name</label><input type="text" name="guardian_name" class="input-field" required></div>
                    <div><label class="label">Contact (email or phone)</label><input type="text" name="guardian_contact" class="input-field" required></div>
                    <div><label class="label">Relationship</label>
                        <select name="relationship" class="input-field">
                            <option value="parent">Parent</option>
                            <option value="sibling">Sibling</option>
                            <option value="spouse">Spouse</option>
                            <option value="friend">Trusted Friend</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary">Add Guardian</button>
                </form>
            </div>

            ${guardians.length > 0 ? `
            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Your Guardians</h3>
                ${guardians.map(g => `
                    <div class="border-b border-gray-100 py-3 last:border-0">
                        <div class="flex justify-between items-start">
                            <div>
                                <p class="text-sm font-semibold text-gray-800">${g.guardian_name}</p>
                                <p class="text-xs text-gray-500">${g.relationship} · ${g.guardian_contact}</p>
                                <span class="chip ${g.verification_status === 'verified' ? 'chip-low' : 'chip-moderate'} mt-1">${g.verification_status}</span>
                            </div>
                            <button onclick="removeGuardian(${g.id})" class="text-red-400 text-xs">Remove</button>
                        </div>
                        ${g.verification_status === 'pending' ? `
                        <div class="mt-2 flex gap-2">
                            <input type="text" id="code-${g.id}" class="input-field text-sm !py-2" placeholder="Verification code" maxlength="6">
                            <button onclick="verifyGuardian(${g.id})" class="btn-secondary text-xs !py-2">Verify</button>
                        </div>
                        <p class="text-xs text-gray-400 mt-1">Code: ${g.verification_code} (demo: shown for testing)</p>
                        ` : ''}

                        ${g.verification_status === 'verified' ? `
                        <div class="mt-3 space-y-2">
                            <p class="text-xs font-semibold text-gray-500">Permissions:</p>
                            ${['emergency_location', 'stress_level', 'wellness_summary', 'cycle_info'].map(perm => {
                                const c = consents.find(c => c.guardian_id === g.id && c.permission_type === perm);
                                return `
                                <label class="flex items-center gap-2 text-sm text-gray-700">
                                    <input type="checkbox" ${c?.enabled ? 'checked' : ''} onchange="toggleConsent(${g.id}, '${perm}', this.checked, ${c?.id || 0})">
                                    ${perm.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                </label>`;
                            }).join('')}
                        </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>` : `
            <div class="empty-state card">
                <p class="text-gray-500">No guardians added yet. Add a trusted person for emergency alerts.</p>
            </div>`}
        </div>
        ${renderNav('profile')}`;
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p></div></div>${renderNav('profile')}`;
    }
}

async function handleAddGuardian(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
        await API.post('/api/guardians/', {
            guardian_name: form.get('guardian_name'),
            guardian_contact: form.get('guardian_contact'),
            relationship: form.get('relationship'),
        });
        showToast('Guardian added!', 'success');
        renderConsent();
    } catch (err) { showToast(err.message, 'error'); }
}

async function verifyGuardian(id) {
    const code = document.getElementById(`code-${id}`).value;
    try {
        await API.post(`/api/guardians/${id}/verify`, { verification_code: code });
        showToast('Guardian verified!', 'success');
        renderConsent();
    } catch (err) { showToast(err.message, 'error'); }
}

async function removeGuardian(id) {
    try {
        await API.del(`/api/guardians/${id}`);
        showToast('Guardian removed.', 'info');
        renderConsent();
    } catch (err) { showToast(err.message, 'error'); }
}

async function toggleConsent(guardianId, permType, enabled, consentId) {
    try {
        if (consentId) {
            await API.put(`/api/consent/${consentId}`, { enabled: enabled ? 1 : 0 });
        } else {
            await API.post('/api/consent/', { guardian_id: guardianId, permission_type: permType, enabled: enabled ? 1 : 0 });
        }
        showToast(enabled ? 'Permission granted.' : 'Permission revoked.', 'info');
    } catch (err) { showToast(err.message, 'error'); renderConsent(); }
}
