from copy import copy
from enum import Enum

from gol import Gol


class Keywords(Enum):
    GOL = 'GOL'
    TSK = 'TSK'
    ALL = 'ALL'
    ANY = 'ANY'
    CHECK = '/'
    SPACE = ' '
    CRITICAL = '!'
    OPTIONAL = '?'
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
            value = line[key_space_position + 1:].strip()

            if code == Keywords.GOL.value:

                pending_goal.is_completed = value.endswith(Keywords.CHECK.value)
                pending_goal.name = value
                self._goals.append(copy(pending_goal))
                pending_goal = Gol()

            elif code == Keywords.TSK.value:
                pending_goal.tasks.append(value)

            elif code == Keywords.ALL.value or code == Keywords.ANY.value:
                pending_goal.is_all = True if code == Keywords.ALL.value else False

                for sub_value in value.split(Keywords.SPACE.value):
                    found_link = False
                    for goal in self._goals:
                        if goal.name == sub_value:
                            pending_goal.reference.append(goal)
                            found_link = True
                            break
                    if not found_link:
                        pending_goal.non_reference.append(sub_value)

            elif code == Keywords.RETURN.value or code == '' or None:
                pass

            else:
                raise SyntaxError(f'Unrecognized key "{code}" on line {line_number}')

        return self._goals
