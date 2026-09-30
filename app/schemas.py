from typing import List

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=80
    )

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):
    username: str
    password: str


class RecommendationItem(BaseModel):
    name: str

    category: str

    estimated_price: int

    reason: str

    platform: str

    search_url: str


class RecommendationResponse(BaseModel):
    planner: str

    budget: int

    total_estimate: int

    remaining_budget: int

    summary: str

    budget_breakdown: List[dict]

    recommendations: List[RecommendationItem]

    notes: List[str] = []


class HomeRequest(BaseModel):
    budget: int = Field(
        gt=0,
        le=10_000_000
    )

    rooms: List[str] = Field(
        min_length=1
    )

    style: str = "Modern"

    priorities: str = ""


class PartyRequest(BaseModel):
    budget: int = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10_000
    )

    event_type: str = "Birthday"

    venue: str = ""

    preferences: str = ""


class JewelryRequest(BaseModel):
    budget: int = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = "Wedding"

    style: str = "Elegant"

    metal: str = "Any"

    outfit_color: str = ""

    preferences: str = ""