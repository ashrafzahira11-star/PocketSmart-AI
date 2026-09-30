import base64
import json
import re
from typing import Optional

from google import genai

from .config import settings
from .recommendations import search_url


def _extract_json(text: str):

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.I
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        match = re.search(
            r"\{.*\}",
            text,
            flags=re.S
        )

        if match:

            return json.loads(
                match.group(0)
            )

        raise


def _client():

    if (
        not settings.use_gemini
        or not settings.gemini_api_key
    ):
        return None

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def _normalize(
    result,
    planner,
    budget
):

    result["planner"] = planner

    result["budget"] = budget

    result.setdefault(
        "budget_breakdown",
        []
    )

    result.setdefault(
        "recommendations",
        []
    )

    result.setdefault(
        "notes",
        []
    )

    result.setdefault(
        "summary",
        "AI-generated budget plan."
    )

    for item in result["recommendations"]:

        item.setdefault(
            "name",
            "Recommended item"
        )

        item.setdefault(
            "category",
            "General"
        )

        item["estimated_price"] = int(
            item.get(
                "estimated_price",
                0
            ) or 0
        )

        item.setdefault(
            "reason",
            "Fits the requested preferences."
        )

        item.setdefault(
            "platform",
            "Amazon"
        )

        item["search_url"] = search_url(
            item["platform"],
            item["name"]
        )

    total = sum(
        item["estimated_price"]
        for item in result["recommendations"]
    )

    result["total_estimate"] = total

    result["remaining_budget"] = (
        budget - total
    )

    return result


def generate_text_plan(
    planner: str,
    payload: dict
):

    client = _client()

    if client is None:
        return None

    budget = payload["budget"]

    schema = {

        "type": "object",

        "properties": {

            "summary": {
                "type": "string"
            },

            "budget_breakdown": {

                "type": "array",

                "items": {

                    "type": "object",

                    "properties": {

                        "category": {
                            "type": "string"
                        },

                        "amount": {
                            "type": "integer"
                        },
                    },

                    "required": [
                        "category",
                        "amount"
                    ],
                },
            },

            "recommendations": {

                "type": "array",

                "items": {

                    "type": "object",

                    "properties": {

                        "name": {
                            "type": "string"
                        },

                        "category": {
                            "type": "string"
                        },

                        "estimated_price": {
                            "type": "integer"
                        },

                        "reason": {
                            "type": "string"
                        },

                        "platform": {

                            "type": "string",

                            "enum": [
                                "Amazon",
                                "Flipkart",
                                "IKEA",
                                "Swiggy",
                                "Zomato",
                                "OYO",
                            ],
                        },
                    },

                    "required": [
                        "name",
                        "category",
                        "estimated_price",
                        "reason",
                        "platform",
                    ],
                },
            },

            "notes": {

                "type": "array",

                "items": {
                    "type": "string"
                },
            },
        },

        "required": [
            "summary",
            "budget_breakdown",
            "recommendations",
            "notes",
        ],
    }

    prompt = f"""
You are PocketSmart AI,
a budget recommendation assistant.

Planner: {planner}

User data:

{json.dumps(payload, indent=2)}

Create a practical plan that stays
within the user's total budget of
INR {budget}.

Do not claim that you checked live
inventory, live prices, or private
retailer APIs.

Use approximate prices only.

Use only these platforms when relevant:

Amazon
Flipkart
IKEA
Swiggy
Zomato
OYO

Avoid unsafe, illegal, or regulated
recommendations.

Return only JSON matching the
provided schema.
"""

    response = client.models.generate_content(

        model=settings.gemini_model,

        contents=prompt,

        config={

            "response_mime_type":
                "application/json",

            "response_schema":
                schema,
        },
    )

    return _normalize(
        _extract_json(
            response.text
        ),
        planner,
        budget
    )


def generate_jewelry_plan(
    payload: dict,
    image_bytes: Optional[bytes],
    mime_type: Optional[str]
):

    client = _client()

    if client is None:
        return None

    prompt = f"""
You are PocketSmart AI's jewelry planner.

Budget:
INR {payload["budget"]}

Occasion:
{payload["occasion"]}

Style:
{payload["style"]}

Metal:
{payload["metal"]}

Outfit color:
{payload.get("outfit_color") or "not specified"}

Preferences:
{payload.get("preferences") or "none"}

If an outfit image is provided,
use it only to discuss visible colors,
patterns, neckline/visual balance
and style.

Do not identify the person.

Return a practical budget-aware
jewelry plan as JSON.

Never claim live stock or live pricing.

Use approximate prices.

Platforms may be Amazon or Flipkart.
"""

    contents = [prompt]

    if image_bytes:

        contents.append({

            "inline_data": {

                "mime_type":
                    mime_type or "image/jpeg",

                "data":
                    base64.b64encode(
                        image_bytes
                    ).decode("utf-8"),
            }
        })

    schema = {

        "type": "object",

        "properties": {

            "summary": {
                "type": "string"
            },

            "budget_breakdown": {

                "type": "array",

                "items": {

                    "type": "object",

                    "properties": {

                        "category": {
                            "type": "string"
                        },

                        "amount": {
                            "type": "integer"
                        },
                    },

                    "required": [
                        "category",
                        "amount"
                    ],
                },
            },

            "recommendations": {

                "type": "array",

                "items": {

                    "type": "object",

                    "properties": {

                        "name": {
                            "type": "string"
                        },

                        "category": {
                            "type": "string"
                        },

                        "estimated_price": {
                            "type": "integer"
                        },

                        "reason": {
                            "type": "string"
                        },

                        "platform": {

                            "type": "string",

                            "enum": [
                                "Amazon",
                                "Flipkart"
                            ],
                        },
                    },

                    "required": [
                        "name",
                        "category",
                        "estimated_price",
                        "reason",
                        "platform",
                    ],
                },
            },

            "notes": {

                "type": "array",

                "items": {
                    "type": "string"
                },
            },
        },

        "required": [
            "summary",
            "budget_breakdown",
            "recommendations",
            "notes",
        ],
    }

    response = client.models.generate_content(

        model=settings.gemini_model,

        contents=contents,

        config={

            "response_mime_type":
                "application/json",

            "response_schema":
                schema,
        },
    )

    return _normalize(
        _extract_json(
            response.text
        ),
        "jewelry",
        payload["budget"]
    )