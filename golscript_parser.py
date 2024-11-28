from copy import copy
from enum import Enum

from gol import Gol


class Keywords(Enum):
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

    def parse_script(self, script):
        lines = list(reversed(script.splitlines()))
        line_numbers = reversed(range(1, len(lines) + 1))
        pending_gol = Gol()

        for line_number, line in zip(line_numbers, lines):
            line = line.strip()

            if len(line) == 0:
                continue

            if line.startswith(Keywords.POINTER.value):
                value = line[1:]
                recursive_parser = GolScriptParser()
                golscript = f'Gols/{value}.golscript'

                with open(golscript) as file:
                    new_script = file.read()

                self._gols.extend(recursive_parser.parse_script(new_script))
                continue

            else:
                code, value = tuple(line.split(Keywords.SPACE.value, 1))
                code = code.upper()

                if code == Keywords.GOL.value or code == Keywords.GOAL.value:
                    if value.endswith(Keywords.CHECK.value):
                        pending_gol.is_completed = True
                        value = value[:-1]

                    pending_gol.name = value
                    self._gols.append(copy(pending_gol))
                    pending_gol = Gol()

                elif code == Keywords.TSK.value or code == Keywords.TASK.value:
                    pending_gol.tasks.append(value)

                elif code == Keywords.ALL.value or code == Keywords.ANY.value:
                    pending_gol.is_all = True if code == Keywords.ALL.value else False

                    for sub_gol_and_mod in value.split(Keywords.SPACE.value):
                        sub_gol, mod = sub_gol_and_mod[:-1], sub_gol_and_mod[-1]

                        if sub_gol.startswith(Keywords.POINTER.value):
                            sub_gol = sub_gol[1:]
                            recursive_parser = GolScriptParser()
                            golscript = f'Gols/{sub_gol}.golscript'

                            with open(golscript) as file:
                                new_script = file.read()

                            self._gols.extend(recursive_parser.parse_script(new_script))

                        is_leaf = True
                        pointed_gol = None
                        for gol in self._gols:
                            if gol.name == sub_gol:
                                is_leaf = False
                                pointed_gol = gol
                                break

                        if is_leaf:
                            match mod:
                                case Keywords.SUB_GOL.value:
                                    pending_gol.leaf.add(sub_gol)
                                case Keywords.CRITICAL.value:
                                    pending_gol.critical_leaf.add(sub_gol)
                                case Keywords.OPTIONAL.value:
                                    pending_gol.optional_leaf.add(sub_gol)
                        else:
                            match mod:
                                case Keywords.SUB_GOL.value:
                                    pending_gol.branch.add(pointed_gol)
                                case Keywords.CRITICAL.value:
                                    pending_gol.critical_branch.add(pointed_gol)
                                case Keywords.OPTIONAL.value:
                                    pending_gol.optional_branch.add(pointed_gol)

                else:
                    raise SyntaxError(f'Unrecognized key "{code}" on line {line_number}')

        return self._gols
