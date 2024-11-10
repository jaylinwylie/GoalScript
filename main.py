import re
from itertools import islice

GOLSCRIPT_TOKENS = [
        ('CALL_GOAL', r'GOL'),
        ('CALL_TASK', r'TSK'),
        ('REQUIRE_ALL', r'ALL'),
        ('REQUIRE_ANY', r'ANY'),
        ('REQUIREMENT_REFERENCE', r'(\w+)(?=\!)'),  # Words ending with '!'
        ('REQUIREMENT', r'(\w+)(?=\.)'),  # Words ending with '.'
        ('GOAL_NAME', r'\w+(?=:)\:'),  # Words ending with ':'
        ('TASK_DETAIL', r'.+?(?=;)'),  # Any sequence ending with ';'
]

TOKENIZER_REGEX = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in GOLSCRIPT_TOKENS))


def lexer(script: str) -> list[tuple[str, str | None]]:
    token_list = []
    for match in TOKENIZER_REGEX.finditer(script):
        token_type = match.lastgroup
        token_value = match.group(token_type).strip() if token_type else None
        token_list.append((token_type, token_value))
    return token_list


def process_goal_token(_goals, tokens_iter):
    goal_name = next(tokens_iter)[1]
    _goals[goal_name] = {
            'requirements'          : [],
            'requirement_references': [],
            'requirement_type'      : '',
            'tasks'                 : []
    }
    return goal_name


def process_task_token(_goals, current_goal, tokens_iter):
    task_detail = next(tokens_iter)[1]
    _goals[current_goal]['tasks'].append(task_detail)


def parse(tokens: list[tuple[str, str]]) -> dict[str, dict[str, list[str] | str]]:
    _goals = {}
    current_goal = None
    tokens_iter = iter(tokens)

    for token_type, token_value in tokens_iter:
        if token_type == 'CALL_GOAL':
            current_goal = process_goal_token(_goals, tokens_iter)
        elif token_type == 'CALL_TASK' and current_goal:
            process_task_token(_goals, current_goal, tokens_iter)
        elif token_type in ['REQUIRE_ALL', 'REQUIRE_ANY'] and current_goal:
            req_type = 'all' if token_type == 'REQUIRE_ALL' else 'any'
            _goals[current_goal]['requirement_type'] = req_type
            for token in tokens_iter:
                if token[0] not in ['REQUIREMENT', 'REQUIREMENT_REFERENCE']:
                    break
                req_type_actual, req_detail = token
                if req_type_actual == 'REQUIREMENT_REFERENCE':
                    _goals[current_goal]['requirement_references'].append(req_detail)
                else:
                    _goals[current_goal]['requirements'].append(req_detail)
        else:
            continue

    return _goals


golscript_code = """
GOL CleanFountain:  
TSK Clean the cat's water fountain; 
ALL Water. CleanEmptyFountain!  
GOL CleanEmptyFountain:  
TSK Re-assemble;  
ALL WashedAssembly! CleanFilter!  
GOL WashedAssembly:  
TSK Wash assembly;  
ALL Water. DirtyAssembly!  
GOL CleanFilter:  
TSK Check for filters;  
ANY NewFilter! WashedFilter!  
GOL NewFilter:  
TSK Get a new filter from the box;  
ALL AtCatDrawr. FilterBox.  
GOL WashedFilter:  
TSK Wash filter;  
TSK Order more;  
ALL Water. DirtyFilter! PurchaseOrder.  
GOL DirtyFilter:  
TSK Extract filter;  
ALL DirtyAssembly!  
GOL DirtyAssembly:  
TSK Dis-assemble;  
ALL DirtyFountain!  
GOL DirtyFountain:  
TSK Empty the fountain;  
ALL AtSink. DirtyFullFountain.
"""

tokens = lexer(golscript_code)
goals = parse(tokens)

import pprint

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(goals)