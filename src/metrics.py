"""
metrics.py

This module contains utility functions used to initialize, update, and
manage life metrics within the Life Metrics Simulator. Each metric
represents a dimension of a user's life (such as sleep, productivity,
or well-being) and is stored as an integer value between 0 and 100.

The functions in this file are designed to be reusable and independent
from the web application layer. They focus only on data manipulation and
validation, not us2$er interaction or display logic.

By separating metric-related logic into this module, the project follows
the modular design principles emphasized in CS5001, making the codebase
easier to understand, test, and maintain.
"""
# Enable postponed evaluation of type annotations (PEP 563 style),
# which allows us to use forward references in type hints
from __future__ import annotations

# Import typing helpers for clearer type annotations
from typing import Dict, List

# Define a type alias for the metrics dictionary
# Keys are metric names (strings), values are integers between 0 and 100
MetricDict = Dict[str, int]

# Define a type alias for metric delta dictionaries
# Keys are metric names, values are integer changes to apply
DeltaDict = Dict[str, int]

# Preset metric names for each built-in simulation mode
# These lists define which metrics exist for each profile
DEFAULT_METRICS = {
    # Metrics used in Student Life mode
    "student": [
        "Academics",
        "Wellbeing",
        "Social life",
        "Energy",
        "Finances",
    ],
    # Metrics used in Professional Life mode
    "professional": [
        "Career growth",
        "Work–life balance",
        "Wellbeing",
        "Finances",
        "Burnout",
    ],
    # Custom mode does not use preset metrics and is handled separately
}


def init_metrics(mode: str, custom_metric_names: List[str] | None = None) -> MetricDict:
    """
    Initialize a dictionary of life metrics based on the selected simulation mode.

    This function creates the starting set of metrics for a simulation.
    Each metric begins at a neutral baseline value of 60. The set of
    metrics depends on whether the simulation is running in a built-in
    mode (such as student or professional) or in custom mode.

    Args:
        mode (str): The simulation mode being used. Expected values include
            "student", "professional", or "custom".
        custom_metric_names (List[str] | None): An optional list of metric
            names provided by the user when running a custom simulation.
            This parameter is ignored for non-custom modes.

    Returns:
        MetricDict: A dictionary mapping metric names (strings) to their
        initial integer values, all starting at 60.

    Examples:
        Normal case:
            - Calling init_metrics("student") returns a dictionary with the
              predefined student metrics, each initialized to 60.

        Edge case 1:
            - Calling init_metrics("custom", ["  ", ""]) results in a
              fallback metric named "Primary goal" being created.

        Edge case 2:
            - Calling init_metrics("unknown") uses a default set of generic
              metrics (e.g., Health, Happiness, Productivity) instead of
              raising an error.
    """
    # Check if the simulation is running in custom mode and custom metrics were provided
    if mode == "custom" and custom_metric_names:

        # Clean up metric names by stripping whitespace and removing empty entries
        names = [name.strip() for name in custom_metric_names if name.strip()]
        
        # If no valid metric names remain, fall back to a default placeholder
        if not names:
            names = ["Primary goal"]
    else:
        # Use predefined metrics for student or professional mode,
        # or fall back to a generic default set if the mode is unknown
        names = DEFAULT_METRICS.get(mode, ["Health", "Happiness", "Productivity"])
    # Create and return a dictionary where each metric starts at value 60
    return {name: 60 for name in names}


def apply_deltas(metrics: MetricDict, deltas: DeltaDict) -> MetricDict:
    """
    Apply a set of changes (deltas) to the current life metrics.

    This function updates metric values by applying the corresponding
    delta values provided. Each metric is clamped to remain within the
    valid range of 0 to 100. Any delta that references a metric not
    present in the current metrics dictionary is ignored to prevent
    errors.

    Args:
        metrics (MetricDict): The current dictionary of life metrics,
            where each key is a metric name and each value is an integer
            between 0 and 100.
        deltas (DeltaDict): A dictionary mapping metric names to integer
            changes that should be applied to the current metrics.

    Returns:
        MetricDict: A new dictionary containing the updated metric values
        after all valid deltas have been applied.

    Examples:
        Normal case:
            - Given metrics {"Energy": 60} and deltas {"Energy": -5},
              the function returns {"Energy": 55}.

        Edge case 1:
            - Given metrics {"Energy": 98} and deltas {"Energy": 10},
              the value is clamped and the function returns {"Energy": 100}.

        Edge case 2:
            - Given metrics {"Energy": 60} and deltas {"Sleep": 5},
              the delta is ignored and the original metrics are returned
              unchanged.
    """
    # Create a shallow copy of the metrics dictionary so the original
    # is not mutated directly
    updated = dict(metrics)

    # Loop through each metric delta pair
    for key, delta in deltas.items():
        # Skip any deltas for metrics that are not part of this profile
        if key not in updated:
            continue

        # Compute the new value by applying the delta
        new_value = updated[key] + int(delta)

        # Clamp the new value so it stays between 0 and 100
        updated[key] = max(0, min(100, new_value))

    # Return the updated metrics dictionary
    return updated


def average_score(metrics: MetricDict) -> float:
    """
    Compute the average score across all life metrics.

    This function calculates the arithmetic mean of all metric values
    in the provided metrics dictionary. It is used to generate a simple
    overall balance score for the simulation.

    Args:
        metrics (MetricDict): A dictionary mapping metric names to
            integer values between 0 and 100.

    Returns:
        float: The average of all metric values, rounded to one decimal
        place. If no metrics are provided, the function returns 0.0.

    Examples:
        Normal case:
            - Given metrics {"Energy": 60, "Wellbeing": 80}, the function
              returns 70.0.

        Edge case 1:
            - Given an empty metrics dictionary, the function returns 0.0
              instead of raising an error.

        Edge case 2:
            - Given a single metric {"Focus": 65}, the function returns
              65.0 as the average.
    """
    # Handle the edge case where the metrics dictionary is empty
    if not metrics:
        return 0.0
    # Compute the average metric value and round to one decimal place
    return round(sum(metrics.values()) / len(metrics), 1)
