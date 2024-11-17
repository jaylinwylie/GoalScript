from gol import GolArray
from mermaid_renderer import GolRenderer
from golscript_parser import GolScriptParser

GOLSCRIPT = 'Examples/EpisodeHandedOff.golscript'

with open(GOLSCRIPT) as file:
    golscript = file.read()

parser = GolScriptParser()
renderer = GolRenderer()

gols: GolArray = parser.parse_script(golscript)
mermaid_script = renderer.gols_to_mermaid(gols)

with open('diagram.md', 'w') as file:
    file.write(mermaid_script)