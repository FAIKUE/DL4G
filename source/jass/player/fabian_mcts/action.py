class Action:
    def __init__(self):
        self.player_nr = 0
        self.win_score = 0.0
        self.visit_count = 0
        self.round = None
        self.card = None

    def increment_visit(self):
        self.visit_count += 1
