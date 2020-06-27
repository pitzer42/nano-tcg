from abc import ABC


class PlayerClient(ABC):

    def request_player_id(self):
        raise NotImplementedError()

    def request_match_id_and_password(self, waiting_matches):
        raise NotImplementedError()

    def notify_unavailable_player_id(self, player_id):
        raise NotImplementedError()

    def notify_wrong_password(self, match):
        pass

    def notify_match_has_already_started(self, match):
        raise NotImplementedError()
