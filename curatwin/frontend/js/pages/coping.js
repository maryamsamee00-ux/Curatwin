async function renderCoping() {
    const app = document.getElementById('app');
    app.innerHTML = `<div class="px-5 py-6">${renderNav('coping')}<div class="text-center py-12 text-gray-400">Loading...</div></div>`;

    try {
        const [recs, library] = await Promise.all([
            API.get('/api/coping/recommendations').catch(() => ({ recommendations: [] })),
            API.get('/api/coping/library').catch(() => ({ categories: {} })),
        ]);

        const cats = library.categories || {};
        const catEmojis = { breathing:'🌬', mindfulness:'🧘', cbt_reframing:'💭', stretching:'🤸', study_breaks:'📚', sleep_hygiene:'😴', emotional_stabilization:'🛡', career_anxiety:'🎯', digital_safety:'🔒' };
        const catLabels = { breathing:'Breathing', mindfulness:'Mindfulness', cbt_reframing:'CBT Reframing', stretching:'Stretching', study_breaks:'Study Breaks', sleep_hygiene:'Sleep Hygiene', emotional_stabilization:'Emotional Support', career_anxiety:'Career Support', digital_safety:'Digital Safety' };

        app.innerHTML = `
        <div class="px-5 py-6">
            <h1 class="text-xl font-bold text-gray-900 mb-1">Coping Center</h1>
            <p class="text-sm text-gray-500 mb-4">Private support tools for you</p>

            ${recs.recommendations?.length > 0 ? `
            <div class="card bg-gradient-to-r from-teal-50 to-plum-50">
                <h3 class="text-sm font-semibold text-gray-600 mb-3">Recommended For You</h3>
                ${recs.recommendations.map(r => `
                    <div class="bg-white rounded-xl p-4 mb-3 last:mb-0 shadow-sm">
                        <div class="flex items-center gap-2 mb-2">
                            <span class="text-lg">${catEmojis[r.category] || '💡'}</span>
                            <span class="text-sm font-semibold text-gray-800">${r.title}</span>
                        </div>
                        <p class="text-sm text-gray-600 leading-relaxed">${r.recommendation}</p>
                    </div>
                `).join('')}
                <p class="text-xs text-gray-400 mt-2">Based on your current wellness state (${recs.stress_level || 'unknown'} stress)</p>
            </div>` : ''}

            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mt-6 mb-3">Browse All Categories</h3>
            <div class="space-y-2">
                ${Object.keys(cats).map(cat => `
                    <details class="card !mb-2 cursor-pointer">
                        <summary class="flex items-center gap-2 font-medium text-gray-800 list-none">
                            <span class="text-xl">${catEmojis[cat] || '💡'}</span>
                            <span>${catLabels[cat] || cat}</span>
                            <svg class="w-4 h-4 ml-auto text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </summary>
                        <div class="mt-3 space-y-3">
                            ${(cats[cat] || []).map(item => `
                                <div class="bg-gray-50 rounded-xl p-3">
                                    <p class="text-sm font-semibold text-gray-700 mb-1">${item.title}</p>
                                    <p class="text-xs text-gray-600 leading-relaxed">${item.content}</p>
                                </div>
                            `).join('')}
                        </div>
                    </details>
                `).join('')}
            </div>
        </div>
        ${renderNav('coping')}`;
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p></div></div>${renderNav('coping')}`;
    }
}
