from nano_magic.ui.components import Component


class DeckView(Component):
    _deck_input = 'deckInput'
    _deck_end_button = 'deckEndButton'

    def __init__(self, document):
        super(DeckView, self).__init__(document)
        self._input = document[DeckView._deck_input]
        self._ok = document[DeckView._deck_end_button]
        self._input.value = "30 Serra Angel\n30 Plains"

    def get_deck(self):
        return self._input.value

    def set_action(self, action):
        self._ok.bind(
            'click',
            action
        )

    def reset(self):
        self._input.value = ''

    def show(self):
        super(DeckView, self).show()
        self._input.focus()
