from pathlib import Path

from gol import Gol
from mermaid_renderer import GolRenderer
from golscript_parser import GolScriptParser


parser = GolScriptParser()
renderer = GolRenderer()

folder = Path('gols')

gols: list[Gol] = parser.parse_script('@END')
...
mermaid_script = renderer.gols_to_mermaid(gols)

diagram_path = folder / 'diagram.md'
with open(diagram_path, 'w') as file:
    file.write(mermaid_script)
