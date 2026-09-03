const routes = {
    '': { render: renderLanding, auth: false },
    'register': { render: renderRegister, auth: false },
    'login': { render: renderLogin, auth: false },
    'dashboard': { render: renderDashboard, auth: true },
    'insights': { render: renderInsights, auth: true },
    'cycle': { render: renderCycle, auth: true },
    'coping': { render: renderCoping, auth: true },
    'checkin': { render: renderCheckin, auth: true },
    'profile': { render: renderProfile, auth: true },
    'consent': { render: renderConsent, auth: true },
    'emergency': { render: renderEmergency, auth: true },
};

function navigate(page) {
    window.location.hash = '#/' + page;
}

function getRoute() {
    const hash = window.location.hash.replace('#/', '') || '';
    return hash;
}

async function handleRoute() {
    const route = getRoute();
    const config = routes[route] || routes[''];

    if (config.auth && !Auth.isLoggedIn()) {
        window.location.hash = '#/login';
        return;
    }

    if (!config.auth && Auth.isLoggedIn() && (route === '' || route === 'register' || route === 'login')) {
        navigate('dashboard');
        return;
    }

    const app = document.getElementById('app');
    app.innerHTML = '<div class="text-center py-20 text-gray-400">Loading...</div>';

    try {
        const html = await config.render();
        if (typeof html === 'string') {
            app.innerHTML = html;
        }
    } catch (err) {
        app.innerHTML = `<div class="px-5 py-6"><div class="card"><p class="text-red-500">${err.message}</p><a href="#/" class="text-teal-600 text-sm mt-2 inline-block">Go home</a></div></div>`;
    }
}

window.addEventListener('hashchange', handleRoute);
window.addEventListener('load', handleRoute);
