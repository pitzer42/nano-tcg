from browser import ajax, console

from ui.components import Component


class MulliganComponent(Component):
    _wait_container = 'mulliganContainer'
    _keep_button_id = 'ḱeepButton'
    _mulligan_button_id = 'mulliganButton'
    _cards_mulligan_container_id = 'cardsMulliganContainer'

    def __init__(self, document):
        super(MulliganComponent, self).__init__(
            document,
            MulliganComponent._wait_container
        )
        self._keep_button = document[MulliganComponent._keep_button_id]
        self._mulligan_button = document[MulliganComponent._mulligan_button_id]

    def set_keep_action(self, action):
        self._keep_button.bind('click', action)

    def set_mulligan_action(self, action):
        self._mulligan_button.bind('click', action)

    def show(self, cards):
        console.log(type(cards))
        return

        super(MulliganComponent, self).show()

        images = self._document[MulliganComponent._cards_mulligan_container_id]
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

