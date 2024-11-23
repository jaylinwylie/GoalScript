from copy import copy
from enum import StrEnum
from pathlib import Path

from gol import Gol


class Keywords(StrEnum):
    GOL = 'GOL'
    GOAL = 'GOAL'
    TSK = 'TSK'
    TASK = 'TASK'
    SPACE = ' '
    ALL = 'ALL'
    ANY = 'ANY'
    CHECK = '/'
    SUB_GOL = '.'
    CRITICAL = '!'
    OPTIONAL = '?'
    POINTER = '@'

class GolScriptParser:
    def __init__(self):
        self._gols: list[Gol] = []

    def parse_script(self, script_path):

        with open(script_path) as golscript:
            script = golscript.read()

        lines = list(reversed(script.splitlines()))
        line_numbers = reversed(range(1, len(lines) + 1))
        pending_gol = Gol()

        for line_number, line in zip(line_numbers, lines):
            line = line.strip()

            if len(line) == 0:
                continue

            code, value = tuple(line.split(Keywords.SPACE, 1))

            if code == Keywords.GOL.value or code == Keywords.GOAL.value:
                if value.endswith(Keywords.CHECK):
                    pending_gol.is_completed = True
                    value = value[:-1]
                
                pending_gol.name = value
                self._gols.append(copy(pending_gol))
                pending_gol = Gol()

            elif code == Keywords.TSK.value or code == Keywords.TASK.value:
                pending_gol.tasks.append(value)

            elif code == Keywords.ALL or code == Keywords.ANY:
                pending_gol.is_all = True if code == Keywords.ALL else False

                for sub_gol_and_mod in value.split(Keywords.SPACE):
                    sub_gol, mod = sub_gol_and_mod[:-1], sub_gol_and_mod[-1]

                    if sub_gol.startswith(Keywords.POINTER):
                        sub_gol = sub_gol[1:]
                        recursive_parser = GolScriptParser()
                        folder = script_path.parent
                        golscript = folder / f'{sub_gol}.golscript'
                        self._gols.extend(recursive_parser.parse_script(golscript))

                    is_leaf = True
                    for gol in self._gols:
                        if gol.name == sub_gol:
                            is_leaf = False
                            break

                    if is_leaf:
                        match mod:
                            case Keywords.SUB_GOL:
                                pending_gol.leaf.add(sub_gol)
                            case Keywords.CRITICAL:
                                pending_gol.critical_leaf.add(sub_gol)
                            case Keywords.OPTIONAL:
                                pending_gol.optional_leaf.add(sub_gol)
                    else:
                        match mod:
                            case Keywords.SUB_GOL:
                                pending_gol.branch.add(gol)
                            case Keywords.CRITICAL:
                                pending_gol.critical_branch.add(gol)
                            case Keywords.OPTIONAL:
                                pending_gol.optional_branch.add(gol)

            else:
                raise SyntaxError(f'Unrecognized key "{code}" on line {line_number}')

        return self._gols
