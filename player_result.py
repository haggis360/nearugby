class PlayerResult:
    def __init__(
        self, user_id: int, user_name: str, outcome_total: int, outcome_diff: int
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.outcome_total = outcome_total
        self.outcome_diff = outcome_diff

    def __str__(self):
        return f"PlayerResult {self.user_id} - {self.user_name} outcome {self.outcome_total} diff {self.outcome_diff}"
