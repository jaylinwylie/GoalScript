from goal import Goal, GoalArray
from parser import GolScriptParser

GOLSCRIPT = 'CleanFountain.golscript'

with open(GOLSCRIPT) as file:
    golscript = file.read()


def goal_to_mermaid(goal: Goal, generated: set):
    mermaid_str = []
    if goal.name in generated:
        return mermaid_str
    generated.add(goal.name)

    for non_ref in goal.non_reference:
        mermaid_str.append(f"{non_ref} --> {goal.name}")

    for ref in goal.reference:
        mermaid_str.append(f"{ref.name} --> {goal.name}")
        mermaid_str.extend(goal_to_mermaid(ref, generated))

    for opt in goal.optional:
        mermaid_str.append(f"{opt.name} -.- {goal.name}")
        mermaid_str.extend(goal_to_mermaid(opt, generated))

    return mermaid_str


def list_of_goals_to_mermaid(_goals):
    generated = set()
    mermaid_diagram = ['graph TD']
    for goal in _goals:
        mermaid_diagram.extend(goal_to_mermaid(goal, generated))
    return "\n".join(mermaid_diagram)


goals: GoalArray = GolScriptParser().parse_script(golscript)

with open('diagram.md', 'w') as file:
    file.write(f'```mermaid\n{list_of_goals_to_mermaid(goals)}\n```')