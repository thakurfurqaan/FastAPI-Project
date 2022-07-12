from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(entered_pwd, hashed_pwd):
    return pwd_context.verify(entered_pwd, hashed_pwd)