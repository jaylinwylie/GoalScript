class Goal:
    def __init__(self):
        self.is_all: bool | None = None
        self.is_completed: bool = False
        self.name: str | None = None
        self.tasks: list = []
        self.non_reference: list[str] = []
        self.reference: list[Goal] = []
        self.optional: list[Goal] = []


class GoalArray:
    def __init__(self, goals: list[Goal]):
        self.goals = goals
