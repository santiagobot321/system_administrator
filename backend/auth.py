from passlib.context import CryptContext

# Configure the hashing context, using bcrypt as the main algorithm.
# `passlib.context.CryptContext` is a powerful tool for managing password hashes.
# - `schemes=["bcrypt"]`: Specifies that bcrypt is the default and preferred hashing algorithm.
#   Bcrypt is a strong, widely-used, and recommended algorithm for password storage.
# - `deprecated="auto"`: Automatically handles deprecated hash formats. If you were to add a new,
#   stronger algorithm in the future (e.g., argon2), `verify` would still work with old bcrypt
#   hashes, and `hash` would use the new algorithm.

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain password against a stored hash.

    Args:
        plain_password (str): The password entered by the user.
        hashed_password (str): The hash stored in the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hashes a plain password using the configured context (bcrypt).

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The resulting password hash.
    """
    return pwd_context.hash(password)