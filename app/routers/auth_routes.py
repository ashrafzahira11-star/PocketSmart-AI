from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..auth import (
    COOKIE_NAME,
    create_access_token,
    hash_password,
    verify_password,
)
from ..database import get_db
from ..models import User


router = APIRouter()


@router.post("/register")
def register(

    request: Request,

    username: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db),
):

    username = username.strip()

    if (
        len(username) < 3
        or len(password) < 6
    ):

        return RedirectResponse(
            "/register?error=Username+or+password+is+too+short",
            status_code=303
        )

    existing = (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )

    if existing:

        return RedirectResponse(
            "/register?error=Username+already+exists",
            status_code=303
        )

    user = User(

        username=username,

        password_hash=
            hash_password(password)
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    token = create_access_token(
        user.id
    )

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    response.set_cookie(

        COOKIE_NAME,

        token,

        httponly=True,

        samesite="lax",

        secure=False,

        max_age=60 * 60 * 2,
    )

    return response


@router.post("/login")
def login(

    request: Request,

    username: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db),
):

    user = (

        db.query(User)

        .filter(
            User.username
            == username.strip()
        )

        .first()
    )

    if (
        not user
        or not verify_password(
            password,
            user.password_hash
        )
    ):

        return RedirectResponse(
            "/login?error=Invalid+username+or+password",
            status_code=303
        )

    token = create_access_token(
        user.id
    )

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    response.set_cookie(

        COOKIE_NAME,

        token,

        httponly=True,

        samesite="lax",

        secure=False,

        max_age=60 * 60 * 2,
    )

    return response


@router.post("/logout")
def logout():

    response = RedirectResponse(
        "/",
        status_code=303
    )

    response.delete_cookie(
        COOKIE_NAME
    )

    return response


@router.post("/token")
def token_api(

    username: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db),
):

    user = (

        db.query(User)

        .filter(
            User.username
            == username.strip()
        )

        .first()
    )

    if (
        not user
        or not verify_password(
            password,
            user.password_hash
        )
    ):

        return {
            "authenticated": False,
            "access_token": None
        }

    return {

        "authenticated": True,

        "access_token":
            create_access_token(
                user.id
            ),

        "token_type":
            "bearer",
    }