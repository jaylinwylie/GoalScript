# Introduction
**GolScript** is a goal-tracking language designed to help individuals effectively manage tasks and goals in a structured, assembly-code-like format. It's particularly suited for users who appreciate detailed breakdowns of tasks, dependencies, and conditions, enabling a clear pathway to goal completion.
## GolScript Structure

- **Goals (`GOL`)**: Define an overarching objective.
  - `:` - Ends the goal line.
  - `/` - Marks a goal as completed (✓).


- **Tasks (`TSK`)**: Specific actions required to achieve a goal.
  - `;` - Ends the task line.

  
- **Conditions**:
  - **`ALL`**: All listed sub-goals must be completed.
  - **`ANY`**: Any one of the listed sub-goals must be completed.
    - `?` - Marks a goal or task as optional.
    - `!` - Marks a reference to another goal.
    - `.` - Marks a non-referencing sub-goal.
