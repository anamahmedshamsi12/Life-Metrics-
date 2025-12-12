"""
scenarios.py

This module defines the set of daily scenarios (actions) available to the
user during the simulation. Each scenario represents a choice the user
can make at a given check-in and describes how that choice affects
different life metrics.

Each scenario is represented as a dictionary with the following keys:
- id: A unique string identifier used in forms and routing logic
- label: Short, user-facing text displayed on a button
- description: Optional longer explanation of the scenario
- deltas: A dictionary mapping metric names to integer changes

The scenarios are grouped by simulation mode (student, professional,
or custom). Organizing scenarios this way allows the simulation logic
to remain flexible and easily extensible, which follows the modular
design principles emphasized in CS5001.
"""

# Enable postponed evaluation of type annotations so types can reference
# objects defined later in the file
from __future__ import annotations

# Import typing helpers for clearer dictionary and list annotations
from typing import Dict, List, Any

# Define a type alias for a scenario/action dictionary
# Each action stores metadata and metric deltas
Action = Dict[str, Any]


# Define all available actions grouped by simulation mode
ACTIONS: Dict[str, List[Action]] = {

    # Student Life scenarios
    "student": [
        {
            # Unique identifier for this action
            "id": "study_block",

            # Short label shown to the user
            "label": "Deep study session (2 hrs)",

            # Longer explanation of what the action represents
            "description": "Focus on coursework and assignments.",

            # Metric changes caused by this action
            "deltas": {
                "Academics": +10,
                "Energy": -4,
                "Social life": -3,
                "Wellbeing": -1,
            },
        },
        {
            # Identifier for sleeping early
            "id": "sleep_early",

            # Button label shown in the UI
            "label": "Sleep 8 hours",

            # Explanation of the benefit of this action
            "description": "Prioritize rest and recovery.",

            # Positive deltas emphasizing rest and recovery
            "deltas": {
                "Wellbeing": +6,
                "Energy": +8,
                "Academics": +2,
            },
        },
        {
            # Identifier for social activity
            "id": "hangout_friends",

            # Button label
            "label": "Hang out with friends",

            # Description of the action
            "description": "Spend time socializing and relaxing.",

            # Tradeoffs between social life and responsibilities
            "deltas": {
                "Social life": +9,
                "Wellbeing": +3,
                "Academics": -3,
                "Finances": -2,
            },
        },
        {
            # Identifier for unproductive late-night behavior
            "id": "doomscroll",

            # Button label
            "label": "Late-night scrolling",

            # Description explaining the negative behavior
            "description": "Stay up late on your phone instead of resting.",

            # Mostly negative effects across metrics
            "deltas": {
                "Energy": -6,
                "Wellbeing": -4,
                "Academics": -2,
            },
        },
        {
            # Identifier for working a job shift
            "id": "part_time_work",

            # Button label
            "label": "Part-time job shift",

            # Description of the scenario
            "description": "Earn money but use time and energy.",

            # Financial gain at the cost of energy and social time
            "deltas": {
                "Finances": +8,
                "Energy": -4,
                "Social life": -2,
            },
        },
    ],

    # Professional Life scenarios  # ----------------------------
    "professional": [
        {
            # Identifier for focused work
            "id": "focus_work",

            # Button label
            "label": "Deep work sprint",

            # Description of high-focus professional effort
            "description": "Block out distractions and ship important work.",

            # Tradeoff between career growth and burnout
            "deltas": {
                "Career growth": +9,
                "Burnout": +4,
                "Work–life balance": -4,
                "Wellbeing": -1,
            },
        },
        {
            # Identifier for networking activity
            "id": "network_event",

            # Button label
            "label": "Networking event",

            # Description of the action
            "description": "Meet new people and grow your network.",

            # Mixed career and wellbeing effects
            "deltas": {
                "Career growth": +5,
                "Wellbeing": +2,
                "Finances": -2,
            },
        },
        {
            # Identifier for rest and recovery
            "id": "self_care",

            # Button label
            "label": "Self-care evening",

            # Description emphasizing balance and recovery
            "description": "Turn off notifications and recharge.",

            # Improvements in balance and reduced burnout
            "deltas": {
                "Wellbeing": +7,
                "Work–life balance": +6,
                "Burnout": -5,
            },
        },
        {
            # Identifier for working overtime
            "id": "overtime",

            # Button label
            "label": "Overtime + late emails",

            # Description explaining extended work hours
            "description": "Push extra work past regular hours.",

            # Strong tradeoffs between growth, burnout, and balance
            "deltas": {
                "Career growth": +4,
                "Finances": +3,
                "Work–life balance": -6,
                "Burnout": +6,
                "Wellbeing": -3,
            },
        },
        {
            # Identifier for financial review
            "id": "budget_review",

            # Button label
            "label": "Review budget & finances",

            # Description of careful financial planning
            "description": "Track spending and adjust plans.",

            # Small positive effects focused on finances
            "deltas": {
                "Finances": +6,
                "Wellbeing": +1,
            },
        },
    ],

    # Custom Life scenarios
    "custom": [
        {
            # Identifier for a very positive day
            "id": "strong_day",

            # Button label
            "label": "Strong day",

            # Description shown to the user
            "description": "Most things went your way today.",

            # Deltas are handled dynamically for custom mode
            "deltas": {},
        },
        {
            # Identifier for a neutral day
            "id": "steady_day",

            # Button label
            "label": "Steady day",

            # Description of a balanced day
            "description": "A normal, balanced day.",

            # Deltas are computed dynamically if needed
            "deltas": {},
        },
        {
            # Identifier for a difficult day
            "id": "tough_day",

            # Button label
            "label": "Tough day",

            # Description of a challenging experience
            "description": "Challenging day that pulled you back.",

            # Deltas are computed dynamically if needed
            "deltas": {},
        },
    ],
}

