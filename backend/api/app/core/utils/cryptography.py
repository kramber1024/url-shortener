import secrets


def generate_email_secret() -> str:
    return secrets.token_urlsafe(128)
