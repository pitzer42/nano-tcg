class Player:

    def __init__(self, player_id):
        self.id = player_id

    def to_dict(self) -> dict:
        return dict(
            id=self.id
        )
