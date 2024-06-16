def format_email(email: str) -> str:
    return email.split("@")[0] \
        + f"@{email.split("@")[1].lower()}" if "@" in email else ""
