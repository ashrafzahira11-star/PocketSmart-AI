from fastapi import (
    APIRouter,
    Depends,
    Request
)

from fastapi.responses import (
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import (
    RecommendationHistory
)


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


def page_context(
    request,
    user=None,
    **extra
):

    data = {
        "request": request,
        "user": user
    }

    data.update(extra)

    return data


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=page_context(
            request,
            user
        )
    )


@router.get("/login")
def login_page(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if user:

        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=page_context(
            request,
            user,
            error=request.query_params.get("error")
        )
    )


@router.get("/register")
def register_page(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if user:

        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context=page_context(
            request,
            user,
            error=request.query_params.get("error")
        )
    )


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=page_context(
            request,
            user
        )
    )


@router.get("/home-planner")
def home_planner(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context=page_context(
            request,
            user
        )
    )


@router.get("/party-planner")
def party_planner(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context=page_context(
            request,
            user
        )
    )


@router.get("/jewelry-planner")
def jewelry_planner(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context=page_context(
            request,
            user
        )
    )


@router.get("/history")
def history(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    records = (
        db.query(
            RecommendationHistory
        )
        .filter(
            RecommendationHistory.user_id == user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context=page_context(
            request,
            user,
            records=records
        )
    )