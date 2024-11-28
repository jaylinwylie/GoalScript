from pathlib import Path

from gol import GolArray
from mermaid_renderer import GolRenderer
from golscript_parser import GolScriptParser


parser = GolScriptParser()
renderer = GolRenderer()

folder = Path('Gols')

gols: GolArray = parser.parse_script('@END')
...
mermaid_script = renderer.gols_to_mermaid(gols)

diagram_path = folder / 'diagram.md'
with open(diagram_path, 'w') as file:
    file.write(mermaid_script)
