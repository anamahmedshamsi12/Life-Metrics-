"""
app.py

This file serves as the main Flask application for the Life Metrics project.
It is responsible for handling all web-related behavior, including routing
HTTP requests, managing user session state, and rendering HTML templates.

The core simulation logic (such as metric updates, decision effects, and
recursive trend analysis) is intentionally separated into simulation.py.
This separation helps keep the code organized and readable by isolating
program logic from user interface and routing concerns.

"""
# Import Flask and utilities for handling requests, redirects, templates,
# and sessions
from flask import Flask, render_template, request, redirect, url_for, session

# Import all simulation logic from the simulation module
from simulation import (
    TIME_SLOTS,
    PROFILES,
    start_profile,
    build_custom_profile,
    log_check_in,
    compute_score,
    recursive_metric_trend,
)

# Import the SQLite persistence layer for runs and check-ins
import db

# Create the Flask application instance
app = Flask(__name__)

# Set a secret key so Flask sessions can be securely signed
app.secret_key = "life-metrics-secret-key"

# Ensure the SQLite tables exist before handling any requests
db.init_db()


@app.route("/")
def index():
    """
    Display the landing page where the user selects a simulation mode.

    This function handles requests to the root URL ("/") and renders the
    main menu of the application. From this page, the user can choose to
    start a Student Life simulation, a Professional Life simulation, or
    create a Custom Life simulation.

    Args:
        None

    Returns:
        Response: A rendered HTML response for the index.html template,
        which displays the main menu and mode selection buttons.

    Examples:
        Normal case:
            - A user navigates to "http://127.0.0.1:5000/" and sees the
              main menu with options for Student, Professional, and Custom modes.

        Edge case 1:
            - A user returns to "/" after resetting the simulation, and
              the menu is shown again with no session data required.

        Edge case 2:
            - A user directly visits "/" without any active session, and
              the page still loads correctly since this route does not
              depend on session state.
    """
    # Render and return the main menu page
    return render_template("index.html")


@app.route("/start", methods=["GET", "POST"])
def start():
    """
    Initialize a built-in simulation for either the Student or Professional mode.

    This route is responsible for starting a new simulation using one of the
    predefined profiles. It supports both GET requests (using a query
    parameter in the URL) and POST requests (using form data submitted
    from the landing page).

    Once a valid profile is selected, this function initializes all required
    session state, including metrics, available actions, the current day,
    and an empty log of check-ins, before redirecting the user to the main
    simulation view.

    Args:
        None

    Returns:
        Response: A redirect response to the "/simulate" route if a valid
        profile is provided, or a redirect back to the index page if the
        profile is invalid or missing.

    Examples:
        Normal case:
            - A user clicks "Student Life" on the main menu, which sends
              a request to "/start?profile=student". The simulation is
              initialized and the user is redirected to the simulation page.

        Edge case 1:
            - A user manually navigates to "/start" without providing a
              profile parameter. Since no valid profile is found, the user
              is redirected back to the main menu.

        Edge case 2:
            - A user provides an invalid profile value (e.g., "/start?profile=unknown").
              The function safely detects that the profile does not exist
              and redirects the user to the index page instead of crashing.
    """

    # Attempt to read the selected profile from the URL or submitted form
    profile_key = request.args.get("profile") or request.form.get("profile")

    # Verify that the requested profile exists
    if profile_key not in PROFILES:
        # Redirect to the menu if the profile is invalid
        return redirect(url_for("index"))

    # Initialize the selected profile using core simulation logic
    mode, metrics, actions = start_profile(profile_key)

    # Clear any previous session data
    session.clear()

    # Create a persistent run record so this simulation's history survives
    # across sessions, and remember its id for logging check-ins later
    session["run_id"] = db.create_run(mode, None)

    # Store simulation state in the session
    session["mode"] = mode
    session["metrics"] = metrics
    session["actions"] = actions
    session["day"] = 1

    # Start at the first time slot (Morning)
    session["moment_index"] = 0

    # Initialize an empty log to track all check-ins
    session["log"] = []

    # Redirect to the main simulation view
    return redirect(url_for("simulate"))


@app.route("/custom_setup", methods=["GET", "POST"])
def custom_setup():
    """
    Display and process the setup form for a custom life simulation.

    This route allows the user to define their own simulation by choosing
    custom metric names and writing descriptions for three types of daily
    scenarios (positive, neutral, and challenging). It supports both
    displaying the setup form and processing the submitted form data.

    On submission, the function builds a custom profile using helper logic
    from simulation.py, initializes the session state, and redirects the
    user to the main simulation page.

    Args:
        None

    Returns:
        Response: A rendered HTML response displaying the custom setup form
        when accessed via GET, or a redirect response to the "/simulate"
        route after successfully processing a POST request.

    Examples:
        Normal case:
            - A user navigates to "/custom_setup", fills in custom metric
              names and scenario descriptions, submits the form, and is
              redirected to the simulation page with their custom profile.

        Edge case 1:
            - A user submits the form with some metric fields left blank.
              These values are safely ignored or replaced with defaults
              during profile creation.

        Edge case 2:
            - A user refreshes the "/custom_setup" page without submitting
              the form. The setup page is simply re-rendered with no changes
              to session state.
    """

    # Check whether the form has been submitted
    if request.method == "POST":

        # Collect raw metric names from the form (may include blanks)
        raw_metrics = [
            request.form.get("metric1", ""),
            request.form.get("metric2", ""),
            request.form.get("metric3", ""),
            request.form.get("metric4", ""),
            request.form.get("metric5", ""),
        ]

        # Read the custom action labels and descriptions, applying defaults
        strong_label = request.form.get(
            "strong_label", "").strip() or "High-momentum day"
        strong_desc = (
            request.form.get("strong_desc", "").strip()
            or "You felt focused, aligned, and made real progress."
        )

        steady_label = request.form.get(
            "steady_label", "").strip() or "Steady day"
        steady_desc = (
            request.form.get("steady_desc", "").strip()
            or "A normal day with small wins and some tradeoffs."
        )

        tough_label = request.form.get(
            "tough_label", "").strip() or "Tough day"
        tough_desc = (
            request.form.get("tough_desc", "").strip()
            or "A day that left you more depleted than recharged."
        )

        # Build the custom profile using simulation logic
        mode, clean_metric_names, metrics, actions = build_custom_profile(
            raw_metrics,
            strong_label,
            strong_desc,
            steady_label,
            steady_desc,
            tough_label,
            tough_desc,
        )

        # Clear any existing session data
        session.clear()

        # Create a persistent run record for this custom simulation
        session["run_id"] = db.create_run(mode, clean_metric_names)

        # Store custom simulation state
        session["mode"] = mode
        session["custom_metrics"] = clean_metric_names
        session["metrics"] = metrics
        session["actions"] = actions
        session["day"] = 1
        session["moment_index"] = 0
        session["log"] = []

        # Redirect to the simulation screen
        return redirect(url_for("simulate"))

    # Render the setup form if this is a GET request
    return render_template("custom_setup.html")


@app.route("/simulate", methods=["GET", "POST"])
def simulate():
    """
    Run and display the main simulation loop for all modes
    (Student, Professional, and Custom).

    This function acts as the core controller for the simulation.
    It handles both displaying the current simulation state (GET)
    and processing user decisions (POST). Each simulated day is
    broken into three time slots: Morning, Afternoon, and Evening.

    During a POST request, the user's selected scenario is applied,
    metrics are updated, the action is logged, and the simulation
    advances to the next time slot or day. During a GET request,
    the current state of the simulation is rendered for the user.

    Args:
        None

    Returns:
        Response: A rendered HTML response for the simulation page
        when accessed via GET, or a redirect response back to
        "/simulate" after processing a POST request.

    Examples:
        Normal case:
            - A user selects a scenario during the Morning check-in.
              The system updates metrics, logs the choice, advances
              the time slot, and re-renders the simulation view.

        Edge case 1:
            - A user accesses "/simulate" without an active session
              (for example, after a browser refresh). The function
              safely redirects the user back to the main menu.

        Edge case 2:
            - A user completes the Evening check-in for a day. The
              simulation automatically advances to the next day and
              resets the time slot back to Morning.
    """

    # Read the active simulation mode from the session
    mode = session.get("mode")

    # Redirect to menu if no simulation is active
    if not mode:
        return redirect(url_for("index"))

    # Load current simulation state from the session
    metrics = session.get("metrics", {})
    actions = session.get("actions", [])
    day = session.get("day", 1)
    moment_index = session.get("moment_index", 0)
    log_entries = session.get("log", [])

    # Ensure the time-slot index is valid
    if moment_index < 0 or moment_index >= len(TIME_SLOTS):
        moment_index = 0

    # Handle a submitted check-in
    if request.method == "POST":

        # Read the selected action and optional user note
        action_id = request.form.get("action_id")
        note = request.form.get("note", "").strip()

        # Remember how many entries existed before this check-in so we can
        # tell whether log_check_in actually logged a new one
        entries_before = len(log_entries)

        # Apply the action and update simulation state
        metrics, log_entries, new_day, new_moment_index = log_check_in(
            mode=mode,
            metrics=metrics,
            actions=actions,
            day=day,
            moment_index=moment_index,
            action_id=action_id,
            note=note,
            log_entries=log_entries,
            scale_factor=0.5,
        )

        # Persist updated values back to the session
        session["metrics"] = metrics
        session["log"] = log_entries
        session["day"] = new_day
        session["moment_index"] = new_moment_index

        # Persist this check-in to SQLite so it survives across sessions
        run_id = session.get("run_id")
        if run_id and len(log_entries) > entries_before:
            db.insert_check_in(run_id, action_id, log_entries[-1])

        # Redirect to avoid duplicate form submissions
        return redirect(url_for("simulate"))

    # Render the simulation view

    # Compute an overall balance score from the metrics
    score = compute_score(metrics)

    # Initialize a dictionary to store recursive trend results
    trend_summary = {}

    # Only compute trends if enough log entries exist
    if len(log_entries) >= 2:
        # Compute recursive net change for each metric
        for metric in metrics:
            trend_summary[metric] = recursive_metric_trend(
                log_entries, metric
            )

    # Load custom metric labels if in custom mode
    custom_metrics = session.get(
        "custom_metrics") if mode == "custom" else None

    # Determine the current time-of-day label
    time_label = TIME_SLOTS[moment_index]

    # Compute display-friendly check-in counters
    check_in = moment_index + 1
    total_check_ins = len(TIME_SLOTS)

    # Render the simulation template with all state data
    return render_template(
        "simulate.html",
        mode=mode,
        metrics=metrics,
        actions=actions,
        day=day,
        log=log_entries,
        score=score,
        custom_metrics=custom_metrics,
        time_label=time_label,
        check_in=check_in,
        total_check_ins=total_check_ins,
        trend_summary=trend_summary,
    )


@app.route("/trends")
def trends():
    """
    Display a line-chart dashboard of how each metric has changed over
    time for the currently active run.

    This route reads every check-in stored in SQLite for the run tied to
    the current session, builds one labeled value series per metric, and
    hands that data to the trends template for client-side charting with
    Chart.js.

    Args:
        None

    Returns:
        Response: A rendered HTML response for the trends.html template
        when a run is active, or a redirect to the index page if there
        is no active run (e.g. after a reset or before starting).

    Examples:
        Normal case:
            - A user with at least one logged check-in visits "/trends"
              and sees one line chart per metric.

        Edge case 1:
            - A user visits "/trends" before making any check-ins. The
              page renders with an empty-state message instead of charts.

        Edge case 2:
            - A user visits "/trends" without an active session (no
              run_id). They are redirected back to the main menu.
    """

    # Read the active run and mode from the session
    run_id = session.get("run_id")
    mode = session.get("mode")

    # Redirect to the menu if there is no active run to chart
    if not run_id or not mode:
        return redirect(url_for("index"))

    # Fetch every check-in logged so far for this run from SQLite
    check_ins = db.get_check_ins_for_run(run_id)

    # Build one series per metric: a list of labels and a list of values
    series: dict[str, dict[str, list]] = {}
    for entry in check_ins:
        label = f"Day {entry['day']} · {entry['time_label']}"
        for metric_name, value in entry["metrics"].items():
            series.setdefault(metric_name, {"labels": [], "values": []})
            series[metric_name]["labels"].append(label)
            series[metric_name]["values"].append(value)

    # Load custom metric labels if in custom mode
    custom_metrics = session.get(
        "custom_metrics") if mode == "custom" else None

    # Render the trends template with the chart data
    return render_template(
        "trends.html",
        mode=mode,
        series=series,
        custom_metrics=custom_metrics,
    )


@app.route("/reset")
def reset():
    """
    Clear the current simulation state and return the user to the main menu.

    This route removes all stored session data related to the active
    simulation, including metrics, logs, and progress. It allows the
    user to safely restart the application or choose a different
    simulation mode without residual data from a previous run.

    Args:
        None

    Returns:
        Response: A redirect response to the index ("/") route,
        where the user can select a new simulation mode.

    Examples:
        Normal case:
            - A user clicks a "Back to Menu" or "Reset" button during
              a simulation and is returned to the main menu with a
              fresh session.

        Edge case 1:
            - A user visits "/reset" when no simulation is active.
              The function still works correctly because clearing an
              empty session does not cause an error.

        Edge case 2:
            - A user refreshes the page after calling "/reset".
              The session remains empty and the menu page is shown
              without any unexpected behavior.
    """

    # Clear all session data
    session.clear()

    # Redirect back to the landing page
    return redirect(url_for("index"))


# Run the Flask development server when executed directly
if __name__ == "__main__":
    app.run(debug=True)
