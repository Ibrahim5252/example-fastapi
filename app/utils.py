from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(passwd: str):
    return pwd_context.hash(passwd) #! converts plian passwd to hash(encrypted) passwd.

def verify(plain_passwd, hash_passwd):
    return pwd_context.verify(plain_passwd,hash_passwd) #! compares the plain and hash passwd to verify.