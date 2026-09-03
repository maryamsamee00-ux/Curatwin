const API = {
    token: localStorage.getItem('curatwin_token'),

    setToken(token) {
        this.token = token;
        if (token) localStorage.setItem('curatwin_token', token);
        else localStorage.removeItem('curatwin_token');
    },

    async request(method, path, body = null) {
        const headers = { 'Content-Type': 'application/json' };
        if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

        const opts = { method, headers };
        if (body) opts.body = JSON.stringify(body);

        const res = await fetch(path, opts);

        if (res.status === 401) {
            this.setToken(null);
            window.location.hash = '#/login';
            throw new Error('Session expired. Please log in again.');
        }

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Something went wrong.');
        return data;
    },

    get(path) { return this.request('GET', path); },
    post(path, body) { return this.request('POST', path, body); },
    put(path, body) { return this.request('PUT', path, body); },
    del(path) { return this.request('DELETE', path); },
};
