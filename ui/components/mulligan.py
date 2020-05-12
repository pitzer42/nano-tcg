import json

from ui.components import Component
from ui.scryfall import get_images_url


class MulliganView(Component):
    wait_container = 'mulliganContainer'
    keep_button = 'ḱeepButton'
    mulligan_button = 'mulliganButton'
    cards_mulligan_container = 'cardsMulliganContainer'

    def __init__(self, document):
        super(MulliganView, self).__init__(document)
        self._keep_button = document[MulliganView.keep_button]
        self._mulligan_button = document[MulliganView.mulligan_button]

    def set_keep_action(self, action):
        self._keep_button.bind('click', action)

    def set_mulligan_action(self, action):
        self._mulligan_button.bind('click', action)

    def show(self, cards: str):
        def display_image(image_url):
            img = self._document.createElement('img')
            img.src = image_url
            image_container.appendChild(img)

        image_container = self._document[MulliganView.cards_mulligan_container]
        image_container.innerHTML = ''
        self._element.appendChild(image_container)  # TODO remove?
        cards = json.loads(cards)

        for card in cards:
            get_images_url(card, display_image)

        super(MulliganView, self).show()
