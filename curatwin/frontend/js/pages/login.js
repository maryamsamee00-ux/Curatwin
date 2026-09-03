function renderLogin() {
    return `
    <div class="min-h-screen bg-gradient-to-br from-teal-50 via-white to-plum-50 px-6 py-8 flex flex-col justify-center">
        <h2 class="text-2xl font-bold text-gray-900 mb-1">Welcome Back</h2>
        <p class="text-gray-500 mb-6">Continue your wellness journey</p>

        <form id="login-form" class="space-y-4" onsubmit="handleLogin(event)">
            <div><label class="label">Email</label><input type="email" name="email" class="input-field" placeholder="you@university.edu" required></div>
            <div><label class="label">Password</label><input type="password" name="password" class="input-field" placeholder="Your password" required></div>
            <button type="submit" class="btn-primary" id="login-btn">Log In</button>
        </form>
        <p class="text-sm text-gray-500 text-center mt-4">New here? <a href="#/register" class="text-teal-600 font-medium">Create an account</a></p>
        <a href="#/" class="text-teal-600 text-sm font-medium mt-4 inline-block text-center">&larr; Back to home</a>
    </div>`;
}

async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById('login-btn');
    btn.disabled = true;
    btn.textContent = 'Logging in...';

    const form = new FormData(e.target);
    try {
        const data = await API.post('/api/auth/login', {
            email: form.get('email'),
            password: form.get('password')
        });
        API.setToken(data.access_token);
        Auth.setUser(data.user);
        showToast('Welcome back!', 'success');
        navigate('dashboard');
    } catch (err) {
        showToast(err.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Log In';
    }
}
