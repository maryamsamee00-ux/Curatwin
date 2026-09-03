function renderLanding() {
    return `
    <div class="min-h-screen bg-gradient-to-br from-teal-50 via-white to-plum-50 flex flex-col items-center justify-center px-6 py-12">
        <div class="text-center mb-8">
            <div class="w-20 h-20 bg-gradient-to-br from-teal-500 to-plum-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                <svg class="w-10 h-10 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
            </div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">CuraTwin</h1>
            <p class="text-gray-500 text-lg">Your Personal Wellness Companion</p>
        </div>

        <div class="card max-w-sm w-full">
            <div class="space-y-4 text-center">
                <div class="flex items-center gap-3 text-left p-3 bg-teal-50 rounded-xl">
                    <div class="w-10 h-10 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                    </div>
                    <div><p class="text-sm font-semibold text-gray-800">Wellness Tracking</p><p class="text-xs text-gray-500">Monitor your daily wellness</p></div>
                </div>
                <div class="flex items-center gap-3 text-left p-3 bg-plum-50 rounded-xl">
                    <div class="w-10 h-10 bg-plum-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-plum-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>
                    </div>
                    <div><p class="text-sm font-semibold text-gray-800">Stress Management</p><p class="text-xs text-gray-500">AI-powered personal insights</p></div>
                </div>
                <div class="flex items-center gap-3 text-left p-3 bg-warm-50 rounded-xl">
                    <div class="w-10 h-10 bg-warm-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-amber-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    </div>
                    <div><p class="text-sm font-semibold text-gray-800">Private & Secure</p><p class="text-xs text-gray-500">You control your data</p></div>
                </div>
            </div>
        </div>

        <div class="mt-8 space-y-3 w-full max-w-sm">
            <button onclick="navigate('register')" class="btn-primary">Get Started</button>
            <button onclick="navigate('login')" class="btn-secondary w-full text-center block">I already have an account</button>
        </div>
        <p class="text-xs text-gray-400 mt-6 text-center">A wellness research project. Not a medical device.</p>
    </div>`;
}
