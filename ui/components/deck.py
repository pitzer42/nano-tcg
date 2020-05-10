from ui.components import Component


class DeckView(Component):
    _deck_input = 'deckInput'
    _deck_end_button = 'deckEndButton'

    def __init__(self, document):
        super(DeckView, self).__init__(document)
        self._input = document[DeckView._deck_input]
        self._ok = document[DeckView._deck_end_button]

    def get_deck(self):
        return self._input.value

    def set_action(self, action):
        self._ok.bind(
            'click',
            action
        )

    def reset(self):
        self._input.value = ''
