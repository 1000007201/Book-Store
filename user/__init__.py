from .api import Registration, Activate, Login, Logout, ChangePassword

user_routes = [
    (Registration, '/register'),
    (Activate, '/activate'),
    (Login, '/login'),
    (Logout, '/logout'),
    (ChangePassword, '/change/password')
]
