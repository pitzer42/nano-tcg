from abc import ABC

from channels import Channel
from features.indentify_client.clients import IdentifiableClient
from features.join_match.client import JoinMatchClient
from features.select_or_create_match.clients import SelectOrCreateMatchClient


class Client(IdentifiableClient, SelectOrCreateMatchClient, JoinMatchClient):

    def __init__(self, channel: Channel):
        self._channel = channel
