from goal import Goal


def goal_to_mermaid(goal: Goal, generated: set):
    mermaid_str = []
    if goal.name in generated:
        return mermaid_str
    generated.add(goal.name)

    if len(goal.tasks) > 0:
        task_name = goal.name + 'Tasks'
        task_str = "\n".join([task for task in goal.tasks])
        if goal.is_all:
            mermaid_str.append(f'{task_name}[[{task_str}]] ==> {goal.name}')
        else:
            mermaid_str.append(f'{task_name}{{{task_str}}} ==> {goal.name}')

    else:
        task_name = goal.name
        if goal.is_all:
            mermaid_str.append(f'{task_name}[{goal.name}]')
        else:
            mermaid_str.append(f'{task_name}{{{goal.name}}}')

    for non_ref in goal.non_reference:
        mermaid_str.append(f"{non_ref}(({non_ref})) ---> {task_name}")

    for ref in goal.reference:
        mermaid_str.append(f"{ref.name} --> {task_name}")

    for opt in goal.optional:
        mermaid_str.append(f"{opt.name} -.-> {task_name}")

    return mermaid_str


def list_of_goals_to_mermaid(_goals):
    generated = set()
    mermaid_diagram = ['graph TD']
    for goal in _goals:
        mermaid_diagram.extend(goal_to_mermaid(goal, generated))
    return "\n".join(mermaid_diagram)