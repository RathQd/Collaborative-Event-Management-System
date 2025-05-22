from passlib.context import CryptContext
pass_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# encryption : password + salt
# varification : take same salt parameter and regenerate the same salt and varify the hash value

def hash(password: str):
    return pass_context.hash(password)

def verify_hash(row_password, hashed_password):
    return pass_context.verify(row_password, hashed_password)