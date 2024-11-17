class Gol:
    def __init__(self):
        self.is_all: bool = True
        self.is_completed: bool = False
        self.name: str | None = None
        self.tasks: list = []
        self.non_reference: list[str] = []
        self.reference: list[Gol] = []
        self.optional: list[Gol] = []


class GolArray(list):
    def __init__(self, goals: list[Gol]):
        super().__init__(goals)
