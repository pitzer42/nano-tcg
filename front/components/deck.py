class DeckComponent:

    _deck_container = 'deckContainer'
    _deck_input = 'deckInput'
    _deck_end_button = 'deckEndButton'

    def __init__(self, doc):
        self._container = doc[DeckComponent._deck_container]
        self._input = doc[DeckComponent._deck_input]
        self._ok = doc[DeckComponent._deck_end_button]
        self.hide()

    def get_deck(self):
        return self._input.value

    def set_deck_end_action(self, action):
        self._ok.bind(
            'click',
            action
        )

    def hide(self):
        self._container.style.display = 'none'

    def show(self):
        self._input.value = ''
        self._container.style.display = 'flex'
