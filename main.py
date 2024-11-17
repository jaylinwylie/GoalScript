from pathlib import Path

from gol import GolArray
from mermaid_renderer import GolRenderer
from golscript_parser import GolScriptParser

examples_path = Path('Examples')

for golscript_path in examples_path.glob('*.golscript'):
    with open(golscript_path) as file:
        golscript = file.read()

    parser = GolScriptParser()
    renderer = GolRenderer()

    gols: GolArray = parser.parse_script(golscript)
    mermaid_script = renderer.gols_to_mermaid(gols)
    file_name = golscript_path.stem

    diagram_path = examples_path / f'{file_name}.md'
    with open(diagram_path, 'w') as file:
        file.write(mermaid_script)
