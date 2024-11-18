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
        self._gols: list[Gol] = []

    def parse_script(self, script: str):
        lines = script.splitlines()
        line_numbers = reversed(range(len(lines)))
        lines = reversed(lines)
        pending_gol = Gol()

        for line_number, line in zip(line_numbers, lines):
            line_number += 1
            line = line.strip()
            key_space_position = line.find(Keywords.SPACE.value)
            code = line[:key_space_position]
            value = line[key_space_position + 1:].strip()

            if code == Keywords.GOL.value:

                pending_gol.is_completed = value.endswith(Keywords.CHECK.value)
                pending_gol.name = value
                self._gols.append(copy(pending_gol))
                pending_gol = Gol()

            elif code == Keywords.TSK.value:
                pending_gol.tasks.append(value)

            elif code == Keywords.ALL.value or code == Keywords.ANY.value:
                pending_gol.is_all = True if code == Keywords.ALL.value else False

                for sub_value in value.split(Keywords.SPACE.value):
                    found_link = False
                    modifier = ''

                    if sub_value.endswith(Keywords.CRITICAL.value):
                        sub_value = sub_value[:-1]
                        modifier = Keywords.CRITICAL.value
                    elif sub_value.endswith(Keywords.OPTIONAL.value):
                        sub_value = sub_value[:-1]
                        modifier = Keywords.OPTIONAL.value

                    for gol in self._gols:
                        if gol.name == sub_value:
                            pending_gol.reference.append((gol, modifier))
                            found_link = True
                            break

                    if not found_link:
                        pending_gol.non_reference.append((sub_value, modifier))

            elif code == Keywords.RETURN.value or code == '' or None:
                pass

            else:
                raise SyntaxError(f'Unrecognized key "{code}" on line {line_number}')

        return self._gols
