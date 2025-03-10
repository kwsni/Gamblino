import secrets

def secret_keygen():
        return secrets.token_urlsafe(nbytes=12)
