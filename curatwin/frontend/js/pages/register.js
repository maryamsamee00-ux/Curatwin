function renderRegister() {
    return `
    <div class="min-h-screen bg-gradient-to-br from-teal-50 via-white to-plum-50 px-6 py-8">
        <a href="#/" class="text-teal-600 text-sm font-medium mb-6 inline-block">&larr; Back</a>
        <h2 class="text-2xl font-bold text-gray-900 mb-1">Create Account</h2>
        <p class="text-gray-500 mb-6">Begin your private wellness journey</p>

        <form id="register-form" class="space-y-4" onsubmit="handleRegister(event)">
            <div><label class="label">Name</label><input type="text" name="name" class="input-field" placeholder="Your name" required></div>
            <div><label class="label">Email</label><input type="email" name="email" class="input-field" placeholder="you@university.edu" required></div>
            <div><label class="label">Password</label><input type="password" name="password" class="input-field" placeholder="Min. 8 characters" required minlength="8"></div>
            <div><label class="label">Confirm Password</label><input type="password" name="confirm_password" class="input-field" placeholder="Re-enter password" required></div>
            <div><label class="label">Age Range</label>
                <select name="age_range" class="input-field">
                    <option value="18-20">18-20</option>
                    <option value="21-24" selected>21-24</option>
                    <option value="25+">25+</option>
                </select>
            </div>
            <button type="submit" class="btn-primary" id="register-btn">Create Account</button>
        </form>
        <p class="text-sm text-gray-500 text-center mt-4">Already have an account? <a href="#/login" class="text-teal-600 font-medium">Log in</a></p>
    </div>`;
}

async function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById('register-btn');
    btn.disabled = true;
    btn.textContent = 'Creating account...';

    const form = new FormData(e.target);
    try {
        const data = await API.post('/api/auth/register', {
            name: form.get('name'),
            email: form.get('email'),
            password: form.get('password'),
            confirm_password: form.get('confirm_password'),
            age_range: form.get('age_range')
        });
        API.setToken(data.access_token);
        Auth.setUser(data.user);
        showToast('Welcome to CuraTwin!', 'success');
        navigate('dashboard');
    } catch (err) {
        showToast(err.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Create Account';
    }
}
