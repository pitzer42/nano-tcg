from ui.components import Component


class DeckComponent(Component):
    _deck_container = 'deckContainer'
    _deck_input = 'deckInput'
    _deck_end_button = 'deckEndButton'

    def __init__(self, document):
        super(DeckComponent, self).__init__(
            document,
            DeckComponent._deck_container
        )
        self._input = document[DeckComponent._deck_input]
        self._ok = document[DeckComponent._deck_end_button]

    def get_deck(self):
        return self._input.value

    def set_deck_end_action(self, action):
        self._ok.bind(
            'click',
            action
        )

    def reset(self):
        self._input.value = ''
