from urllib.parse import quote_plus


PLATFORMS = {
    "Amazon":
        "https://www.amazon.in/s?k={q}",

    "Flipkart":
        "https://www.flipkart.com/search?q={q}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={q}",

    "Swiggy":
        "https://www.swiggy.com/search?query={q}",

    "Zomato":
        "https://www.zomato.com/search?query={q}",

    "OYO":
        "https://www.oyorooms.com/search?location={q}",
}


def search_url(
    platform: str,
    query: str
) -> str:

    template = PLATFORMS.get(
        platform,
        PLATFORMS["Amazon"]
    )

    return template.format(
        q=quote_plus(query)
    )


def split_budget(
    budget: int,
    percentages
):

    return [
        {
            "category": name,
            "amount": round(
                budget * percentage
            )
        }

        for name, percentage
        in percentages
    ]


def home_fallback(data):

    budget = data["budget"]

    rooms = data["rooms"]

    style = data["style"]

    priorities = data.get(
        "priorities",
        ""
    )

    percentages = [
        ("Furniture", 0.40),
        ("Lighting", 0.18),
        ("Decor", 0.15),
        ("Storage", 0.15),
        ("Contingency", 0.12),
    ]

    breakdown = split_budget(
        budget,
        percentages
    )

    per_room = max(
        1,
        budget // max(
            1,
            len(rooms)
        )
    )

    ideas = [

        (
            "LED ceiling light",
            "Lighting",
            max(
                1200,
                per_room // 8
            ),
            "Amazon"
        ),

        (
            "Compact side table",
            "Furniture",
            max(
                1800,
                per_room // 5
            ),
            "IKEA"
        ),

        (
            "Cushion cover set",
            "Decor",
            max(
                700,
                per_room // 12
            ),
            "Flipkart"
        ),

        (
            "Wall shelf",
            "Storage",
            max(
                1200,
                per_room // 7
            ),
            "IKEA"
        ),

        (
            "Area rug",
            "Decor",
            max(
                1800,
                per_room // 5
            ),
            "Amazon"
        ),
    ]

    items = []

    for (
        name,
        category,
        price,
        platform
    ) in ideas:

        items.append({

            "name": name,

            "category": category,

            "estimated_price": int(
                price
            ),

            "reason":
                f"Suitable for a "
                f"{style.lower()} style "
                f"setup and can be "
                f"adjusted to your room size.",

            "platform": platform,

            "search_url":
                search_url(
                    platform,
                    f"{name} {style}"
                ),
        })

    total = sum(
        item["estimated_price"]
        for item in items
    )

    return {

        "planner": "home",

        "budget": budget,

        "total_estimate": total,

        "remaining_budget":
            budget - total,

        "summary":
            f"A starter {style} plan "
            f"for {', '.join(rooms)} "
            f"with priority on practical purchases.",

        "budget_breakdown":
            breakdown,

        "recommendations":
            items,

        "notes": [

            "Fallback mode is active "
            "if Gemini is not configured.",

            f"Your stated priorities: "
            f"{priorities or 'balanced value and appearance'}.",

            "Check the retailer page "
            "for current stock, seller, "
            "delivery charges and final price.",
        ],
    }


def party_fallback(data):

    budget = data["budget"]

    guests = data["guests"]

    event_type = data["event_type"]

    venue = data.get(
        "venue"
    ) or "local venue"

    preferences = data.get(
        "preferences",
        ""
    )

    percentages = [

        (
            "Food & beverages",
            0.45
        ),

        (
            "Decoration",
            0.18
        ),

        (
            "Venue",
            0.20
        ),

        (
            "Entertainment",
            0.10
        ),

        (
            "Contingency",
            0.07
        ),
    ]

    breakdown = split_budget(
        budget,
        percentages
    )

    food_per_guest = max(
        250,
        round(
            budget * 0.45 / guests
        )
    )

    ideas = [

        (
            "Catering package",
            "Food & beverages",
            food_per_guest * guests,
            "Swiggy"
        ),

        (
            "Party decoration set",
            "Decoration",
            max(
                1200,
                round(
                    budget * 0.18
                )
            ),
            "Amazon"
        ),

        (
            f"{venue} search",
            "Venue",
            max(
                2000,
                round(
                    budget * 0.20
                )
            ),
            "OYO"
        ),

        (
            "Birthday/event cake",
            "Food & beverages",
            max(
                1000,
                round(
                    budget * 0.08
                )
            ),
            "Zomato"
        ),

        (
            "Party speaker",
            "Entertainment",
            max(
                1500,
                round(
                    budget * 0.10
                )
            ),
            "Amazon"
        ),
    ]

    items = []

    for (
        name,
        category,
        price,
        platform
    ) in ideas:

        items.append({

            "name": name,

            "category": category,

            "estimated_price":
                int(price),

            "reason":
                f"Designed as a "
                f"practical starting point "
                f"for a {event_type.lower()} "
                f"with {guests} guests.",

            "platform": platform,

            "search_url":
                search_url(
                    platform,
                    f"{name} {event_type}"
                ),
        })

    total = sum(
        item["estimated_price"]
        for item in items
    )

    return {

        "planner": "party",

        "budget": budget,

        "total_estimate": total,

        "remaining_budget":
            budget - total,

        "summary":
            f"A balanced {event_type} "
            f"plan for approximately "
            f"{guests} guests at/around {venue}.",

        "budget_breakdown":
            breakdown,

        "recommendations":
            items,

        "notes": [

            "Fallback mode is active "
            "if Gemini is not configured.",

            f"Preferences: "
            f"{preferences or 'balanced and family-friendly'}.",

            "Venue and food prices vary "
            "by location, date, vendor "
            "and availability.",
        ],
    }


def jewelry_fallback(data):

    budget = data["budget"]

    occasion = data["occasion"]

    style = data["style"]

    metal = data["metal"]

    color = data.get(
        "outfit_color"
    ) or "your outfit color"

    percentages = [

        (
            "Main jewelry",
            0.55
        ),

        (
            "Earrings",
            0.20
        ),

        (
            "Bracelet/bangle",
            0.15
        ),

        (
            "Contingency",
            0.10
        ),
    ]

    breakdown = split_budget(
        budget,
        percentages
    )

    ideas = [

        (
            "Statement necklace",
            "Main jewelry",
            max(
                1500,
                round(
                    budget * 0.55
                )
            ),
            "Amazon"
        ),

        (
            "Matching earrings",
            "Earrings",
            max(
                700,
                round(
                    budget * 0.20
                )
            ),
            "Flipkart"
        ),

        (
            "Minimal bracelet",
            "Bracelet/bangle",
            max(
                500,
                round(
                    budget * 0.15
                )
            ),
            "Amazon"
        ),
    ]

    items = []

    for (
        name,
        category,
        price,
        platform
    ) in ideas:

        items.append({

            "name": name,

            "category": category,

            "estimated_price":
                int(price),

            "reason":
                f"{style} styling "
                f"for a {occasion.lower()} "
                f"with {color} clothing "
                f"and {metal} preference.",

            "platform": platform,

            "search_url":
                search_url(
                    platform,
                    f"{name} {style} {metal}"
                ),
        })

    total = sum(
        item["estimated_price"]
        for item in items
    )

    return {

        "planner": "jewelry",

        "budget": budget,

        "total_estimate": total,

        "remaining_budget":
            budget - total,

        "summary":
            f"A {style.lower()} "
            f"jewelry starting set "
            f"for {occasion.lower()} wear.",

        "budget_breakdown":
            breakdown,

        "recommendations":
            items,

        "notes": [

            "Fallback mode is active "
            "if Gemini is not configured.",

            "Image analysis is only "
            "performed when Gemini is "
            "configured and an image is supplied.",

            "Verify material, plating, "
            "size, seller rating and "
            "return policy before buying.",
        ],
    }