# Final Project Report

* Student Name: Anam Shamsi
* Github Username: anamahmedshamsi12
* Semester: Fall 2025
* Course: CS5001



## Description 
General overview of the project, what you did, why you did it, etc. 
>## Overview
> The Life Metrics Simulator is an interactive Python-based application designed to show how everyday decisions, which are often viewed as small or insignificant, can accumulate and have a measurable impact over time through a system of quantitative life metrics. The program allows users to either choose from predefined profiles or create a custom simulation in which they define their own metrics and types of decisions, making the experience flexible and personally relevant. Each simulated day is divided into several check-ins, during which users select a decision and may optionally write a brief reflection, and these choices result in gradual changes to the underlying metrics that are stored and carried forward across multiple interactions. As the simulation continues, the program keeps a detailed record of user decisions and calculates longer-term trends that help reveal patterns in behavior that may not be obvious from individual choices alone. By converting abstract concepts such as focus, energy, or well-being into structured numerical values, the simulator provides a clear way to think about decision-making as a cumulative process rather than a collection of isolated events.

>## Why I Did It
> The earliest version of this project was originally implemented as a Pygame-based simulation, inspired by the role-playing game Persona 5, in which characters are required to make a series of daily decisions that incrementally influence quantified attributes such as relationships, responsibilities, and personal growth. That framework initially appealed to me because it presents life as a system governed by repeated choices, where seemingly minor actions accumulate and shape longer-term outcomes, an idea that closely aligns with both behavioral psychology and cognitive science. I was particularly interested in exploring how this decision-driven structure could be translated into a real-world context, effectively reframing everyday behavior as a computational process in which actions serve as inputs and internal states evolve over time. Pygame provided a suitable environment for this early exploration, as it allowed for rapid prototyping of interaction, immediate feedback, and visible metric changes within a contained graphical loop. However, as the project matured, I began to recognize that the game-oriented structure, while engaging, imposed conceptual and architectural constraints that conflicted with the project’s broader goal of serving as a reflective and practical tool. The continuous render loop and emphasis on immediacy reinforced an entertainment-focused experience, whereas the system I was developing was increasingly concerned with deliberation, persistence, and cumulative patterns of behavior. In response, I made a deliberate transition away from the interactive RPG format and toward an application-style design, motivated by the desire to create a system that could realistically be used to support reflection on real-life decision-making rather than simulate it as gameplay. This shift also allowed the project to more directly reflect my academic background, as it emphasized modeling cognitive processes, behavioral trends, and emotional regulation through structured state transitions rather than through game mechanics.

## Key Features
Highlight some key features of this project that you want to show off/talk about/focus on. 
>## Key Features

>**Decision-Driven Simulation Model**  
The project models everyday behavior as a sequence of intentional decisions rather than isolated actions. Each user choice serves as an input that incrementally adjusts underlying life metrics, allowing the simulator to emphasize cumulative effects over time rather than short-term outcomes.

>**Multiple Simulation Modes**  
The application supports Student Mode, Professional Mode, and Custom Mode, each tailored to different life contexts. Predefined modes provide structured scenarios, while Custom Mode allows users to define their own metrics and decision categories, making the system adaptable to individual priorities.

>**Dynamic Metric Visualization**  
Life metrics are visualized using horizontal progress bars with percentage values and threshold-based color changes. Metrics update in real time after each check-in, providing immediate visual feedback while also supporting long-term trend observation.

>**Custom Mode Presets for High-Level Decisions**  
Custom Mode introduces high-level decision presets that summarize how a portion of the day felt overall, allowing users to update multiple metrics simultaneously without entering granular actions. This design balances ease of use with meaningful state changes.

>**Cumulative Trend Tracking**  
The simulator maintains a structured log of decisions and computes longer-term trends, enabling users to identify behavioral patterns across multiple days. This feature reinforces the idea that consistency and repetition shape outcomes more than single decisions.

>**Session-Based State Management**  
The application uses session-based state management to persist simulation data across interactions. This allows users to progress naturally through check-ins and days without manual data handling, while keeping the simulation logic cleanly separated from the interface.

>**Web-Based, App-Like Interface**  
Built with Flask and HTML/CSS, the project presents an app-style graphical interface rather than a command-line or game-based experience. This design choice makes the simulator accessible, intuitive, and aligned with real-world reflective use.
## Guide
How do we run your project? What should we do to see it in action? - Note this isn't installing, this is actual use of the project.. If it is a website, you can point towards the gui, use screenshots, etc talking about features. 

>##    Life Metrics Simulator Guide
The application runs locally using Flask. Once the server is running, the simulator is accessed through a web browser at http://127.0.0.1:5000. To start the simulator, the user must navigate into the project directory and run:`python3 src/app.py`. The URL is only active while the Flask server is running, as shown below:
```python
anamwork@MacBook-Pro finalproject-anamahmedshamsi12 % python3 src/app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 172-829-255
```
>## Graphical User Interface (GUI)

All interaction happens through a browser-based graphical user interface built with HTML/CSS and Flask templates.

**The application has three main screens:**

---

### 1. Main Menu – Mode Selection

When the user visits `http://127.0.0.1:5000`, they see the **landing page:**

> ![Main Menu Variant](report%20images/screenshots/life_metrics_menu_page.png)
>This screen is the first page the user sees when they open the Life Metrics Simulator. It includes the custom Life Metrics logo and a section that introduces the purpose of the tool: helping users understand how their daily decisions shape long-term balance. 

>From here, users scroll or navigate to select one of the simulation modes and begin interacting with the tool:
>![Main Menu](report%20images/screenshots/life_metrics_menu_page_2.png)
>Each button is styled as a rounded “card” and routes the user to the appropriate setup or simulation screen. This screen makes it immediately clear how to start the simulator without requiring any command-line interaction.


### 2. Custom Setup Screen
If the user chooses **Custom Mode**, they are taken to a guided setup form where they can:

- Define up to **five life metrics** (e.g., Focus, Energy, Mood, Social Battery).
- Configure **three decisions** (Decision 1, Decision 2, Decision 3) with:
  - A label (e.g., “Deep Focus Day”, “Balanced Day”, “Procrastinated / Social Day”)
  - A description explaining what that decision represents.


  
>![Custom Mode Intro](report%20images/screenshots/custom_metrics_.png)
>This panel gives the user a short overview of how the decision-based system works: defining metrics, choosing from three decision types, and logging optional reflections. It helps users understand how their custom inputs translate into simulation behavior.

>![Step 1 – Name your metrics](report%20images/screenshots/custom_mode_step_1.png)
>In Step 1, the user selects up to five metrics that matter to them such as Focus, Social Energy, Mental Health, or Progress. These custom labels become the axes the simulator tracks and visualizes throughout the run.

>![Step 2 – Define your decisions](report%20images/screenshots/custom_mode_step_2.png)
>In Step 2, the user describes three types of “typical days” or decisions they commonly make. Each decision includes a custom label and descriptive example. These three decisions form the core actions the user will choose between during each check-in.

>![Sample Custom Mode Check-in Interface](report%20images/screenshots/custom_mode_output.png)
>Sample Custom Mode check-in interface during a morning check-in. The left panel displays a snapshot of sample user-defined life metrics represented as horizontal progress bars with percentage values and threshold-based color changes. The right panel presents high-level decision presets that summarize how the day felt overall, along with an optional reflection input and a brief history of recent check-ins. Selecting a decision applies a proportional adjustment across all custom metrics, demonstrating cumulative pattern tracking rather than isolated actions.
## 2. Student Mode
Student Mode models the kinds of daily decisions that shape an academic lifestyle. This mode is designed to help users visualize how typical student scenarios such as studying late, socializing, prioritizing mental health, or managing responsibilities that affect long-term balance across several life categories.


>![Student Life Metrics Dashboard](report%20images/screenshots/student_life_metrics.png)
>Student Mode simulation dashboard during a morning check-in. Each life metric is displayed as a horizontal progress bar with a percentage value, and bar colors dynamically change based on defined thresholds, with green indicating healthier ranges, yellow indicating moderate or mixed ranges, and red indicating low values. The overall score summarizes cumulative decision impact, and all metrics update in real time after each check-in.

>Student Mode Decisions Dashboard
>![Student Life Decisions](report%20images/screenshots/life_metrics_student_decisions.png)
Decision selection interface in Student Mode, showing three decision cards presented at each check-in. Each card represents a distinct type of daily decision and includes a brief description to guide user choice. Selecting a decision triggers metric updates, advances the simulation to the next check-in, and records the action in the decision log, emphasizing how individual choices contribute to cumulative outcomes over time.*

## 3. Professional Mode
Professional Mode models decision-making within a professional context by representing how recurring workplace choices influence productivity, cognitive load, and work-life balance over time. The mode is structured around realistic professional scenarios that involve trade-offs between efficiency, rest, and personal well-being, encouraging users to reflect on how habitual responses to these situations shape longer-term outcomes rather than short-term performance.
>![Professional Dashboard](report%20images/screenshots/professional_mode.png)
>Professional Mode dashboard showing dynamically updated, color-coded life metrics that reflect the cumulative effects of professional decision-making.*



>![Professional Life Decisions](report%20images/screenshots/professional_mode_decisions.png)
>Decision selection interface in Professional Mode, presenting realistic workplace-related choices at each check-in. Each decision represents a trade-off commonly encountered in professional settings, and selecting an option advances the simulation, updates life metrics, and records the action in the decision log to reflect cumulative behavioral patterns.

## Installation Instructions
If we wanted to run this project locally, what would we need to do?  If we need to get API key's include that information, and also command line startup commands to execute the project. If you have a lot of dependencies, you can also include a requirements.txt file, but make sure to include that we need to run `pip install -r requirements.txt` or something similar.

>## Running the Project Locally

This project runs as a local Flask web application and does not require any API keys.

1. Make sure Python is installed on your machine.
2. Download or clone the project repository so the project files are available locally.
3. Open a terminal and navigate to the project’s root directory.
4. Install the required dependency by running `pip install flask`.
5. Start the application by running `python3 app.py`.
6. Open a web browser and navigate to `http://127.0.0.1:5000`.

The application will remain accessible in the browser as long as the Flask server is running.
This project only requires Flask. If a requirements.txt file is provided, dependencies can be installed using pip install -r requirements.txt.

## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did. 
>## Life Metrics Code Review 
This project is structured around a clear separation of concerns, with simulation logic isolated from the web interface and reusable components grouped into focused modules. This design improves readability, testability, and extensibility.
## Code Overview and Key Components

This section highlights key parts of the project’s codebase and explains how they work together to support the overall simulation. Rather than describing every function, this overview focuses on the core logic that drives state management, decision handling, and metric updates.

## Code Walkthrough (All Functions)

This section documents the purpose and behavior of every function (and class method) in the project’s Python modules. Each file is linked for direct review.

---

## 1. `app.py` (Flask routes / controller)
Link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/src/app.py

`app.py` is the controller layer. It handles routing, reads form inputs, writes/reads session state, and delegates simulation logic to the simulation module.

#### `index()`
```python
@app.route("/")
def index():
```
>Renders the landing page (index.html) where the user chooses a mode (Student, Professional, Custom). This route does not rely on session state, so it is safe to revisit at any time.

#### `start()`
```python
@app.route("/start", methods=["GET", "POST"])
def start():
```
Starts a built-in profile (Student or Professional). It reads the selected profile from query parameters or form data, validates it, clears any existing session state, initializes metrics/actions/day/time-slot, then redirects to /simulate. Key idea: this route sets the baseline session variables that the rest of the app depends on.

#### `custom_setup()`
```python 
@app.route("/custom_setup", methods=["GET", "POST"])
def custom_setup():
```
>Handles the Custom Mode setup form. On GET, it renders custom_setup.html. On POST, it.
Reads raw metric names and custom decision labels/descriptions from the form, applies default labels/descriptions if fields are blank, builds a custom profile using build_custom_profile(...), stores the resulting mode/metrics/actions in the session, and redirects to /simulate.
This route is the bridge between user-defined configuration and the simulation state.

#### `simulate()`
```python
@app.route("/simulate", methods=["GET", "POST"])
def simulate():
```
>This is the main simulation loop (controller). It supports:

**GET:** render the dashboard + decision options using the current session state

**POST:** apply a decision, update metrics and log entries, advance time/day, then redirect back to GET

>If session["mode"] is missing, it redirects to / to prevent invalidsimulation access. 
It computes an overall score (via compute_score) and optionally computes metric trends (via recursive_metric_trend) when enough log entries exist. 
It uses TIME_SLOTS and moment_index to model “Morning / Afternoon / Evening” check-ins.


#### `reset()`
```python
@app.route("/reset")
def reset():
```
>Clears all session data and returns the user to the main menu. This ensures a clean restart without leftover state

## `2. simulation.py` 
Link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/src/simulation.py

The `simulation.py` file contains the core logic of the Life Metrics Simulator. It is responsible for modeling how decisions affect life metrics, how simulated time progresses, how user actions are logged, and how higher-level summaries such as overall scores and trends are computed. 


**CS5001 concepts:** The concepts here that are demonstrated include functions, lists, dictionaries, loops, conditionals, recursion, state management, and modular design.

### Discrete Time Modeling (Lists and Indexing)

Time in the simulation is modeled as a fixed sequence of daily check-ins rather than continuous time. This is implemented using a list and an index variable, allowing the simulation to advance in predictable, discrete steps.

```python
TIME_SLOTS = ["Morning", "Afternoon", "Evening"]
```
>**This demonstrates the use of lists, indexing, and integer state variables to represent structured progression through time.**

### Profile Initialization (Dictionaries and Defensive Copying)

>The start_profile function initializes a built-in simulation mode by retrieving predefined configuration data. Fresh copies of metrics and actions are returned to avoid unintended mutation of global defaults.
```python
def start_profile(profile_key):
    mode = PROFILES[profile_key]["mode"]
    metrics = PROFILES[profile_key]["metrics"].copy()
    actions = list(PROFILES[profile_key]["actions"])
    return mode, metrics, actions
```
>**This function demonstrates dictionary lookup, defensive programming through copying, and clean function interfaces.**

### Custom Mode 

Custom Mode allows users to define their own metrics and decision labels. The build_custom_profile function sanitizes user input, applies defaults when necessary, and constructs the data structures required for the simulation to run.
```python
def build_custom_profile(raw_metrics, strong_label, strong_desc, steady_label, steady_desc, tough_label, tough_desc):
    clean_metric_names = [m.strip() for m in raw_metrics if m and m.strip()]
    if not clean_metric_names:
        clean_metric_names = ["Primary Goal"]

    metrics = {name: 60 for name in clean_metric_names}

    actions = [
        {"id": "strong_day", "label": strong_label, "description": strong_desc},
        {"id": "steady_day", "label": steady_label, "description": steady_desc},
        {"id": "tough_day", "label": tough_label, "description": tough_desc},
    ]

    return "custom", clean_metric_names, metrics, actions
```
>**This demonstrates list comprehensions, conditionals, dictionary comprehensions, and robust handling of user input.**

### Decision Processing and State Transitions (Loops and Conditionals)

The `log_check_in` function is the central state-transition mechanism of the simulation. It applies decision effects, records user actions, and advances the simulation through time and days.
```python
def log_check_in(mode, metrics, actions, day, moment_index, action_id, note, log_entries, scale_factor=0.5):
    chosen = next((a for a in actions if a["id"] == action_id), None)
    if not chosen:
        return metrics, log_entries, day, moment_index

    if mode == "custom":
        for metric in metrics:
            change = 5 if action_id == "strong_day" else -5 if action_id == "tough_day" else 1
            metrics[metric] = max(0, min(100, metrics[metric] + change))
    else:
        for metric, delta in chosen["deltas"].items():
            if metric in metrics:
                updated = metrics[metric] + int(delta * scale_factor)
                metrics[metric] = max(0, min(100, updated))

    log_entries.append({
        "day": day,
        "time": TIME_SLOTS[moment_index],
        "action_id": action_id,
        "note": note,
        "delta": chosen.get("deltas", {}),
    })

    moment_index += 1
    if moment_index >= len(TIME_SLOTS):
        day += 1
        moment_index = 0

    return metrics, log_entries, day, moment_index
```
>**This function demonstrates loops, conditionals, dictionary iteration, structured logging using lists of dictionaries, and maintaining invariants by clamping metric values to valid ranges.**

### Aggregation and Abstraction (Functions)
The `compute_score` function summarizes multiple metric values into a single score. This abstraction allows the interface to display an overall balance indicator without exposing internal details.
```python
def compute_score(metrics):
    if not metrics:
        return 0.0
    return round(sum(metrics.values()) / len(metrics), 1)
```
>**This demonstrates aggregation, defensive conditionals, and numeric computation.**


### Recursion for Trend Analysis

To demonstrate recursion, the project includes a function that computes cumulative metric trends by recursively traversing historical log entries.
```python
def recursive_metric_trend(log_entries, metric, index=0):
    if index >= len(log_entries):
        return 0
    change = log_entries[index].get("delta", {}).get(metric, 0)
    return change + recursive_metric_trend(log_entries, metric, index + 1)
```
>**This function demonstrates recursion with a clear base case and recursive case, as well as sequential processing of time-based data.**

## 3. `metrics.py`
Link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/src/metrics.py

The metrics.py file contains helper functions that operate directly on the simulation’s metric data. Its purpose is to centralize logic related to initializing metrics, applying changes, and computing summaries, allowing the simulation and routing layers to remain focused on control flow rather than low-level data manipulation.

**CS5001 concepts:** The concepts demonstrated in this file include functions, dictionaries, loops, conditionals, aggregation, defensive programming, and invariants.


### Metric Initialization (Dictionaries and Defaults)

Metric initialization is handled through dictionary construction to ensure that each simulation run begins with a clean and predictable state. This function also applies default behavior when user-defined metrics are missing or invalid.
```python 
def init_metrics(mode, custom_metric_names=None):
    if mode in DEFAULT_METRICS:
        return DEFAULT_METRICS[mode].copy()

    clean_names = []
    if custom_metric_names:
        for name in custom_metric_names:
            stripped = name.strip()
            if stripped:
                clean_names.append(stripped)

    if not clean_names:
        clean_names = ["Primary Goal"]

    return {metric: 60 for metric in clean_names}
```
>**This demonstrates dictionary construction, loops for input sanitization, conditionals for default handling, and defensive programming to guarantee valid initial state.**

### Applying Metric Changes (Loops and Invariants)

The `apply_deltas` function updates metric values based on scenario effects while enforcing value boundaries. Metric values are clamped between 0 and 100 to maintain consistency across the simulation.
```python
def apply_deltas(metrics, deltas):
    updated_metrics = metrics.copy()

    for metric, delta in deltas.items():
        if metric in updated_metrics:
            new_value = updated_metrics[metric] + delta
            updated_metrics[metric] = max(0, min(100, new_value))

    return updated_metrics
```
>**This demonstrates loops, dictionary iteration, conditional membership checks, and maintaining invariants through value clamping.**

Overall Score Calculation (Aggregation and Functions)

The `average_score` function summarizes the current state of multiple metrics into a single numeric value, which is used by the interface to present an overall balance indicator.
```python
def average_score(metrics):
    if not metrics:
        return 0.0
    return round(sum(metrics.values()) / len(metrics), 1)
```
>**This demonstrates aggregation, defensive conditionals to prevent division errors, and numeric computation using dictionary values.**

## 4. `sessions.py`
Link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/src/sessions.py

The sessions.py file defines a session abstraction that represents a single run of the Life Metrics Simulator. It encapsulates mutable simulation state such as the current day, metric values, and log history. By grouping related state and behavior into a session object, the project demonstrates clear organization and controlled state management.

**CS5001 concepts:** The concepts demonstrated in this file include classes and objects, instance variables, functions, loops, conditionals, lists, dictionaries, and state progression.

### Session Initialization (Classes and Instance Variables)

The session object is initialized with a profile and sets up the baseline simulation state. Metrics are copied to prevent shared mutation between sessions.
```python
class Session:
    def __init__(self, profile):
        self.profile = profile
        self.day = 1
        self.metrics = profile.initial_metrics.copy()
        self.logs = []
```
>**This demonstrates object-oriented programming, instance variables, defensive copying, and structured initialization of program state.**

### Applying Activities (Loops and Conditionals)

Activities selected by the user apply deterministic changes to the current metric values. Each update enforces bounds to preserve valid ranges.
```python
def apply_activity(self, activity_name, effects):
    for metric, delta in effects.items():
        if metric in self.metrics:
            new_value = self.metrics[metric] + delta
            self.metrics[metric] = max(0, min(100, new_value))
```
>**This demonstrates loops, dictionary iteration, conditionals, and invariant enforcement through value clamping.**

### Random Variability (Conditionals and Controlled Randomness)

To simulate real-world variability, the session may apply small random changes with a fixed probability. This introduces non-determinism while remaining controlled.
```python
def maybe_apply_random_event(self):
    if random.random() > 0.2:
        return

    for metric in self.metrics:
        change = random.choice([-2, -1, 1])
        self.metrics[metric] = max(0, min(100, self.metrics[metric] + change))
```
>**This demonstrates conditionals, loops, and probabilistic branching using random values.**
### Advancing the Simulation (State Progression)

The session tracks progression across days. Advancing the simulation simply increments the day counter.
```python
def end_day(self):
    self.day += 1
```
>**This demonstrates integer state variables and explicit time progression.**

### Recording Logs (Lists of Dictionaries)

User activity and reflections are stored as structured log entries. Each log entry records the day and associated metadata.
```python
def add_log_entry(self, note, mood):
    self.logs.append({
        "day": self.day,
        "note": note,
        "mood": mood
    })
```
>**This demonstrates lists of dictionaries, appending structured data, and maintaining a history of user actions.**

## 5. `profiles.py`
Link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/src/profiles.py

The `profiles.py` ile defines the configuration for each simulation mode, including Student, Professional, and Custom profiles. Rather than hard-coding behavior throughout the program, this file centralizes profile-related data and structure, allowing the simulation logic to remain generic and extensible. Each profile acts as a blueprint that specifies initial metric values and descriptive metadata.

**CS5001 concepts:** The concepts demonstrated in this file include classes, constructors, dictionaries, functions, conditionals, data abstraction, and modular design.

### Profile Abstraction (Classes and Encapsulation)

The Profile class encapsulates all information required to initialize a simulation mode. Grouping related data into a single object improves clarity and allows profiles to be passed cleanly between components.
The `profile.py` class encapsulates all information required to initialize a simulation mode. Grouping related data into a single object improves clarity and allows profiles to be passed cleanly between components.
```python
class Profile:
    def __init__(self, name, initial_metrics, mode="student", activity_labels=None):
        self.name = name
        self.initial_metrics = initial_metrics
        self.mode = mode
        self.activity_labels = activity_labels
```
>**This demonstrates object-oriented programming, encapsulation of related data, and the use of constructors to initialize instance variables.**

### Predefined Profiles (Dictionaries as Configuration)
Student and Professional modes are defined using dictionaries that store baseline metric values. These dictionaries function as static configuration objects that can be reused across simulation runs.
```python
STUDENT_PROFILE = Profile(
    name="Student Life",
    initial_metrics={
        "Academics": 70,
        "Mental Health": 65,
        "Social Life": 60,
    },
    mode="student"
)
```
>**This demonstrates dictionary literals as configuration data and separation of static data from program logic.**

### Profile Selection Logic (Conditionals)
The `get_profile_from_form_value` function maps user input from the interface to an internal profile object. This provides a clear translation layer between external form values and internal program structures.
```python
def get_profile_from_form_value(value):
    if value == "student":
        return STUDENT_PROFILE
    return PROFESSIONAL_PROFILE
```
>**This demonstrates conditional branching and controlled mapping from user input to program state.*8

### Custom Profile Construction 

Custom Mode profiles are built dynamically based on user input. Metric names are cleaned, validated, and normalized before being used to construct a new profile instance.
```python
def build_custom_profile(metric_names, activity_labels):
    clean_names = [m.strip() for m in metric_names if m and m.strip()]
    if not clean_names:
        clean_names = ["Primary Goal"]

    normalized_metrics = {}
    for name in clean_names:
        normalized_metrics[name] = 50

    return Profile(
        name="Custom Life",
        initial_metrics=normalized_metrics,
        mode="custom",
        activity_labels=activity_labels
    )
```
>**This demonstrates list comprehensions, loops, conditionals, dictionary construction, and robust handling of user-defined input.**

## 6. `scenarios.py`
Link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/src/scenarios.py

The `scenarios.py` file defines the library of decisions available in each simulation mode. Rather than encoding decision logic directly into functions, this file uses a data-driven approach in which each scenario is represented as structured data. This allows the simulation engine to remain generic while supporting different modes and behaviors through configuration alone.

**CS5001 concepts:** The concepts demonstrated in this file include dictionaries, lists, nested data structures, modular design, and separation of data from logic.

Scenario Definitions (Nested Dictionaries and Lists)

All scenarios are stored in a single dictionary keyed by mode. Each mode maps to a list of scenario dictionaries, where each scenario contains an identifier, a label, a description, and metric deltas.
```python
ACTIONS = {
    "student": [
        {
            "id": "study_session",
            "label": "Focused study session",
            "description": "Spend uninterrupted time studying or completing assignments.",
            "deltas": {
                "Academics": 8,
                "Mental Health": -2,
                "Social Life": -1
            }
        },
        {
            "id": "social_event",
            "label": "Socialize with friends",
            "description": "Attend a social gathering or spend time with friends.",
            "deltas": {
                "Academics": -2,
                "Mental Health": 5,
                "Social Life": 6
            }
        }
    ],
    "professional": [
        {
            "id": "productive_workday",
            "label": "Highly productive workday",
            "description": "Make significant progress on professional responsibilities.",
            "deltas": {
                "Career": 7,
                "Energy": -3,
                "Work-Life Balance": -2
            }
        }
    ]
}
```
>**This demonstrates nested dictionaries and lists, where structured data is used to describe behavior rather than embedding logic directly in code.**

### Data-Driven Design (Separation of Logic and Configuration)

By defining scenarios entirely as data, the simulation engine can iterate over scenarios and apply their effects without needing to know the specifics of each mode. This makes it easier to add or modify scenarios without changing simulation logic.
```python
for scenario in ACTIONS[mode]:
    if scenario["id"] == action_id:
        deltas = scenario["deltas"]
```
>**This demonstrates looping over lists, dictionary access, and separation of concerns between data and control flow.**

### Stable Identifiers (String Matching and Consistency)

Each scenario includes a stable string identifier (id) that is used internally to match user selections with scenario effects. This ensures that display labels can change without breaking internal logic.

if scenario["id"] == selected_id:
    apply_deltas(metrics, scenario["deltas"])
```python
if scenario["id"] == selected_id:
    apply_deltas(metrics, scenario["deltas"])
```
>**This demonstrates string comparison, conditional logic, and the use of identifiers to maintain consistency across program components.**

## 7. `tests_life_metrics.py`
Link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/src/test_life_metrics.py

The `tests_life_metrics.py` file contains automated unit tests used to verify the correctness of the simulation logic. Rather than relying only on manual testing through the web interface, these tests validate that key functions behave as expected, including edge cases such as out-of-range values, empty inputs, and invalid scenario selections. This makes it easy to demonstrate that the project was tested systematically prior to submission.

**CS5001 concepts:** The concepts demonstrated in this file include unit testing, functions, conditionals, dictionaries, lists, edge case analysis, and verification of invariants.

### Test Helper Function (Code Reuse and Set Logic)

A helper function is used to reduce repetition when checking dictionary keys. This ensures metric dictionaries contain exactly the expected fields.

```python
def __check_dict_keys(self, actual, expected_keys):
    self.assertEqual(set(actual.keys()), set(expected_keys))
```
>**This demonstrates helper methods for reuse, dictionary key access, and set-based comparison to avoid ordering issues.**

### Boundary Testing for Clamping (Edge Cases and Invariants)

These tests verify that metric values are always constrained to valid bounds. This is important because the simulation should never allow metrics to drop below 0 or exceed 100.
```python
def test_clamp_basic(self):
    self.assertEqual(clamp(-10), 0)
    self.assertEqual(clamp(50), 50)
    self.assertEqual(clamp(150), 100)
```
>**This demonstrates edge case testing and invariant verification using boundary values.**

### Testing Metric Updates (Dictionaries and Correctness)

This test ensures that applying deltas correctly updates metrics and still enforces clamping behavior.

```python
def test_clamp_basic(self):
    self.assertEqual(clamp(-10), 0)
    self.assertEqual(clamp(50), 50)
    self.assertEqual(clamp(150), 100)
```
>**This demonstrates edge case testing and invariant verification using boundary values.**

### Testing Metric Updates (Dictionaries and Correctness)

This test ensures that applying deltas correctly updates metrics and still enforces clamping behavior.
```python
def test_apply_deltas_and_clamp(self):
    metrics = {"Energy": 98}
    deltas = {"Energy": 10}
    updated = apply_deltas(metrics, deltas)
    self.assertEqual(updated["Energy"], 100)
```
>**This demonstrates dictionary-based input/output testing and validation of update rules.**

### Testing Score Computation (Aggregation and Empty Cases)

This test verifies that the score function computes correct averages and safely handles empty inputs.
```python
def test_average_score_normal_and_empty(self):
    self.assertEqual(average_score({"A": 50, "B": 70}), 60.0)
    self.assertEqual(average_score({}), 0.0)
```
>**This demonstrates testing aggregation logic and confirming safe behavior for edge cases.**

### Testing State Transitions (Time Progression Logic)

This test validates that a user check-in advances the time slot index correctly and appends a log entry.
```python
def test_log_check_in_advances_time(self):
    mode = "student"
    metrics = {"Academics": 70}
    actions = [{"id": "test_action", "label": "Test", "deltas": {"Academics": 10}}]
    logs = []

    metrics, logs, new_day, new_index = log_check_in(
        mode, metrics, actions, 1, 0, "test_action", "", logs, 1.0
    )

    self.assertEqual(len(logs), 1)
    self.assertEqual(new_index, 1)
    self.assertEqual(metrics["Academics"], 80)
```
>**This demonstrates testing state progression, list updates (logging), and correctness of metric mutation after one decision.**

### Testing Recursion (Correctness of Recursive Trend)

This test verifies that the recursive trend function correctly aggregates metric deltas across history.
```python
def test_recursive_metric_trend_basic(self):
    logs = [
        {"delta": {"Energy": 2}},
        {"delta": {"Energy": -1}},
        {"delta": {"Energy": 3}},
    ]
    self.assertEqual(recursive_metric_trend(logs, "Energy"), 4)
```
>**This demonstrates recursion testing, verification of base/recursive case behavior, and cumulative computation across a list.**


## Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.
#### Challenges
>One of the most significant challenges throughout this project was conceptual rather than purely technical, as the central goal was not simply to build a functioning program, but to design a system that meaningfully modeled the cumulative impact of everyday decisions over time. Early iterations of the simulator handled individual actions well, but translating these isolated updates into a coherent long-term structure required careful consideration of how state should persist, evolve, and remain interpretable across multiple days and check-ins. Ensuring that metric values, logs, and time progression remained synchronized without producing contradictory or unintuitive outcomes forced me to think more deeply about how abstract concepts such as balance, progress, and decline could be represented computationally.

>Another major challenge emerged from the project’s architectural evolution. The earliest version of the simulator was implemented using Pygame, inspired by role-playing games that frame personal growth through metrics and decision-making. While this approach was effective for rapid experimentation, it became increasingly clear that the continuous render loop and game-oriented structure conflicted with the reflective and episodic nature of the system I was trying to build. Transitioning from a Pygame-based prototype to a Flask-based web application required a substantial refactor of both logic and design, but more importantly, it required reevaluating how users should interact with the system. This shift marked a conceptual turning point, reframing the simulator from an interactive game into a practical tool intended to encourage intentional reflection rather than immediate feedback.

> Handling user-defined input in Custom Mode also presented persistent challenges. Allowing users to define their own metrics and decision labels introduced a wide range of potential edge cases, including empty submissions, inconsistent naming, and ambiguous configurations. Addressing these issues required implementing defensive programming strategies that ensured the simulation could always initialize into a valid and stable state, even when user input was incomplete or imperfect. Designing these safeguards reinforced the importance of anticipating failure cases and treating input validation as a core component of program correctness rather than an afterthought.

#### Rewarding
> Incorporating recursion for trend analysis proved to be both intellectually demanding and rewarding. While recursion is often introduced in abstract or contrived examples, applying it within the context of accumulated decision data required careful structuring of base cases and recursive calls to ensure clarity and correctness. Integrating this recursive logic into the simulation allowed the system to surface longer-term behavioral patterns rather than only immediate outcomes, which aligned closely with the project’s overarching goals. Although these challenges introduced moments of friction throughout development, they ultimately represent the areas in which the most learning occurred. Each obstacle required revisiting assumptions, refining abstractions, and applying course concepts in a context that felt authentic rather than artificial. The final structure of the project reflects this iterative process and serves as a record of both technical growth and conceptual refinement.



## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

> A recorded demo video demonstrating a complete example run of the project
is included in the repository at the following link: https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/testrun.mp4


## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

_Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_

### Life Metrics Testing
The project was tested using a combination of automated unit tests and manual
edge-case testing. Unit tests were written to validate core simulation logic,
including metric updates, score computation, clamping behavior, custom mode
initialization, and recursive trend analysis. These tests are located in
[`src/test_life_metrics.py`](src/test_life_metrics.py) and were executed using Python’s `unittest`
framework.

The output from running the test suite is documented in
[`tests_output.txt`](tests_output.txt). Additional manual and terminal-based
edge-case tests were performed to validate defensive behavior and state
transitions, with commands and observed outputs recorded in
[`tests_output.txt`](tests_output.txt).



## 4. Testing Artifacts
## 4. Testing Artifacts

The following artifacts are included in the repository to document how the project was tested and to provide verifiable evidence that the code was executed and validated prior to submission:

- **Unit Tests**  
  The automated unit tests are implemented using Python’s `unittest` framework and are located in  
  [`src/tests.py`](src/tests.py).  
  These tests cover core simulation logic, including metric updates, clamping behavior, score computation, custom mode initialization, and recursive trend analysis.

- **Automated Test Output**  
  The console output from running the full unit test suite is recorded in  
  [`tests_output.txt`](tests_output.txt).  
  This file shows that all tests were discovered and executed successfully.

- **Manual and Terminal Edge-Case Testing**  
  Additional edge cases and defensive behaviors were tested directly from the terminal and through manual interaction with the application. The commands used and their observed outputs are documented in  
  [`manual_test_notes.txt`](manual_test_notes.txt).



- The recorded demo can be viewed at the following link:
  https://github.com/Fa25-CS5001-Online-Lionelle/finalproject-anamahmedshamsi12/blob/main/testrun.mp4

---


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

> One area that could be further developed is the complexity of how decisions influence metrics. In its current form, the simulator applies mostly linear, predefined changes, which was sufficient for illustrating core programming concepts but limits how realistically long-term behavior is modeled. With additional time, I would expand this logic to allow for more nuanced relationships between metrics, such as compounding effects or interactions where progress in one area gradually impacts others. The simulation is also limited to a single session, and introducing persistent storage would allow users to track patterns over longer periods rather than viewing each run in isolation.

>The interface itself could also be extended to better support reflection and analysis. While the current dashboard provides clear feedback through dynamic metric bars and summary values, additional visualizations such as historical graphs or trend timelines could make long-term patterns more visible and interpretable. Looking further ahead, the system could incorporate adaptive behavior, allowing decision impacts to shift based on prior user history. These additions would build naturally on the existing structure and move the project closer to functioning as a sustained decision-reflection tool rather than a standalone simulation.

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.

> This course reshaped how I understand programming, not as a collection of isolated techniques, but as a way of thinking about systems, structure, and long-term behavior. Before CS5001, my exposure to programming felt more mechanical and goal driven, focused primarily on getting something to work rather than understanding why it worked the way it did. Over the semester, concepts such as functions, recursion, data structures, and state management began to feel less abstract and more like tools for expressing ideas clearly and intentionally. What stood out most was how the course created space for creativity alongside technical rigor, particularly through open-ended assignments and the final project, which allowed me to explore personal interests and design choices rather than follow a rigid specification. Building a project that blended decision-making, reflection, and simulation made the learning process feel exploratory rather than prescriptive. Through this process, I also came to appreciate how early design choices influence everything that follows, and how refactoring is often a sign of deeper understanding rather than error. Moving forward, I know that continuing to grow will require deeper engagement with larger systems, stronger testing practices, and continued practice translating conceptual ideas into coherent code. More than learning Python itself, this course encouraged a way of reasoning that values structure, clarity, and creative problem solving, which is something I expect to carry forward beyond this class.