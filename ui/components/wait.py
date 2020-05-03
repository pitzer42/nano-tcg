from ui.components import Component


class WaitComponent(Component):
    _wait_container = 'waitContainer'

    def __init__(self, document):
        super(WaitComponent, self).__init__(
            document,
            WaitComponent._wait_container
        )
