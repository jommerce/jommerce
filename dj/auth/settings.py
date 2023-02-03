AUTH_PASSWORD_VALIDATORS = [
    "dj.auth.validators.password.length",
    "dj.auth.validators.password.number",
    "dj.auth.validators.password.lowercase",
    "dj.auth.validators.password.uppercase",
    "dj.auth.validators.password.symbol",
]

AUTH_USERNAME_VALIDATORS = [
    "dj.auth.validators.username.length",
    "dj.auth.validators.username.ascii",
    "dj.auth.validators.username.identifier",
]
AUTH_PASSWORD_HASHERS = ["dj.auth.hashers.default"]
AUTH_LOGIN_URL = "/auth/login/"
AUTH_LOGIN_REDIRECT_URL = "/"
AUTH_LOGOUT_REDIRECT_URL = "/"
AUTH_SIGNUP_REDIRECT_URL = "/"
AUTH_USER_MODEL = "auth.User"

# Sessions
# ----------------------------------------------------------------------------------------------------------------------
# Cookie name. This can be whatever you want.
AUTH_SESSION_COOKIE_NAME = "session_key"
# Age of cookie, in seconds (default: 2 weeks).
AUTH_SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# A string like "example.com", or None for standard domain cookie.
AUTH_SESSION_COOKIE_DOMAIN = None
# Whether the session cookie should be secure (https:// only).
AUTH_SESSION_COOKIE_SECURE = False
# The path of the session cookie.
AUTH_SESSION_COOKIE_PATH = "/"
# Whether to use the HttpOnly flag.
AUTH_SESSION_COOKIE_HTTPONLY = True
# Whether to set the flag restricting cookie leaks on cross-site requests.
# This can be 'Lax', 'Strict', 'None', or False to disable the flag.
AUTH_SESSION_COOKIE_SAMESITE = "Lax"
