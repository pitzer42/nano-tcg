import json

from ui.components import Component
from ui.scryfall import get_images_url


class BoardView(Component):
    board_container = 'boardContainer'

    def __init__(self, document):
        super(BoardView, self).__init__(document)
        self._board_container = document[BoardView.board_container]

    def set_board(self, cards):
        self._board_container.innerHTML = ''
        cards = json.loads(cards)

        def display_option(image_url):
            img = self._document.createElement('img')
            img.src = image_url
            self._board_container.appendChild(img)

        for card in cards:
            get_images_url(
                card,
                display_option
            )

        super(BoardView, self).show()
