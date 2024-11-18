class Gol:
    def __init__(self):
        self.is_all: bool = True
        self.is_completed: bool = False
        self.name: str | None = None
        self.tasks: list = []
        self.non_reference: list[tuple[str, str]] = []
        self.reference: list[tuple[Gol, str]] = []


class GolArray(list):
    def __init__(self, goals: list[Gol]):
        super().__init__(goals)
