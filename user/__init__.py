from .api import Registration, Activate, Login, Logout, ChangePassword, SetPassword, ForgetPassword

user_routes = [
    (Registration, '/register'),
    (Activate, '/activate'),
    (Login, '/login'),
    (Logout, '/logout'),
    (ChangePassword, '/change/password'),
    (ForgetPassword, '/password/forget'),
    (SetPassword, '/password/set')
]
