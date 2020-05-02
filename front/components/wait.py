from front.components import Component


class WaitComponent(Component):
    _wait_container = 'waitContainer'

    def __init__(self, doc):
        super(WaitComponent, self).__init__(WaitComponent._wait_container)
