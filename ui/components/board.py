import json

from ui.components import Component
from ui.scryfall import get_images_url


class BoardView(Component):

    hand = 'BoardHandContainer'
    
    def __init__(self, document):
        super(BoardView, self).__init__(document)
        self.hand = document[BoardView.hand]

    def set_hand(self, cards):
        self.hand.innerHTML = ''

        def display_image(image_url):
            img = self._document.createElement('img')
            img.src = image_url
            self.hand.appendChild(img)

        cards = json.loads(cards)
        for card in cards:
            get_images_url(card, display_image)

        super(BoardView, self).show()


