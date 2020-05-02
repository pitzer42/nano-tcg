class WaitComponent:

    _wait_container = 'waitContainer'

    def __init__(self, doc):
        self._container = doc[WaitComponent._wait_container]
        self.hide()

    def hide(self):
        self._container.style.display = 'none'

    def show(self):
        self._container.style.display = 'flex'
