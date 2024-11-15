from asyncio import current_task
from copy import copy
from enum import Enum

GOLSCRIPT = 'CleanFountain.golscript'


class Keywords(Enum):
    GOL = 'GOL'
    TSK = 'TSK'
    ALL = 'ALL'
    ANY = 'ANY'
    GOL_END = ':'
    TSK_END = ';'
    OPTIONAL = '?'
    REFERENCE = '!'
    NON_REFERENCE = '.'
    SPACE = ' '


class Goal:
    def __init__(self):
        self.name: str | None = None
        self.tasks: list = []
        self.non_reference: list[str] = []
        self.reference: list[Goal] = []
        self.optional: list[Goal] = []
        self.is_completed: bool = False


class GolScriptParser:
    def __init__(self):
        self.goals: list[Goal] = []

    def parse_script(self, golscript: str):
        lines = golscript.splitlines()
        line_numbers = reversed(range(len(lines)))
        lines = reversed(lines)
        pending_goal = Goal()

        for line_number, line in zip(line_numbers, lines):
            line = line.strip()
            key_space_position = line.find(Keywords.SPACE.value)
            code = line[:key_space_position]
            value = line[key_space_position + 1:]

            if code == Keywords.GOL.value:
                goal_end_position = value.find(Keywords.GOL_END.value)
                pending_goal.name = value[:goal_end_position]
                self.goals.append(copy(pending_goal))
                pending_goal = Goal()

            if code == Keywords.TSK.value:
                task_end_position = value.find(Keywords.TSK_END.value)
                if task_end_position == -1:
                    raise SyntaxError(f'Missing ; in TSK on line {line_number + 1}')

                pending_goal.tasks.append(value[:task_end_position])

            elif code == Keywords.ALL.value or code == Keywords.ANY.value:
                values = value.split(Keywords.SPACE.value)
                for value in values:
                    if value.endswith(Keywords.NON_REFERENCE.value):
                        pending_goal.non_reference.append(value[:-1])

                    elif value.endswith(Keywords.REFERENCE.value):
                        value = value[:-1]
                        for goal in self.goals:
                            if goal.name == value:
                                pending_goal.reference.append(goal)

                    elif value.endswith(Keywords.OPTIONAL.value):
                        value = value[:-1]
                        for goal in self.goals:
                            if goal.name == value:
                                pending_goal.optional.append(goal)

                    else:
                        raise f'Missing punctuation in ALL or ANY on line {line_number + 1}'


golscript = GolScriptParser()

with open(GOLSCRIPT) as file:
    golscript.parse_script(file.read())


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


def list_of_goals_to_mermaid(goals):
    generated = set()
    mermaid_diagram = ['graph TD']
    for goal in goals:
        mermaid_diagram.extend(goal_to_mermaid(goal, generated))
    return "\n".join(mermaid_diagram)


with open('diagram.md', 'w') as file:
    file.write(f'```mermaid\n{list_of_goals_to_mermaid(golscript.goals)}\n```')
