class Gol:
    def __init__(self):
        self.is_all: bool = True
        self.is_completed: bool = False

        self.name: str | None = None
        self.tasks: list = []

        self.leaf: set[str] = set()
        self.critical_leaf: set[str] = set()
        self.optional_leaf: set[str] = set()

        self.branch: set[Gol] = set()
        self.critical_branch: set[Gol] = set()
        self.optional_branch: set[Gol] = set()

