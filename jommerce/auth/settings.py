AUTH_SUPERUSER_ID = 1
AUTH_PASSWORD_VALIDATORS = [
    "jommerce.auth.validators.validate_password_lowercase",
    "jommerce.auth.validators.validate_password_uppercase",
    "jommerce.auth.validators.validate_password_number",
    "jommerce.auth.validators.validate_password_length",
]
