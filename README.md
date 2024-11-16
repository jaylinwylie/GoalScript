# Introduction to GolScript

**GolScript** is a goal-tracking language designed to help individuals effectively manage tasks and goals in a structured, assembly-code-like format. It's particularly suited for users who appreciate detailed breakdowns of tasks, dependencies, and conditions, enabling a clear pathway to goal completion.

## GolScript Structure

GolScript scripts are divided into goals (`GOL`), tasks (`TSK`), and conditions (`ALL`, `ANY`). Here’s a breakdown of each component:

- **Goals (`GOL`)**: Define an overarching objective.
- **Tasks (`TSK`)**: Specific actions required to achieve a goal.
- **Conditions**:
  - **`ALL`**: All listed sub-goals or tasks must be completed.
  - **`ANY`**: Any one of the listed sub-goals or tasks must be completed.
  - **Markers**:
    - `?` - Marks a goal or task as optional.
    - `!` - Marks a reference to another goal.
    - `.` - Marks a non-referencing sub-goal or task.
