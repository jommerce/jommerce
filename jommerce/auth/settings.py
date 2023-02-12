AUTH_PASSWORD_VALIDATORS = [
    "jommerce.auth.validators.password.length",
    "jommerce.auth.validators.password.number",
    "jommerce.auth.validators.password.lowercase",
    "jommerce.auth.validators.password.uppercase",
    "jommerce.auth.validators.password.symbol",
]

AUTH_USERNAME_VALIDATORS = [
    "jommerce.auth.validators.username.length",
    "jommerce.auth.validators.username.ascii",
    "jommerce.auth.validators.username.identifier",
]
AUTH_PASSWORD_HASHERS = ["jommerce.auth.hashers.default"]
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
