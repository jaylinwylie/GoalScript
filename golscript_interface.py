import logging

import ipywidgets as widgets
from IPython.display import display, Markdown
from mermaid_renderer import GolRenderer
from golscript_parser import GolScriptParser

# Create the widgets
code_input = widgets.Textarea(
        layout=widgets.Layout(width='99%', height='300px')
)
button = widgets.Button(
        description="Render",
        layout=widgets.Layout(width='99%', height='40px')
)
output_area = widgets.Output(
        layout=widgets.Layout(width='99%', height='100%')
)

last_good_render: str = ''


# Define the render function
def render(_):
    global last_good_render

    with output_area:
        golscript = code_input.value
        try:
            renderer = GolRenderer()
            parser = GolScriptParser()
            gols = parser.parse_script(golscript)
            mermaid_diagram = renderer.gols_to_mermaid(gols)
            last_good_render = mermaid_diagram
            output_area.clear_output()
            display(Markdown(mermaid_diagram))
        except Exception as e:
            pass
            mermaid_diagram = last_good_render



code_input.observe(render)

display(code_input, output_area)
