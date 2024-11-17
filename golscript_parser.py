from copy import copy
from enum import Enum

from gol import Gol


class Keywords(Enum):
    GOL = 'GOL'
    TSK = 'TSK'
    ALL = 'ALL'
    ANY = 'ANY'
    CHECK = '/'
    GOL_END = ':'
    TSK_END = ';'
    OPTIONAL = '?'
    REFERENCE = '!'
    NON_REFERENCE = '.'
    SPACE = ' '
    RETURN = '\n'


class GolScriptParser:
    def __init__(self):
        self._goals: list[Gol] = []

    def parse_script(self, script: str):
        lines = script.splitlines()
        line_numbers = reversed(range(len(lines)))
        lines = reversed(lines)
        pending_goal = Gol()

        for line_number, line in zip(line_numbers, lines):
            line_number += 1
            line = line.strip()
            key_space_position = line.find(Keywords.SPACE.value)
            code = line[:key_space_position]
            value = line[key_space_position + 1:]

            if code == Keywords.GOL.value:
                if Keywords.GOL_END.value not in value:
                    raise SyntaxError(f'Missing : in GOL on line {line_number}')

                pending_goal.is_completed = value.endswith(Keywords.CHECK.value)
                goal_end_position = value.find(Keywords.GOL_END.value)
                pending_goal.name = value[:goal_end_position]
                self._goals.append(copy(pending_goal))
                pending_goal = Gol()

            elif code == Keywords.TSK.value:
                if Keywords.TSK_END.value not in value:
                    raise SyntaxError(f'Missing ; in TSK on line {line_number}')

                task_end_position = value.find(Keywords.TSK_END.value)
                pending_goal.tasks.append(value[:task_end_position])

            elif code == Keywords.ALL.value or code == Keywords.ANY.value:
                pending_goal.is_all = True if code == Keywords.ALL.value else False

                for sub_value in value.split(Keywords.SPACE.value):
                    if sub_value.endswith(Keywords.NON_REFERENCE.value):
                        pending_goal.non_reference.append(sub_value[:-1])

                    elif sub_value.endswith(Keywords.REFERENCE.value):
                        sub_value = sub_value[:-1]
                        for goal in self._goals:
                            if goal.name == sub_value:
                                pending_goal.reference.append(goal)

                    elif sub_value.endswith(Keywords.OPTIONAL.value):
                        sub_value = sub_value[:-1]
                        for goal in self._goals:
                            if goal.name == sub_value:
                                pending_goal.optional.append(goal)

                    else:
                        raise SyntaxError(f'Missing punctuation in {("ANY", "ALL")[int(pending_goal.is_all)]} on line {line_number}')

            elif code == Keywords.RETURN.value or code == '' or None:
                pass

            else:
                raise SyntaxError(f'Unrecognized key "{code}" on line {line_number}')

        return self._goals
