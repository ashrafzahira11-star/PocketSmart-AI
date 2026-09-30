import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from ..auth import require_user
from ..database import get_db
from ..gemini_utils import (
    generate_jewelry_plan,
    generate_text_plan,
)
from ..models import (
    RecommendationHistory,
    User,
)
from ..recommendations import (
    home_fallback,
    jewelry_fallback,
    party_fallback,
)
from ..schemas import (
    HomeRequest,
    PartyRequest,
)


router = APIRouter(
    prefix="/api",
    tags=["planners"]
)


def save_history(
    db,
    user,
    planner,
    budget,
    payload,
    result
):

    record = RecommendationHistory(

        user_id=user.id,

        planner_type=planner,

        budget=budget,

        input_summary=json.dumps(
            payload,
            ensure_ascii=False
        ),

        result_json=json.dumps(
            result,
            ensure_ascii=False
        ),
    )

    db.add(record)

    db.commit()


@router.post("/generate-home")
def generate_home(

    data: HomeRequest,

    user: User = Depends(
        require_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    payload = data.model_dump()

    try:

        result = generate_text_plan(
            "home",
            payload
        )

    except Exception:

        result = None

    result = (
        result
        or home_fallback(payload)
    )

    save_history(
        db,
        user,
        "home",
        data.budget,
        payload,
        result
    )

    return result


@router.post("/generate-party")
def generate_party(

    data: PartyRequest,

    user: User = Depends(
        require_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    payload = data.model_dump()

    try:

        result = generate_text_plan(
            "party",
            payload
        )

    except Exception:

        result = None

    result = (
        result
        or party_fallback(payload)
    )

    save_history(
        db,
        user,
        "party",
        data.budget,
        payload,
        result
    )

    return result


@router.post("/generate-jewelry")
async def generate_jewelry(

    budget: int = Form(...),

    occasion: str = Form(
        "Wedding"
    ),

    style: str = Form(
        "Elegant"
    ),

    metal: str = Form(
        "Any"
    ),

    outfit_color: str = Form(
        ""
    ),

    preferences: str = Form(
        ""
    ),

    outfit_image:
        UploadFile | None = File(
            None
        ),

    user: User = Depends(
        require_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail=
                "Budget must be greater than zero."
        )

    payload = {

        "budget": budget,

        "occasion": occasion,

        "style": style,

        "metal": metal,

        "outfit_color":
            outfit_color,

        "preferences":
            preferences,
    }

    image_bytes = None

    mime_type = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        mime_type = (
            outfit_image.content_type
            or "image/jpeg"
        )

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if mime_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail=
                    "Use JPG, PNG or WEBP."
            )

        image_bytes = (
            await outfit_image.read()
        )

        if len(image_bytes) > 5 * 1024 * 1024:

            raise HTTPException(
                status_code=400,
                detail=
                    "Image must be 5 MB or smaller."
            )

    try:

        result = generate_jewelry_plan(

            payload,

            image_bytes,

            mime_type
        )

    except Exception:

        result = None

    result = (
        result
        or jewelry_fallback(
            payload
        )
    )

    save_history(

        db,

        user,

        "jewelry",

        budget,

        payload,

        result
    )

    return result


@router.get(
    "/recommendations-details/{history_id}"
)
def recommendation_details(

    history_id: int,

    user: User = Depends(
        require_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    record = (

        db.query(
            RecommendationHistory
        )

        .filter(

            RecommendationHistory.id
            == history_id,

            RecommendationHistory.user_id
            == user.id,
        )

        .first()
    )

    if not record:

        raise HTTPException(
            status_code=404,
            detail=
                "Recommendation not found."
        )

    return json.loads(
        record.result_json
    )


@router.get(
    "/session-info"
)
def session_info(
    user: User = Depends(
        require_user
    )
):

    return {

        "logged_in": True,

        "user_id": user.id,

        "username": user.username,
    }


@router.get(
    "/session-data"
)
def session_data(

    user: User = Depends(
        require_user
    ),

    db: Session = Depends(
        get_db
    )
):

    count = (

        db.query(
            RecommendationHistory
        )

        .filter(
            RecommendationHistory.user_id
            == user.id
        )

        .count()
    )

    return {

        "username":
            user.username,

        "recommendation_count":
            count,
    }