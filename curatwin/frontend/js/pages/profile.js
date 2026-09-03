async function renderProfile() {
    const app = document.getElementById('app');
    app.innerHTML = `<div class="px-5 py-6">${renderNav('profile')}<div class="text-center py-12 text-gray-400">Loading...</div></div>`;

    try {
        const profile = await API.get('/api/users/profile').catch(() => null);

        app.innerHTML = `
        <div class="px-5 py-6">
            <div class="flex items-center justify-between mb-4">
                <h1 class="text-xl font-bold text-gray-900">Profile</h1>
                <button onclick="Auth.logout()" class="text-red-500 text-sm font-medium">Log out</button>
            </div>

            <div class="card">
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-14 h-14 bg-gradient-to-br from-teal-400 to-plum-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
                        ${(Auth.user?.name || 'U')[0].toUpperCase()}
                    </div>
                    <div>
                        <p class="font-semibold text-gray-800">${Auth.user?.name || ''}</p>
                        <p class="text-sm text-gray-500">${Auth.user?.email || ''}</p>
                    </div>
                </div>
            </div>

            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Wellness Profile</h3>
                <form onsubmit="handleProfileUpdate(event)" class="space-y-3">
                    <div><label class="label">Age Range</label>
                        <select name="age_range" class="input-field" id="prof-age">
                            <option value="18-20" ${profile?.age_range === '18-20' ? 'selected' : ''}>18-20</option>
                            <option value="21-24" ${profile?.age_range === '21-24' ? 'selected' : ''}>21-24</option>
                            <option value="25+" ${profile?.age_range === '25+' ? 'selected' : ''}>25+</option>
                        </select>
                    </div>
                    <div><label class="label">University</label>
                        <input type="text" name="university" class="input-field" value="${profile?.university || ''}" placeholder="Your university">
                    </div>
                    <input type="hidden" name="onboarding_complete" value="1">
                    <button type="submit" class="btn-primary">Save Profile</button>
                </form>
            </div>

            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Privacy & Consent</h3>
                <a href="#/consent" class="block p-3 bg-gray-50 rounded-xl mb-2">
                    <p class="text-sm font-semibold text-gray-700">Consent Management</p>
                    <p class="text-xs text-gray-500">Control what information is shared</p>
                </a>
                <a href="#/emergency" class="block p-3 bg-red-50 rounded-xl">
                    <p class="text-sm font-semibold text-red-700">Emergency Contacts</p>
                    <p class="text-xs text-gray-500">Manage guardian alerts</p>
                </a>
            </div>

            <p class="text-xs text-gray-400 text-center mt-4">CuraTwin is a wellness research project, not a medical device. All predictions are AI estimates.</p>
        </div>
        ${renderNav('profile')}`;
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p></div></div>${renderNav('profile')}`;
    }
}

async function handleProfileUpdate(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
        await API.put('/api/users/profile', {
            age_range: form.get('age_range'),
            university: form.get('university') || '',
            onboarding_complete: 1,
        });
        showToast('Profile updated!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    }
}
