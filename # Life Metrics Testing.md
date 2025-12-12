# Life Metrics Testing
The following manual tests were performed by running the Flask application locally
and interacting with the web interface as an end user. These tests focus on behavior
that cannot be fully validated through unit tests alone, such as session state,
navigation flow, and user input handling.

--------------------------------------------------
Application Navigation and Session State
--------------------------------------------------
- Navigated directly to /simulate without starting a simulation.
  Result: User was redirected back to the main menu without error.

- Refreshed the page during an active simulation.
  Result: Day count, time slot, metrics, and logs persisted correctly.

- Reset the simulation using the reset route.
  Result: Session data cleared and application returned to the landing page.

--------------------------------------------------
Time Progression
--------------------------------------------------
- Completed Morning, Afternoon, and Evening check-ins in sequence.
  Result: Time advanced correctly between slots.

- Completed an Evening check-in.
  Result: Day counter incremented and time slot reset to Morning.

--------------------------------------------------
Metric Updates and Boundaries
--------------------------------------------------
- Selected repeated positive decisions across multiple check-ins.
  Result: Metrics increased but never exceeded the upper bound of 100.

- Selected repeated negative decisions.
  Result: Metrics decreased but never dropped below 0.

- Verified that overall score updated consistently with metric changes.

--------------------------------------------------
Decision Logging
--------------------------------------------------
- Submitted multiple decisions with and without reflection notes.
  Result: Each decision produced exactly one log entry.

- Submitted reflection notes containing special characters.
  Result: Notes rendered correctly and did not cause errors.

--------------------------------------------------
Custom Mode Edge Cases
--------------------------------------------------
- Submitted Custom Mode with all metric fields left blank.
  Result: Default metric initialized and simulation started successfully.

- Submitted Custom Mode with whitespace-only metric names.
  Result: Invalid metric names ignored and defaults applied.

- Submitted a mix of valid and invalid metric names.
  Result: Only valid metric names were used.

--------------------------------------------------
Overall Result
--------------------------------------------------
All manual test cases behaved as expected. The application maintained valid state,
handled edge cases safely, and did not crash or enter invalid states during testing.

### Terminal Edge Case Testing

In addition to unit tests, I ran several boundary and invalid-input checks directly from the terminal to validate defensive behavior in the core simulation logic. These checks confirmed that metric values remain clamped within valid bounds (0–100), score computation handles empty inputs safely, the recursive trend function returns a valid base-case result on empty history, and Custom Mode applies defaults when metric names are left blank. The exact commands and outputs are documented in `tests_output.txt`.
