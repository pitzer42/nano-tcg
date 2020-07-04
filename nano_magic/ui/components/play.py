import json
from functools import partial

from nano_magic.ui.components import Component
from nano_magic.ui.scryfall import get_images_url


class PlayView(Component):
    hand_container = 'handContainer'
    pass_button = 'passButton'

    def __init__(self, document):
        super(PlayView, self).__init__(document)
        self.on_choice = lambda: None
        self.on_pass = lambda: None
        self._hand_container = document[PlayView.hand_container]
        self._pass_button = document[PlayView.pass_button]
        self._pass_button.onclick = self.bridge

    def bridge(self, event):
        self.on_pass(event)

    def set_options(self, options):
        self._hand_container.innerHTML = ''
        options = json.loads(options)

        def display_option(option_i, image_url):
            img = self._document.createElement('img')
            img.src = image_url
            self._hand_container.appendChild(img)
            img.onclick = lambda *args: self.on_choice(option_i)

        n_options = len(options)
        for i in range(n_options):
            option = options[i]
            get_images_url(
                option,
                partial(display_option, i)
            )
