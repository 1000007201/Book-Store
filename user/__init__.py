from .api import Registration, Activate, Login, Logout

user_routes = [
    (Registration, '/register'),
    (Activate, '/activate'),
    (Login, '/login'),
    (Logout, '/logout')
]
