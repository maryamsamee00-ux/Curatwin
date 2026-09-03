async function renderInsights() {
    const app = document.getElementById('app');
    app.innerHTML = `<div class="px-5 py-6">${renderNav('insights')}<div class="text-center py-12 text-gray-400">Loading insights...</div></div>`;

    try {
        const [overview, stressTrend, moodTrend] = await Promise.all([
            API.get('/api/insights/overview').catch(() => ({ has_data: false })),
            API.get('/api/insights/stress-trend').catch(() => ({ trend: [] })),
            API.get('/api/insights/mood-trend').catch(() => ({ trend: [] })),
        ]);

        app.innerHTML = `
        <div class="px-5 py-6">
            <h1 class="text-xl font-bold text-gray-900 mb-1">Wellness Insights</h1>
            <p class="text-sm text-gray-500 mb-4">Your personalized trends and patterns</p>

            ${!overview.has_data ? `
            <div class="empty-state card">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="w-12 h-12 mx-auto mb-3 text-gray-300"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                <p class="text-gray-500">Your personalized insights will appear as data is collected.</p>
                <a href="#/checkin" class="text-teal-600 font-semibold text-sm mt-3 inline-block">Complete a check-in</a>
            </div>` : `

            ${overview.stress_distribution ? `
            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Stress Distribution (7 days)</h3>
                <div style="height:200px"><canvas id="stress-doughnut"></canvas></div>
                <p class="text-sm text-gray-600 mt-2">Dominant: <span class="font-semibold">${overview.dominant_stress || 'N/A'}</span></p>
            </div>` : ''}

            ${moodTrend.trend.length > 0 ? `
            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Mood Trend (30 days)</h3>
                <div style="height:200px"><canvas id="mood-chart"></canvas></div>
            </div>` : ''}

            ${stressTrend.trend.length > 0 ? `
            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Stress Timeline</h3>
                <div style="height:200px"><canvas id="stress-chart"></canvas></div>
            </div>` : ''}

            <div class="card">
                <h3 class="text-sm font-semibold text-gray-500 uppercase mb-3">Weekly Summary</h3>
                <div class="grid grid-cols-2 gap-3">
                    <div class="bg-teal-50 rounded-xl p-3 text-center">
                        <p class="text-xs text-gray-500">Avg Mood</p>
                        <p class="text-xl font-bold text-teal-700">${overview.avg_mood ?? '—'}%</p>
                    </div>
                    <div class="bg-plum-50 rounded-xl p-3 text-center">
                        <p class="text-xs text-gray-500">Avg Sleep</p>
                        <p class="text-xl font-bold text-plum-700">${overview.avg_sleep ?? '—'}%</p>
                    </div>
                    <div class="bg-warm-50 rounded-xl p-3 text-center">
                        <p class="text-xs text-gray-500">Avg Energy</p>
                        <p class="text-xl font-bold text-amber-700">${overview.avg_energy ?? '—'}%</p>
                    </div>
                    <div class="bg-gray-50 rounded-xl p-3 text-center">
                        <p class="text-xs text-gray-500">Avg HRV</p>
                        <p class="text-xl font-bold text-gray-700">${overview.avg_hrv ?? '—'}</p>
                    </div>
                </div>
            </div>`}
        </div>
        ${renderNav('insights')}`;

        // Render charts after DOM is ready
        setTimeout(() => {
            if (overview.stress_distribution) {
                const sd = overview.stress_distribution;
                renderDoughnutChart('stress-doughnut', ['Low', 'Moderate', 'High'], [sd.low||0, sd.moderate||0, sd.high||0], ['#0d9488', '#f59e0b', '#ef4444']);
            }
            if (moodTrend.trend.length > 0) {
                renderLineChart('mood-chart',
                    moodTrend.trend.map(t => t.date?.slice(5,10) || ''),
                    [
                        { label: 'Mood', data: moodTrend.trend.map(t => t.mood * 100), borderColor: '#0d9488', backgroundColor: 'rgba(13,148,136,0.1)', fill: true },
                        { label: 'Sleep', data: moodTrend.trend.map(t => t.sleep * 100), borderColor: '#7c3aed', borderDash: [5,5] },
                    ],
                    'Mood & Sleep Trend'
                );
            }
            if (stressTrend.trend.length > 0) {
                const stressMap = { low: 25, moderate: 55, high: 85 };
                renderLineChart('stress-chart',
                    stressTrend.trend.map((t, i) => i + 1),
                    [{ label: 'Stress Level', data: stressTrend.trend.map(t => stressMap[t.stress_level] || 50), borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', fill: true }],
                    'Stress Over Time'
                );
            }
        }, 100);
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p></div></div>${renderNav('insights')}`;
    }
}
