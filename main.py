from goal import GoalArray
from mermaid_renderer import list_of_goals_to_mermaid
from parser import GolScriptParser

GOLSCRIPT = 'Today.golscript'

with open(GOLSCRIPT) as file:
    golscript = file.read()

goals: GoalArray = GolScriptParser().parse_script(golscript)

with open('diagram.md', 'w') as file:
    file.write(f'```mermaid\n{list_of_goals_to_mermaid(goals)}\n```')