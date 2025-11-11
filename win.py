
class Win:
    def __init__(self, pieces):
        self.pieces = pieces  

    def check_winner(self, next_turn_color: str):
        """
        Returns 'r' if red has captured all green pieces,
        'g' if green has captured all red pieces,
        or None if no winner yet.
        """
        opponent = "g" if next_turn_color == "r" else "r"

        for piece in self.pieces.positions.values():
            if piece and piece[0] == opponent:
                return None  # means opponent still has pieces
        return next_turn_color
