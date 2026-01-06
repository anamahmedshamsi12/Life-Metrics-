
> The Life Metrics Simulator is an interactive Python-based application designed to show how everyday decisions, which are often viewed as small or insignificant, can accumulate and have a measurable impact over time through a system of quantitative life metrics. The program allows users to either choose from predefined profiles or create a custom simulation in which they define their own metrics and types of decisions, making the experience flexible and personally relevant. Each simulated day is divided into several check-ins, during which users select a decision and may optionally write a brief reflection, and these choices result in gradual changes to the underlying metrics that are stored and carried forward across multiple interactions. As the simulation continues, the program keeps a detailed record of user decisions and calculates longer-term trends that help reveal patterns in behavior that may not be obvious from individual choices alone. By converting abstract concepts such as focus, energy, or well-being into structured numerical values, the simulator provides a clear way to think about decision-making as a cumulative process rather than a collection of isolated events.

## Key Features

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

>## Running the Project Locally

This project runs as a local Flask web application and does not require any API keys.

1. Make sure Python is installed on your machine.
2. Download or clone the project repository so the project files are available locally.
3. Open a terminal and navigate to the project’s root directory.
4. Install the required dependency by running `pip install flask`.
5. Start the application by running `python3 app.py`.
6. Open a web browser and navigate to `py`.

The application will remain accessible in the browser as long as the Flask server is running.

