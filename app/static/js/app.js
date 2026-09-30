function money(value) {

    return "₹" +
        Number(value || 0)
            .toLocaleString("en-IN");
}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function (c) {

            return {

                "&": "&amp;",

                "<": "&lt;",

                ">": "&gt;",

                '"': "&quot;",

                "'": "&#039;"

            }[c];

        }
    );
}


function renderResult(
    target,
    data
) {

    const breakdown =
        (data.budget_breakdown || [])
        .map(function (x) {

            return `
                <div class="breakdown-row">

                    <span>
                        ${escapeHtml(
                            x.category
                        )}
                    </span>

                    <strong>
                        ${money(x.amount)}
                    </strong>

                </div>
            `;

        })
        .join("");


    const items =
        (data.recommendations || [])
        .map(function (item) {

            return `
                <article class="recommendation">

                    <div class="rec-top">

                        <span class="tag">
                            ${escapeHtml(
                                item.category
                            )}
                        </span>

                        <span>
                            ${escapeHtml(
                                item.platform
                            )}
                        </span>

                    </div>


                    <h3>
                        ${escapeHtml(
                            item.name
                        )}
                    </h3>


                    <p>
                        ${escapeHtml(
                            item.reason
                        )}
                    </p>


                    <div class="rec-bottom">

                        <strong>
                            ${money(
                                item.estimated_price
                            )}
                        </strong>

                        <a
                            href="${escapeHtml(
                                item.search_url
                            )}"
                            target="_blank"
                            rel="noopener"
                        >
                            Search platform ↗
                        </a>

                    </div>

                </article>
            `;

        })
        .join("");


    target.innerHTML = `

        <div class="result-head">

            <div>

                <p class="eyebrow">
                    ${escapeHtml(
                        data.planner
                    )} PLAN
                </p>

                <h2>
                    ${money(
                        data.total_estimate
                    )}
                    estimated
                </h2>

            </div>


            <div class="remaining">

                ${money(
                    data.remaining_budget
                )}

                remaining

            </div>

        </div>


        <p>
            ${escapeHtml(
                data.summary
            )}
        </p>


        <h3>
            Budget allocation
        </h3>


        <div class="breakdown">

            ${breakdown}

        </div>


        <h3>
            Recommendations
        </h3>


        <div class="recommendations">

            ${items}

        </div>


        <div class="notes">

            <strong>
                Notes
            </strong>

            <ul>

                ${(data.notes || [])
                    .map(function (note) {

                        return `
                            <li>
                                ${escapeHtml(
                                    note
                                )}
                            </li>
                        `;

                    })
                    .join("")
                }

            </ul>

        </div>
    `;
}


async function postJSON(
    url,
    payload
) {

    const response =
        await fetch(
            url,
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(
                        payload
                    )

            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );

    }


    return data;
}


function setLoading(
    button,
    yes
) {

    button.disabled = yes;

    if (!button.dataset.oldText) {

        button.dataset.oldText =
            button.textContent;

    }

    button.textContent =
        yes
            ? "Generating..."
            : button.dataset.oldText;
}


function setupHomePlanner() {

    const form =
        document.getElementById(
            "homeForm"
        );

    if (!form) return;


    form.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();


            const button =
                form.querySelector(
                    "button"
                );


            setLoading(
                button,
                true
            );


            try {

                const data =
                    await postJSON(
                        "/api/generate-home",
                        {

                            budget:
                                Number(
                                    document
                                    .getElementById(
                                        "homeBudget"
                                    )
                                    .value
                                ),

                            rooms:
                                [
                                    ...
                                    document
                                    .getElementById(
                                        "homeRooms"
                                    )
                                    .selectedOptions
                                ]
                                .map(
                                    o => o.value
                                ),

                            style:
                                document
                                .getElementById(
                                    "homeStyle"
                                )
                                .value,

                            priorities:
                                document
                                .getElementById(
                                    "homePriorities"
                                )
                                .value

                        }
                    );


                renderResult(

                    document
                    .getElementById(
                        "homeResult"
                    ),

                    data
                );


            } catch (err) {

                document
                    .getElementById(
                        "homeResult"
                    )
                    .innerHTML =
                    `
                    <div class="alert">
                        ${escapeHtml(
                            err.message
                        )}
                    </div>
                    `;

            } finally {

                setLoading(
                    button,
                    false
                );

            }

        }
    );
}


function setupPartyPlanner() {

    const form =
        document.getElementById(
            "partyForm"
        );

    if (!form) return;


    form.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();


            const button =
                form.querySelector(
                    "button"
                );


            setLoading(
                button,
                true
            );


            try {

                const data =
                    await postJSON(
                        "/api/generate-party",
                        {

                            budget:
                                Number(
                                    document
                                    .getElementById(
                                        "partyBudget"
                                    )
                                    .value
                                ),

                            guests:
                                Number(
                                    document
                                    .getElementById(
                                        "partyGuests"
                                    )
                                    .value
                                ),

                            event_type:
                                document
                                .getElementById(
                                    "partyType"
                                )
                                .value,

                            venue:
                                document
                                .getElementById(
                                    "partyVenue"
                                )
                                .value,

                            preferences:
                                document
                                .getElementById(
                                    "partyPreferences"
                                )
                                .value

                        }
                    );


                renderResult(

                    document
                    .getElementById(
                        "partyResult"
                    ),

                    data
                );


            } catch (err) {

                document
                    .getElementById(
                        "partyResult"
                    )
                    .innerHTML =
                    `
                    <div class="alert">
                        ${escapeHtml(
                            err.message
                        )}
                    </div>
                    `;

            } finally {

                setLoading(
                    button,
                    false
                );

            }

        }
    );
}


function setupJewelryPlanner() {

    const form =
        document.getElementById(
            "jewelryForm"
        );

    if (!form) return;


    form.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();


            const button =
                form.querySelector(
                    "button"
                );


            setLoading(
                button,
                true
            );


            try {

                const response =
                    await fetch(
                        "/api/generate-jewelry",
                        {

                            method: "POST",

                            body:
                                new FormData(
                                    form
                                )

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Request failed"
                    );

                }


                renderResult(

                    document
                    .getElementById(
                        "jewelryResult"
                    ),

                    data
                );


            } catch (err) {

                document
                    .getElementById(
                        "jewelryResult"
                    )
                    .innerHTML =
                    `
                    <div class="alert">
                        ${escapeHtml(
                            err.message
                        )}
                    </div>
                    `;

            } finally {

                setLoading(
                    button,
                    false
                );

            }

        }
    );
}


async function loadHistory(id) {

    const target =
        document.getElementById(
            "historyResult"
        );


    target.innerHTML =
        "<div class='empty'>Loading...</div>";


    try {

        const response =
            await fetch(
                `/api/recommendations-details/${id}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not load history."
            );

        }


        renderResult(
            target,
            data
        );


    } catch (err) {

        target.innerHTML =
            `
            <div class="alert">
                ${escapeHtml(
                    err.message
                )}
            </div>
            `;

    }
}