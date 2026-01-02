from passlib.context import CryptContext


context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)


def hash_password(raw_pass: str, /) -> str:
    """
    Hashes a plain password using bcrypt.
    """
    return context.hash(raw_pass)


def verify_password(raw_pass: str, hashed_pass: str, /) -> bool:
    return context.verify(raw_pass, hashed_pass)