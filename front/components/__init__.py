class Component:

    def __init__(self, document, element_id):
        self._element = document[element_id]
        self.hide()

    def hide(self):
        self._element.style.display = 'none'

    def show(self):
        self._element.style.display = 'flex'
