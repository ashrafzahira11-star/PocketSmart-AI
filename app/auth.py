from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

ALGORITHM = "HS256"

COOKIE_NAME = "pocketsmart_token"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    password: str,
    password_hash: str
) -> bool:

    return pwd_context.verify(
        password,
        password_hash
    )


def create_access_token(user_id: int) -> str:

    expires = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expires
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM
    )


def get_user_from_token(
    token: str,
    db: Session
):

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            return None

        return db.get(
            User,
            int(user_id)
        )

    except (
        JWTError,
        ValueError,
        TypeError
    ):

        return None


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):

    token = request.cookies.get(
        COOKIE_NAME
    )

    if not token:
        return None

    return get_user_from_token(
        token,
        db
    )


def require_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:

    user = get_current_user(
        request,
        db
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in first."
        )

    return user