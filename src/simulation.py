"""
simulation.py

Core simulation logic for the Life Metrics project.

This module is independent of Flask so it can be tested directly.
It defines:

- Built-in profiles (student and professional), including their
  starting metrics and available actions.
- Rules for applying metric changes at each check-in.
- Helper functions to start profiles, apply daily decisions, and
  compute an overall balance score.
- A recursive helper that looks at how a single metric changes
  over time based on the log entries.
"""

from typing import Dict, List, Tuple, Any

# Each simulated day is split into three check-ins.
TIME_SLOTS: List[str] = ["Morning", "Afternoon", "Evening"]

# Built-in profiles for the student and professional modes.
PROFILES: Dict[str, Dict[str, Any]] = {
    # Student Life profile
    "student": {
        "mode": "student",
        "metrics": {
            "Academics": 70,
            "Mental Health": 70,
            "Social Life": 65,
            "Sleep": 60,
            "Finances": 55,
            "Family": 72,
            "Friendships": 68,
            "Relationships": 65,
        },
        "actions": [
            {
                "id": "night_library_grind",
                "label": "Night library grind before a deadline",
                "description": (
                    "You stay late on campus or at home grinding through readings, "
                    "problem sets, or a project. You turn things in on time, "
                    "but sleep and social time take a hit."
                ),
                "deltas": {
                    "Academics": +7,
                    "Sleep": -5,
                    "Mental Health": -2,
                    "Social Life": -3,
                    "Friendships": -2,
                    "Relationships": -2,
                },
            },
            {
                "id": "back_to_back_plans",
                "label": "Back-to-back plans and late-night hangout",
                "description": (
                    "You say yes to every plan: coffee with friends, a club event, "
                    "and a late-night hangout. You feel connected, but school and "
                    "rest slide a bit."
                ),
                "deltas": {
                    "Social Life": +6,
                    "Friendships": +6,
                    "Relationships": +4,
                    "Sleep": -4,
                    "Academics": -3,
                    "Finances": -2,
                },
            },
            {
                "id": "family_day_light_work",
                "label": "Family check-in + light schoolwork",
                "description": (
                    "You spend intentional time with family (calls or in person), "
                    "do a smaller amount of schoolwork, and keep the evening low-key."
                ),
                "deltas": {
                    "Family": +5,
                    "Relationships": +3,
                    "Mental Health": +4,
                    "Academics": +1,
                    "Social Life": 0,
                    "Sleep": +1,
                    "Finances": -1,
                },
            },
            {
                "id": "mental_health_reset",
                "label": "Mental health reset & boundaries",
                "description": (
                    "You protect a slower day: rest, therapy, journaling, or a long walk. "
                    "You say no to extra plans and keep school tasks minimal."
                ),
                "deltas": {
                    "Mental Health": +7,
                    "Sleep": +3,
                    "Academics": -2,
                    "Social Life": -1,
                    "Friendships": 0,
                    "Relationships": +2,
                    "Finances": -1,
                },
            },
        ],
    },

    # Professional Life profile
    "professional": {
        "mode": "professional",
        "metrics": {
            "Career Growth": 70,
            "Mental Health": 65,
            "Work-Life Balance": 60,
            "Finances": 75,
            "Physical Health": 60,
            "Family": 70,
            "Friendships": 65,
            "Relationships": 65,
        },
        "actions": [
            {
                "id": "emergency_late_meeting",
                "label": "Emergency late meeting and after-hours emails",
                "description": (
                    "A project blows up or a deadline moves up. You stay online late, "
                    "answer messages, and push work forward at the cost of rest and "
                    "personal time."
                ),
                "deltas": {
                    "Career Growth": +7,
                    "Finances": +1,
                    "Work-Life Balance": -6,
                    "Mental Health": -4,
                    "Physical Health": -2,
                    "Family": -3,
                    "Friendships": -3,
                    "Relationships": -3,
                },
            },
            {
                "id": "protected_nine_to_five",
                "label": "Protected 9–5 with a real evening",
                "description": (
                    "You work solid hours, then actually log off: no email, no extra tasks. "
                    "You cook, rest, see loved ones, or do something just for you."
                ),
                "deltas": {
                    "Work-Life Balance": +7,
                    "Mental Health": +4,
                    "Family": +3,
                    "Friendships": +3,
                    "Relationships": +3,
                    "Career Growth": -1,
                    "Finances": 0,
                    "Physical Health": +2,
                },
            },
            {
                "id": "deep_focus_block",
                "label": "Deep-focus work block with breaks",
                "description": (
                    "You carve out a focused block for meaningful work, limit meetings, "
                    "and take real breaks. You do a bit less socializing after work "
                    "to recover."
                ),
                "deltas": {
                    "Career Growth": +5,
                    "Mental Health": +2,
                    "Physical Health": +2,
                    "Work-Life Balance": +1,
                    "Family": 0,
                    "Friendships": -1,
                    "Relationships": 0,
                    "Finances": +1,
                },
            },
            {
                "id": "weekend_fully_offline",
                "label": "Weekend fully offline from work",
                "description": (
                    "You ignore work notifications, don’t touch your inbox, and lean into "
                    "rest, hobbies, and people you care about."
                ),
                "deltas": {
                    "Mental Health": +6,
                    "Work-Life Balance": +6,
                    "Family": +4,
                    "Friendships": +4,
                    "Relationships": +4,
                    "Physical Health": +3,
                    "Career Growth": -2,
                    "Finances": -1,
                },
            },
        ],
    },
}


def clamp(value: int) -> int:
    """
    Clamp a metric value into the inclusive range [0, 100].

    Args:
        value (int): Original metric value.

    Returns:
        int: Value forced into the range from 0 to 100.

    Examples:
        Normal case:
            - clamp(75) returns 75.

        Edge case 1:
            - clamp(-10) returns 0.

        Edge case 2:
            - clamp(150) returns 100.
    """
    return max(0, min(100, value))


def compute_score(metrics: Dict[str, int]) -> int:
    """
    Compute a simple overall balance score for the current metrics.

    The score is defined as the rounded average of all metric values.

    Args:
        metrics (Dict[str, int]): Dictionary mapping metric names to
            their current integer values.

    Returns:
        int: Overall score representing the average of all metrics.
        Returns 0 if the metrics dictionary is empty.

    Examples:
        Normal case:
            - Given {"A": 70, "B": 80}, compute_score returns 75.

        Edge case 1:
            - Given an empty dictionary, compute_score returns 0.

        Edge case 2:
            - Given a single metric {"A": 63}, compute_score returns 63.
    """
    if not metrics:
        return 0
    return round(sum(metrics.values()) / len(metrics))


def apply_scaled_deltas(
    metrics: Dict[str, int],
    deltas: Dict[str, int],
    factor: float = 0.5,
) -> None:
    """
    Apply scaled metric deltas for a micro check-in in built-in modes.

    The raw deltas in PROFILES represent a full-day effect. This
    function scales them down so that 2–3 micro check-ins roughly
    match the impact of one intense day.

    Args:
        metrics (Dict[str, int]): Dictionary of current metric values.
            This dictionary is updated in place.
        deltas (Dict[str, int]): Dictionary mapping metric names to
            full-day delta values.
        factor (float): Multiplier used to scale the deltas for a
            single check-in. Defaults to 0.5.

    Returns:
        None

    Examples:
        Normal case:
            - If "Academics" is 60 and deltas["Academics"] is +10
              with factor 0.5, the metric becomes 65.

        Edge case 1:
            - If a metric is missing from metrics, it is treated as
              base 50 for that calculation.

        Edge case 2:
            - If scaling produces 0 but the original delta is non-zero,
              the function nudges the metric by +/- 1 so the action
              still has an effect.
    """
    for metric_name, delta in deltas.items():
        base = metrics.get(metric_name, 50)
        scaled = int(delta * factor)

        if scaled == 0 and delta != 0:
            scaled = 1 if delta > 0 else -1

        metrics[metric_name] = clamp(base + scaled)


def apply_custom_effect(metrics: Dict[str, int], action_id: str) -> None:
    """
    Apply gentle, generic changes for the custom life mode.

    strong_day  -> small positive bump for all metrics.
    tough_day   -> small negative bump for all metrics.
    steady_day  -> mixed: some metrics up, others slightly down.

    Args:
        metrics (Dict[str, int]): Dictionary of current metric values.
            This dictionary is updated in place.
        action_id (str): Identifier of the selected custom action.

    Returns:
        None

    Examples:
        Normal case:
            - For a "strong_day", all metrics increase by a small amount
              and remain clamped in [0, 100].

        Edge case 1:
            - If metrics is empty, the function returns immediately
              without attempting any updates.

        Edge case 2:
            - For a "steady_day" with an odd number of metrics, the last
              metric still receives a valid delta based on its index.
    """
    names = list(metrics.keys())
    if not names:
        return

    if action_id == "strong_day":
        for name in names:
            metrics[name] = clamp(metrics[name] + 3)
    elif action_id == "tough_day":
        for name in names:
            metrics[name] = clamp(metrics[name] - 3)
    else:
        # "Steady day": alternate small boosts and small dips.
        for index, name in enumerate(names):
            delta = 2 if index % 2 == 0 else -1
            metrics[name] = clamp(metrics[name] + delta)


def start_profile(
    profile_key: str,
) -> Tuple[str, Dict[str, int], List[Dict[str, Any]]]:
    """
    Initialize a built-in profile by key.

    This function looks up the profile in the PROFILES dictionary,
    copies its starting metrics, and returns the mode, metrics, and
    actions used by that profile.

    Args:
        profile_key (str): Key in the PROFILES dictionary
            (e.g., "student" or "professional").

    Returns:
        Tuple[str, Dict[str, int], List[Dict[str, Any]]]: A tuple
        (mode, metrics, actions) where:
            - mode: String identifying the mode (e.g., "student").
            - metrics: Copy of the starting metrics for the profile.
            - actions: List of action dictionaries for this profile.

    Raises:
        KeyError: If profile_key is not found in PROFILES.

    Examples:
        Normal case:
            - start_profile("student") returns the student mode string,
              its starting metrics, and its actions list.

        Edge case 1:
            - start_profile("professional") returns the professional
              configuration.

        Edge case 2:
            - start_profile("unknown") raises a KeyError, signaling that
              the caller must handle invalid profile keys.
    """
    profile = PROFILES[profile_key]
    mode = profile["mode"]
    metrics = profile["metrics"].copy()
    actions = profile["actions"]
    return mode, metrics, actions


def build_custom_profile(
    metric_names: List[str],
    strong_label: str,
    strong_desc: str,
    steady_label: str,
    steady_desc: str,
    tough_label: str,
    tough_desc: str,
) -> Tuple[str, List[str], Dict[str, int], List[Dict[str, str]]]:
    """
    Build a custom profile from user-provided metric names and labels.

    This helper creates the configuration for a custom simulation mode
    by cleaning up metric names and using labels/descriptions for three
    daily patterns: strong, steady, and tough days.

    Args:
        metric_names (List[str]): List of metric names. Empty or
            whitespace-only entries are filtered out.
        strong_label (str): Label for the "strong" day pattern.
        strong_desc (str): Description for the "strong" day pattern.
        steady_label (str): Label for the "steady" day pattern.
        steady_desc (str): Description for the "steady" day pattern.
        tough_label (str): Label for the "tough" day pattern.
        tough_desc (str): Description for the "tough" day pattern.

    Returns:
        Tuple[str, List[str], Dict[str, int], List[Dict[str, str]]]:
        A tuple (mode, metric_names_clean, metrics, actions) where:
            - mode: The string "custom".
            - metric_names_clean: Final list of cleaned metric names.
            - metrics: Starting metric dictionary with values initialized.
            - actions: List of custom action dictionaries.

    Examples:
        Normal case:
            - Providing ["Energy", "Focus"] and custom labels builds a
              custom profile with both metrics starting at 70.

        Edge case 1:
            - If metric_names contains only blanks or empty strings,
              a default list of metrics is used instead.

        Edge case 2:
            - If labels or descriptions are very short, the profile still
              builds correctly since this function does not enforce length.
    """
    metric_names_clean = [m.strip() for m in metric_names if m.strip()]

    if not metric_names_clean:
        metric_names_clean = ["Energy", "Focus", "Connection", "Stability"]

    metrics = {name: 70 for name in metric_names_clean}

    actions = [
        {"id": "strong_day", "label": strong_label, "description": strong_desc},
        {"id": "steady_day", "label": steady_label, "description": steady_desc},
        {"id": "tough_day", "label": tough_label, "description": tough_desc},
    ]

    return "custom", metric_names_clean, metrics, actions


def log_check_in(
    mode: str,
    metrics: Dict[str, int],
    actions: List[Dict[str, Any]],
    day: int,
    moment_index: int,
    action_id: str,
    note: str,
    log_entries: List[Dict[str, Any]],
    scale_factor: float = 0.5,
) -> Tuple[Dict[str, int], List[Dict[str, Any]], int, int]:
    """
    Apply the selected action, log the check-in, and advance the moment/day.

    This function:
    1. Finds the selected action by its ID.
    2. Applies metric changes (scaled or custom).
    3. Logs the current snapshot with a note.
    4. Advances the time slot and possibly the day.

    Args:
        mode (str): Current mode ("student", "professional", or "custom").
        metrics (Dict[str, int]): Current metrics dictionary, updated in place.
        actions (List[Dict[str, Any]]): List of available action dictionaries.
        day (int): Current simulated day number.
        moment_index (int): Index into TIME_SLOTS for the current check-in.
        action_id (str): Identifier of the chosen action.
        note (str): Optional textual note for this check-in.
        log_entries (List[Dict[str, Any]]): Existing list of log entries,
            updated in place.
        scale_factor (float): Factor used for scaling deltas in non-custom
            modes. Defaults to 0.5.

    Returns:
        Tuple[Dict[str, int], List[Dict[str, Any]], int, int]: A tuple
        (metrics, log_entries, new_day, new_moment_index) representing the
        updated metrics, updated logs, next day number, and next moment index.

    Examples:
        Normal case:
            - For a valid action_id, metrics are updated, a log entry is
              added, and the moment index advances.

        Edge case 1:
            - If action_id does not match any action, this function returns
              the state unchanged.

        Edge case 2:
            - If moment_index is out of range, it is normalized back to 0
              before logging and advancing.
    """
    selected = next((a for a in actions if a.get("id") == action_id), None)
    if selected is None:
        return metrics, log_entries, day, moment_index

    if mode == "custom":
        apply_custom_effect(metrics, action_id)
    else:
        deltas = selected.get("deltas", {})
        apply_scaled_deltas(metrics, deltas, factor=scale_factor)

    if moment_index < 0 or moment_index >= len(TIME_SLOTS):
        moment_index = 0

    time_label = TIME_SLOTS[moment_index]

    log_entries.append(
        {
            "day": day,
            "moment": moment_index + 1,
            "time_label": time_label,
            "action_label": selected.get("label", ""),
            "snapshot": metrics.copy(),
            "note": note,
        }
    )

    new_moment_index = moment_index + 1
    new_day = day
    if new_moment_index >= len(TIME_SLOTS):
        new_moment_index = 0
        new_day += 1

    return metrics, log_entries, new_day, new_moment_index


def recursive_metric_trend(
    log_entries: List[Dict[str, Any]],
    metric_name: str,
    index: int = 0,
) -> int:
    """
    Recursively compute the net change of a metric over time.

    This function walks through the list of log entries one step at a time.
    At each step, it compares the metric in the current snapshot with the
    metric in the next snapshot and adds that difference to the result.

    Base case:
        - When index reaches the final entry, the function returns 0.

    Recursive case:
        - Compute the difference between the current and next snapshot
          for the given metric, then add that to the result of the
          recursive call on the next index.

    Args:
        log_entries (List[Dict[str, Any]]): List of logged simulation
            entries, each containing a "snapshot" dictionary.
        metric_name (str): Name of the metric to analyze.
        index (int): Current index in the recursion, starting from 0.

    Returns:
        int: Net change of the specified metric across all log entries.

    Examples:
        Normal case:
            - If a metric moves from 60 to 65 to 70 across three snapshots,
              recursive_metric_trend returns +10.

        Edge case 1:
            - If there are fewer than 2 log entries, the function returns 0
              since no change can be measured.

        Edge case 2:
            - If a snapshot does not contain the given metric, its value
              defaults to 0 for that comparison.
    """
    if index >= len(log_entries) - 1:
        return 0

    current_value = log_entries[index]["snapshot"].get(metric_name, 0)
    next_value = log_entries[index + 1]["snapshot"].get(metric_name, 0)
    difference = next_value - current_value

    return difference + \
        recursive_metric_trend(log_entries, metric_name, index + 1)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
