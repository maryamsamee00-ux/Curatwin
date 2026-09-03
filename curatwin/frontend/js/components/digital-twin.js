function renderDigitalTwin(twin) {
    if (!twin) return `<div class="empty-state"><p>Loading your wellness twin...</p></div>`;

    const score = twin.wellness_score || 50;
    const state = twin.state || 'moderate';
    const stateLabels = { well: 'Feeling Well', moderate: 'Moderate', stressed: 'Under Stress' };
    const stateColors = { well: '#0d9488', moderate: '#f59e0b', stressed: '#ef4444' };
    const stateEmojis = { well: '🌿', moderate: '🌤', stressed: '⚡' };

    return `
    <div class="text-center mb-4">
        <div class="twin-ring ${state}" style="--ring-percent: ${score}%">
            <div class="text-center">
                <div class="text-3xl mb-1">${stateEmojis[state]}</div>
                <div class="text-2xl font-bold" style="color: ${stateColors[state]}">${Math.round(score)}</div>
                <div class="text-xs text-gray-500">/100</div>
            </div>
        </div>
        <h3 class="mt-3 text-lg font-semibold text-gray-800">${stateLabels[state]}</h3>
        <span class="chip chip-${state === 'well' ? 'low' : state}">${twin.stress_category} Stress</span>
        <p class="text-xs text-gray-400 mt-2 italic">${twin.disclaimer}</p>
    </div>`;
}
