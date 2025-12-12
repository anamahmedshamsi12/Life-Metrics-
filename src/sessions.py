"""
sessions.py

Defines the Session class, which represents a single run of the
Life Metrics Simulator.

A Session:
- Tracks the current day number
- Holds the current metric values (e.g., academics, wellbeing)
- Applies activities (deterministic effects) and random events (small noise)
- Stores daily log entries written by the user

This module focuses on simulation mechanics and does not handle any
web or UI concerns. Keeping this logic separate from Flask routes
follows the modular design principles emphasized in CS5001 and makes
it easier to test and maintain.
"""

# Import the random module to introduce small stochastic events
import random


class Session:
    """
    Represents one active simulation session.

    Attributes:
        profile (Profile):
            The Profile object used to initialize this session.

        day (int):
            The current day in the simulation (starting from 1).

        metrics (dict[str, int]):
            Mutable mapping of metric names to their current values in [0, 100].

        logs (list[dict]):
            List of daily log entries.
            Each entry is a dict with keys:
                - "day" (int): day the entry was recorded
                - "note" (str): free-form user text
                - "mood" (int | None): optional mood rating
    """

    def __init__(self, profile):
        """
        Initialize a new Session from a given Profile.

        This constructor uses the provided Profile to seed the simulation
        with initial metric values and sets the starting day number.

        Args:
            profile (Profile): The profile whose initial_metrics and mode
                will seed this session.

        Returns:
            None

        Examples:
            Normal case:
                - Creating Session(student_profile) sets day to 1 and copies
                  the initial metrics from student_profile.

            Edge case 1:
                - If profile.initial_metrics is an empty dictionary, the
                  session still initializes, but metrics remain empty.

            Edge case 2:
                - If the same Profile instance is reused across multiple
                  Session objects, each Session still maintains its own
                  independent copy of metrics.
        """

        # Store the Profile object used to configure this session
        self.profile = profile

        # Initialize the simulation day counter at 1
        self.day = 1

        # Copy the initial metrics so the original profile is not mutated
        self.metrics = profile.initial_metrics.copy()

        # Initialize an empty list to store daily log entries
        self.logs: list[dict] = []

    # --------------------------------------------------------------------- #
    # Core simulation mechanics                                            #
    # --------------------------------------------------------------------- #

    def apply_activity(self, activity_name: str, effects: dict) -> None:
        """
        Apply an activity's effects to the current metrics.

        This method applies deterministic changes to the session's metrics
        based on the provided effects dictionary. Each affected metric is
        updated and then clamped into the valid range [0, 100].

        Args:
            activity_name (str):
                Human-readable label for the activity. This argument is
                currently not stored inside the Session, but it can be used
                by the caller for logging or UI display.
            effects (dict[str, int]):
                Mapping from metric name to change in value. For example,
                {"academics": +5, "wellbeing": -2}.

        Returns:
            None

        Examples:
            Normal case:
                - If metrics["academics"] is 60 and effects["academics"]
                  is +5, the new value becomes 65.

            Edge case 1:
                - If effects includes a metric that does not exist in
                  self.metrics, that entry is ignored safely.

            Edge case 2:
                - If applying the delta would push a metric below 0 or
                  above 100, the result is clamped to stay within [0, 100].
        """

        # Loop over each metric and its delta in the provided effects
        for metric, delta in effects.items():
            # Only apply changes to metrics that exist in this session
            if metric in self.metrics:
                # Compute the new value by adding the delta
                new_value = self.metrics[metric] + delta

                # Clamp the new metric value into the valid range [0, 100]
                self.metrics[metric] = max(0, min(100, new_value))

    def maybe_apply_random_event(self) -> None:
        """
        Optionally apply a small random adjustment to metrics.

        This method models unpredictable life events by adding a small
        random change to each metric with a fixed probability. The changes
        are intentionally small so user choices remain the main driver of
        the simulation.

        Args:
            None

        Returns:
            None

        Examples:
            Normal case:
                - On some calls, metrics may shift by -2, -1, or +1, but
                  only when the random check passes.

            Edge case 1:
                - If metrics is empty, the function does nothing and
                  returns safely.

            Edge case 2:
                - If random.random() is always >= 0.2 (for example, due
                  to a seeded random state), no random events are applied.
        """

        # Draw a random float in [0, 1) and apply random effects
        # with 20% probability
        if random.random() < 0.2:
            # Loop over each metric in the session
            for metric in self.metrics:
                # Choose a small random delta to apply
                delta = random.choice([-2, -1, 1])

                # Compute the new value by adding the delta
                new_value = self.metrics[metric] + delta

                # Clamp the updated value into the valid range [0, 100]
                self.metrics[metric] = max(0, min(100, new_value))

    def end_day(self) -> None:
        """
        Advance the simulation to the next day.

        This method is called after activities (and any random events)
        have been applied so that the internal day counter reflects the
        end-of-day state.

        Args:
            None

        Returns:
            None

        Examples:
            Normal case:
                - If self.day is 3, calling end_day() updates it to 4.

            Edge case 1:
                - If end_day() is called multiple times in a row without
                  any activities, the day counter continues to increment.

            Edge case 2:
                - If self.day starts at an unusually large value, the
                  method still increments it by exactly 1.
        """

        # Increment the current day number by one
        self.day += 1

    # --------------------------------------------------------------------- #
    # Daily log management                                                 #
    # --------------------------------------------------------------------- #

    def add_log_entry(self, note: str, mood) -> None:
        """
        Record a daily log entry for the current day.

        This method stores a single log entry containing the current day
        number, the user's note, and an optional mood rating. These logs
        can later be displayed or analyzed.

        Args:
            note (str):
                Free-form text written by the user. This may be an empty
                string if the user only wants to record a mood.
            mood (int | None):
                Optional numeric mood rating (e.g., from 0 to 10). If mood
                parsing fails upstream, this value may be None.

        Returns:
            None

        Examples:
            Normal case:
                - Calling add_log_entry("Felt productive", 8) appends a
                  new log dictionary with the current day, note, and mood.

            Edge case 1:
                - Passing an empty string for note and a valid mood still
                  records the entry, allowing mood-only tracking.

            Edge case 2:
                - Passing mood as None still records the entry, which
                  makes it robust to parsing or validation issues.
        """

        # Append a new log entry dictionary to the logs list
        self.logs.append(
            {
                # Store which day this log entry is associated with
                "day": self.day,

                # Store the free-form note entered by the user
                "note": note,

                # Store the optional mood rating for this day
                "mood": mood,
            }
        )

