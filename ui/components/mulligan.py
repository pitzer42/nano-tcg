import json

from browser import ajax

from ui.components import Component


class MulliganView(Component):
    _wait_container = 'mulliganContainer'
    _keep_button_id = 'ḱeepButton'
    _mulligan_button_id = 'mulliganButton'
    _cards_mulligan_container_id = 'cardsMulliganContainer'

    def __init__(self, document):
        super(MulliganView, self).__init__(document)
        self._keep_button = document[MulliganView._keep_button_id]
        self._mulligan_button = document[MulliganView._mulligan_button_id]

    def set_keep_action(self, action):
        self._keep_button.bind('click', action)

    def set_mulligan_action(self, action):
        self._mulligan_button.bind('click', action)

    def show(self, cards):
        cards = json.loads(cards)

        super(MulliganView, self).show()

        images = self._document[MulliganView._cards_mulligan_container_id]
        images.innerHTML = ''
        self._element.appendChild(images)

        def foo(response):
            start = response.text.index('small')
            start += len('small') + 3
            end = response.text.index(',', start)
            end -= 1
            sub = response.text[start:end]

            img = self._document.createElement('img')
            img.src = sub
            images.appendChild(img)

        for card in cards:
            request = ajax.Ajax()
            request.bind('complete', foo)
            request.open(
                'GET',
                'https://api.scryfall.com/cards/named?exact=' + card.replace(' ', '+')
            )
            request.send()

