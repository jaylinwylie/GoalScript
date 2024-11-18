from gol import Gol


class GolRenderer:

    @staticmethod
    def goal_to_mermaid(self, gol: Gol, generated: set):
        mermaid_str = []
        if gol.name in generated:
            return mermaid_str
        generated.add(gol.name)

        if len(gol.tasks) > 0:
            task_name = gol.name + 'Tasks'
            task_str = "\n".join([task for task in gol.tasks])
            if gol.is_all:
                mermaid_str.append(f'{task_name}[[{task_str}]] ==> {gol.name}')
            else:
                mermaid_str.append(f'{task_name}{{{task_str}}} ==> {gol.name}')

        else:
            task_name = gol.name
            if gol.is_all:
                mermaid_str.append(f'{task_name}[{gol.name}]')
            else:
                mermaid_str.append(f'{task_name}{{{gol.name}}}')

        for non_ref in gol.non_reference:
            mermaid_str.append(f"{non_ref}(({non_ref})) ---> {task_name}")

        for ref in gol.reference:
            mermaid_str.append(f"{ref.name} --> {task_name}")


        return mermaid_str

    def gols_to_mermaid(self, _goals):
        generated = set()
        mermaid_diagram = ['graph TD']
        for goal in _goals:
            mermaid_diagram.extend(self.goal_to_mermaid(self, goal, generated))
        return '```mermaid\n' + '\n'.join(mermaid_diagram) + '\n```'
