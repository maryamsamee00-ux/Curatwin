const Auth = {
    user: JSON.parse(localStorage.getItem('curatwin_user') || 'null'),

    setUser(user) {
        this.user = user;
        if (user) localStorage.setItem('curatwin_user', JSON.stringify(user));
        else localStorage.removeItem('curatwin_user');
    },

    isLoggedIn() { return !!API.token && !!this.user; },

    logout() {
        API.setToken(null);
        this.setUser(null);
        window.location.hash = '#/';
    }
};
