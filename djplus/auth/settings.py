AUTH_PASSWORD_VALIDATORS = [
    "djplus.auth.validators.password.length",
    "djplus.auth.validators.password.number",
    "djplus.auth.validators.password.lowercase",
    "djplus.auth.validators.password.uppercase",
    "djplus.auth.validators.password.symbol",
]

AUTH_USERNAME_VALIDATORS = [
    "djplus.auth.validators.username.length",
    "djplus.auth.validators.username.ascii",
    "djplus.auth.validators.username.identifier",
]
AUTH_PASSWORD_HASHERS = ["djplus.auth.hashers.default"]
