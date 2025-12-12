"""
profiles.py

This module defines the Profile class and helper functions used to
construct the different lifestyle profiles in the Life Metrics Simulator.

A Profile represents the configuration for a simulation mode and
encapsulates all information needed to start and run a simulation,
including:

- A human-readable name (e.g., "Student Life" or "Professional Life")
- The initial set of life metrics and their starting values
- A mode identifier string ("student", "professional", or "custom")
- Optional activity labels and descriptions for custom simulations

Separating profile construction into this module helps keep the
simulation logic modular and organized. It allows new profiles to be
added or modified without changing the core simulation or routing
logic, following the modular design principles emphasized in CS5001.
"""

class Profile:
    """
    Represents a lifestyle profile used by the simulator.

    Attributes:
        name (str):
            Human-readable label for the profile (shown in the UI).

        initial_metrics (dict[str, int]):
            Mapping from metric name (snake_case) to an initial value in [0, 100].

        mode (str):
            Short identifier for the profile type:
            - "student"
            - "professional"
            - "custom"

        activity_labels (list[str]):
            Optional list of labels for activities, primarily used for
            Custom Life simulations where the user defines their own actions.
    """
class Profile:
    """
    Represent a simulation profile configuration.

    A Profile object groups together the information required to
    initialize a simulation mode, including its name, starting
    metrics, and optional activity labels.

    Args:
        name (str): A human-readable name for the profile.
        initial_metrics (dict[str, int]): A dictionary mapping metric
            names to their starting values.
        mode (str): A string identifier for the simulation mode
            ("student", "professional", or "custom").
        activity_labels (list[str] | None): Optional list of activity
            labels used primarily in custom simulations.

    Returns:
        None

    Examples:
        Normal case:
            - Creating a Profile with a name, metrics, and mode stores
              all values as instance attributes.

        Edge case 1:
            - If activity_labels is not provided, it defaults to an
              empty list to avoid None-related errors.

        Edge case 2:
            - If an empty metrics dictionary is provided, the Profile
              still initializes correctly, though the simulation
              may have limited behavior.
    """

    def __init__(self, name, initial_metrics, mode: str = "student", activity_labels=None):
        # Store the human-readable name of the profile
        self.name = name

        # Store the initial metrics dictionary for the simulation
        self.initial_metrics = initial_metrics

        # Store the mode identifier string
        self.mode = mode

        # Store activity labels, defaulting to an empty list if none are provided
        self.activity_labels = activity_labels or []


def get_profile_from_form_value(value: str) -> Profile:
    """
    Map a submitted form value to a predefined Profile instance.

    This function translates simple form input values into fully
    configured Profile objects for built-in simulation modes.

    Args:
        value (str): The value submitted by the form, typically
            "student" or "professional".

    Returns:
        Profile: A new Profile instance initialized with appropriate
        metrics and mode information.

    Examples:
        Normal case:
            - Calling get_profile_from_form_value("student") returns
              a Student Life profile with predefined starting metrics.

        Edge case 1:
            - Calling get_profile_from_form_value("professional")
              returns the Professional Life profile.

        Edge case 2:
            - Calling get_profile_from_form_value("unknown") safely
              defaults to the Professional Life profile instead of
              raising an error.
    """

    # Check whether the form value matches the student profile
    if value == "student":
        # Return a predefined Student Life profile with balanced
        # academic and wellbeing-focused starting metrics
        return Profile(
            name="Student Life",
            initial_metrics={
                "academics": 60,
                "wellbeing": 55,
                "social": 50,
                "career_readiness": 45,
            },
            mode="student",
        )

    # Default to the Professional Life profile if no match is found
    return Profile(
        name="Professional Life",
        initial_metrics={
            "career": 60,
            "finances": 50,
            "work_life_balance": 45,
            "relationships": 50,
        },
        mode="professional",
    )


def build_custom_profile(metric_names: list[str], activity_labels: list[str]) -> Profile:
    """
    Construct a custom simulation profile from user-provided inputs.

    This function creates a Profile object using metric names and
    activity labels supplied by the user. Metric names are normalized
    for internal use, and all metrics start at a neutral baseline value.

    Args:
        metric_names (list[str]): A list of metric names entered by
            the user (e.g., ["Energy", "Discipline"]).
        activity_labels (list[str]): A list of activity labels that
            describe the types of daily scenarios in the simulation.

    Returns:
        Profile: A Profile instance configured for custom simulation
        mode.

    Examples:
        Normal case:
            - Providing ["Energy", "Focus"] creates a Custom Life
              profile with both metrics initialized to 50.

        Edge case 1:
            - Providing an empty metric list causes the function to
              fall back to a default set of metrics.

        Edge case 2:
            - Providing metric names with spaces (e.g., "Work Life")
              results in keys being converted to snake_case.
    """

    # Check whether any metric names were provided
    if not metric_names:
        # Fall back to a default set of metrics if the list is empty
        metric_names = ["Energy", "Wellbeing", "Productivity"]

    # Initialize an empty dictionary to store normalized metrics
    metrics: dict[str, int] = {}

    # Loop through each provided metric name
    for name in metric_names:
        # Convert the name to lowercase and replace spaces with underscores
        key = name.lower().replace(" ", "_")

        # Initialize the metric to a neutral baseline value
        metrics[key] = 50

    # Create and return the Custom Life profile
    return Profile(
        name="Custom Life",
        initial_metrics=metrics,
        mode="custom",
        activity_labels=activity_labels,
    )

