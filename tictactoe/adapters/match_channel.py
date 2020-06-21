from adapters.match_channel import MatchChannel
from channels import Channel


class TicTacToeMatchClient(MatchChannel):

    def __init__(self, inner_channel: Channel):
        super(TicTacToeMatchClient, self).__init__(inner_channel)
