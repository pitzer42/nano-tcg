class WaitForPriority:

    def __init__(self, matches):
        self.matches = matches

    async def execute(self, player_id, match_id):
        match = await self.matches.get_by_id(match_id)
        await match.priority_change(player_id)
        await match.channel.receive()
        return match.current_player == player_id

