from gol import Gol


class GolRenderer:
    @staticmethod
    def gols_to_mermaid(gols):
        generated = set()
        mermaid_diagram = ['graph TD']
        for gol in gols:
            mermaid_str = []
            if gol.name in generated:
                return mermaid_str

            generated.add(gol.name)
            has_tasks = len(gol.tasks) > 0

            if has_tasks:
                gol_name = gol.name + 'Tasks'
                task_str = "\n".join([task for task in gol.tasks])
                task_str = f'"`_{task_str}_`"'
                if gol.is_all:
                    mermaid_str.append(f'{gol_name}[[{task_str}]] --> {gol.name}')
                else:
                    mermaid_str.append(f'{gol_name}{{{task_str}}} --> {gol.name}')

            else:
                gol_name = gol.name
                if gol.is_all:
                    mermaid_str.append(f'{gol_name}[{gol.name}]')
                else:
                    mermaid_str.append(f'{gol_name}{{{gol.name}}}')

            for leaf in gol.critical_leaf:
                mermaid_str.append(f'{leaf}({leaf}) ===== {gol_name}')
            for leaf in gol.leaf:
                mermaid_str.append(f'{leaf}({leaf}) ---- {gol_name}')
            for leaf in gol.optional_leaf:
                mermaid_str.append(f'{leaf}({leaf}) ..- {gol_name}')

            for branch in gol.critical_branch:
                mermaid_str.append(f'{branch.name} ==== {gol_name}')
            for branch in gol.branch:
                mermaid_str.append(f'{branch.name} --- {gol_name}')
            for branch in gol.optional_branch:
                mermaid_str.append(f'{branch.name} .- {gol_name}')

            mermaid_output = mermaid_str
            mermaid_diagram.extend(mermaid_output)
        return '```mermaid\n' + '\n'.join(mermaid_diagram) + '\n```'
