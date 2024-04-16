from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes="bcrypt", deprecated="auto")

def hash(password: str):
    return PWD_CONTEXT.hash(password)