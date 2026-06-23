"""
app.py

This file serves as the main Flask application for the Life Metrics project.
It is responsible for handling all web-related behavior, including routing
HTTP requests, managing user accounts and session state, and rendering HTML
templates.

The core simulation logic (such as metric updates, decision effects, and
recursive trend analysis) is intentionally separated into simulation.py.
This separation helps keep the code organized and readable by isolating
program logic from user interface and routing concerns. Persistence (user
accounts, runs, and check-ins) lives in models.py.

"""
import json
import os

# Load variables from a local .env file (e.g. DATABASE_URL, SECRET_KEY)
# when running outside of a platform that injects them directly.
from dotenv import load_dotenv

load_dotenv()

# Import Flask and utilities for handling requests, redirects, templates,
# sessions, and flash messages
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

# Import Flask-Login for authenticated user sessions
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

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

# Import the SQLAlchemy persistence layer for users, runs, and check-ins
from models import (
    db,
    User,
    create_run,
    insert_check_in,
    get_check_ins_for_run,
    get_runs_for_user,
    get_owned_run,
)

# Create the Flask application instance
app = Flask(__name__)

# Set a secret key so Flask sessions can be securely signed. In production
# this must come from the SECRET_KEY environment variable.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Resolve the database connection string: use DATABASE_URL when provided
# (e.g. Postgres on Render), otherwise fall back to a local SQLite file.
_database_url = os.environ.get("DATABASE_URL")
if not _database_url:
    _database_url = "sqlite:///" + os.path.join(
        os.path.dirname(__file__), "life_metrics.db"
    )
elif _database_url.startswith("postgres://"):
    # SQLAlchemy/psycopg2 require the "postgresql://" scheme, but some
    # platforms (including Render) still hand out "postgres://" URLs.
    _database_url = _database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = _database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Wire SQLAlchemy into this app and ensure tables exist
db.init_app(app)
with app.app_context():
    db.create_all()

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    """Look up a User by id for Flask-Login's session handling."""
    return db.session.get(User, int(user_id))


# Session keys used to hold live simulation state. Flask-Login stores its
# own auth keys (e.g. "_user_id") in this same session cookie, so clearing
# simulation state must only remove these keys rather than calling
# session.clear(), which would also log the user out.
_SIMULATION_SESSION_KEYS = (
    "run_id",
    "mode",
    "metrics",
    "actions",
    "day",
    "moment_index",
    "log",
    "custom_metrics",
)


def _clear_simulation_session():
    """Remove only the simulation-related keys from the session."""
    for key in _SIMULATION_SESSION_KEYS:
        session.pop(key, None)


@app.route("/")
def index():
    """
    Display the marketing landing page, or send signed-in users straight
    to their dashboard.

    Returns:
        Response: A redirect to "/dashboard" if the visitor is already
        logged in, otherwise a rendered landing.html response.
    """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("landing.html")


@app.route("/modes")
@login_required
def modes():
    """
    Display the simulation mode picker (Student, Professional, Custom).

    Returns:
        Response: A rendered HTML response for the modes.html template.
    """
    return render_template("modes.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Display and process the account registration form.

    Validates that the email is not already registered and that the
    password and confirmation match, hashes the password, creates the
    user, logs them in, and redirects to the dashboard.

    Returns:
        Response: A rendered register.html response, or a redirect to
        "/dashboard" once registration succeeds.
    """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not email or not password:
            flash("Email and password are required.")
        elif password != confirm_password:
            flash("Passwords do not match.")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.")
        else:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Display and process the login form.

    Returns:
        Response: A rendered login.html response, or a redirect to
        "/dashboard" once authentication succeeds.
    """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """
    Log the current user out and return them to the landing page.

    Returns:
        Response: A redirect to "/".
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/start", methods=["GET", "POST"])
@login_required
def start():
    """
    Initialize a built-in simulation for either the Student or Professional mode.

    This route is responsible for starting a new simulation using one of the
    predefined profiles. It supports both GET requests (using a query
    parameter in the URL) and POST requests (using form data submitted
    from the mode picker).

    Once a valid profile is selected, this function initializes all required
    session state, including metrics, available actions, the current day,
    and an empty log of check-ins, before redirecting the user to the main
    simulation view.

    Args:
        None

    Returns:
        Response: A redirect response to the "/simulate" route if a valid
        profile is provided, or a redirect back to the mode picker if the
        profile is invalid or missing.

    Examples:
        Normal case:
            - A user clicks "Student Life" on the mode picker, which sends
              a request to "/start?profile=student". The simulation is
              initialized and the user is redirected to the simulation page.

        Edge case 1:
            - A user manually navigates to "/start" without providing a
              profile parameter. Since no valid profile is found, the user
              is redirected back to the mode picker.

        Edge case 2:
            - A user provides an invalid profile value (e.g., "/start?profile=unknown").
              The function safely detects that the profile does not exist
              and redirects the user to the mode picker instead of crashing.
    """

    # Attempt to read the selected profile from the URL or submitted form
    profile_key = request.args.get("profile") or request.form.get("profile")

    # Verify that the requested profile exists
    if profile_key not in PROFILES:
        # Redirect to the mode picker if the profile is invalid
        return redirect(url_for("modes"))

    # Initialize the selected profile using core simulation logic
    mode, metrics, actions = start_profile(profile_key)

    # Clear any previous simulation session data (without touching login state)
    _clear_simulation_session()

    # Create a persistent run record so this simulation's history survives
    # across sessions, and remember its id for logging check-ins later
    session["run_id"] = create_run(current_user.id, mode, None)

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
@login_required
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

        # Clear any existing simulation session data (without touching login state)
        _clear_simulation_session()

        # Create a persistent run record for this custom simulation. The
        # custom action labels/descriptions are stored too so this run can
        # be fully reconstructed later from the dashboard's "Continue" link.
        session["run_id"] = create_run(
            current_user.id, mode, clean_metric_names, actions
        )

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
@login_required
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
              safely redirects the user back to the mode picker.

        Edge case 2:
            - A user completes the Evening check-in for a day. The
              simulation automatically advances to the next day and
              resets the time slot back to Morning.
    """

    # Read the active simulation mode from the session
    mode = session.get("mode")

    # Redirect to the mode picker if no simulation is active
    if not mode:
        return redirect(url_for("modes"))

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

        # Persist this check-in to the database so it survives across sessions
        run_id = session.get("run_id")
        if run_id and len(log_entries) > entries_before:
            insert_check_in(run_id, action_id, log_entries[-1])

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
@login_required
def trends():
    """
    Display a line-chart dashboard of how each metric has changed over
    time for the currently active run.

    This route reads every check-in stored in the database for the run
    tied to the current session, builds one labeled value series per
    metric, and hands that data to the trends template for client-side
    charting with Chart.js.

    Args:
        None

    Returns:
        Response: A rendered HTML response for the trends.html template
        when a run is active, or a redirect to the mode picker if there
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
              run_id). They are redirected back to the mode picker.
    """

    # Read the active run and mode from the session
    run_id = session.get("run_id")
    mode = session.get("mode")

    # Redirect to the mode picker if there is no active run to chart
    if not run_id or not mode:
        return redirect(url_for("modes"))

    # Fetch every check-in logged so far for this run from the database
    check_ins = get_check_ins_for_run(run_id)

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


def _build_actions_and_baseline(run):
    """
    Determine the actions list and starting-metric baseline for a run.

    Built-in modes look these up from PROFILES; custom mode reconstructs
    them from the run's stored custom_metric_names/custom_actions columns.

    Args:
        run (Run): The run to build actions/baseline for.

    Returns:
        Tuple[list, dict, list | None]: (actions, baseline_metrics,
        custom_metric_names). custom_metric_names is None for built-in modes.
    """
    if run.mode in PROFILES:
        return (
            PROFILES[run.mode]["actions"],
            PROFILES[run.mode]["metrics"],
            None,
        )

    custom_metric_names = (
        json.loads(run.custom_metric_names) if run.custom_metric_names else []
    )
    custom_actions = json.loads(run.custom_actions) if run.custom_actions else []
    baseline_metrics = {name: 70 for name in custom_metric_names}
    return custom_actions, baseline_metrics, custom_metric_names


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Display every run the current user has started, newest first.

    Returns:
        Response: A rendered dashboard.html response listing each run
        with its mode, start date, and check-in count, or an empty-state
        prompt to choose a mode if the user has no runs yet.
    """
    runs = get_runs_for_user(current_user.id)
    run_summaries = [
        {
            "id": run.id,
            "mode": run.mode,
            "created_at": run.created_at,
            "check_in_count": len(get_check_ins_for_run(run.id)),
        }
        for run in runs
    ]
    return render_template("dashboard.html", runs=run_summaries)


@app.route("/dashboard/continue/<int:run_id>")
@login_required
def dashboard_continue(run_id):
    """
    Reconstruct a past run's live simulation state into the session and
    resume it on the "/simulate" page.

    Args:
        run_id (int): The run to resume.

    Returns:
        Response: A redirect to "/simulate" with the run's state loaded
        into the session, or to "/dashboard" if the run does not exist
        or does not belong to the current user.
    """
    run = get_owned_run(run_id, current_user.id)
    if run is None:
        return redirect(url_for("dashboard"))

    actions, baseline_metrics, custom_metric_names = _build_actions_and_baseline(run)
    check_ins = get_check_ins_for_run(run.id)

    if check_ins:
        last = check_ins[-1]
        metrics = dict(last["metrics"])
        if last["moment_index"] < len(TIME_SLOTS):
            day, moment_index = last["day"], last["moment_index"]
        else:
            day, moment_index = last["day"] + 1, 0
        log_entries = [
            {
                "day": entry["day"],
                "moment": entry["moment_index"],
                "time_label": entry["time_label"],
                "action_label": entry["action_label"],
                "snapshot": entry["metrics"],
                "note": entry["note"],
            }
            for entry in check_ins
        ]
    else:
        metrics = dict(baseline_metrics)
        day, moment_index = 1, 0
        log_entries = []

    _clear_simulation_session()
    session["run_id"] = run.id
    session["mode"] = run.mode
    session["metrics"] = metrics
    session["actions"] = actions
    session["day"] = day
    session["moment_index"] = moment_index
    session["log"] = log_entries
    if custom_metric_names:
        session["custom_metrics"] = custom_metric_names

    return redirect(url_for("simulate"))


@app.route("/dashboard/trends/<int:run_id>")
@login_required
def dashboard_trends(run_id):
    """
    Point the session at a past run so "/trends" can chart it.

    Args:
        run_id (int): The run to view trends for.

    Returns:
        Response: A redirect to "/trends", or to "/dashboard" if the run
        does not exist or does not belong to the current user.
    """
    run = get_owned_run(run_id, current_user.id)
    if run is None:
        return redirect(url_for("dashboard"))

    session["run_id"] = run.id
    session["mode"] = run.mode
    if run.custom_metric_names:
        session["custom_metrics"] = json.loads(run.custom_metric_names)

    return redirect(url_for("trends"))


@app.route("/reset")
def reset():
    """
    Clear the current simulation state and return the user to the
    mode picker (or landing page, if logged out).

    This route removes all stored session data related to the active
    simulation, including metrics, logs, and progress. It allows the
    user to safely restart the application or choose a different
    simulation mode without residual data from a previous run.

    Args:
        None

    Returns:
        Response: A redirect response to the mode picker if logged in,
        otherwise to the landing page.

    Examples:
        Normal case:
            - A user clicks a "Back to Menu" or "Reset" button during
              a simulation and is returned to the mode picker with a
              fresh session.

        Edge case 1:
            - A user visits "/reset" when no simulation is active.
              The function still works correctly because clearing an
              empty session does not cause an error.

        Edge case 2:
            - A user refreshes the page after calling "/reset".
              The session remains empty and the mode picker is shown
              without any unexpected behavior.
    """

    # Clear simulation session data (without touching login state)
    _clear_simulation_session()

    # Redirect back to the mode picker if logged in, else the landing page
    if current_user.is_authenticated:
        return redirect(url_for("modes"))
    return redirect(url_for("index"))


# Run the Flask development server when executed directly
if __name__ == "__main__":
    app.run(debug=True)
