from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY
import hashlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _truncate_to_72_bytes(password: str) -> str:
    encoded = password.encode("utf-8")
    if len(encoded) <= 72:
        return password

    truncated = encoded[:72]
    while True:
        try:
            return truncated.decode("utf-8")
        except UnicodeDecodeError:
            truncated = truncated[:-1]


def _prepare_password_for_bcrypt(password: str) -> str:
    safe_password = _truncate_to_72_bytes(password)
    return hashlib.sha256(safe_password.encode("utf-8")).hexdigest()


def hash_password(password):
    hashed_input = _prepare_password_for_bcrypt(password)
    return pwd_context.hash(hashed_input)


def verify_password(plain, hashed):
    plain_hashed_input = _prepare_password_for_bcrypt(plain)
    return pwd_context.verify(plain_hashed_input, hashed)

def create_token(data):
    data.update({"exp": datetime.utcnow() + timedelta(hours=24)})
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")