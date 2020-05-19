class Component:
    root = 'ViewRoot'

    def __init__(self, document, template_id=None):
        if template_id is None:
            template_id = type(self).__name__ + Component.__name__
        self._document = document
        template = document[template_id]
        clone = template.content.cloneNode(True)
        root = document[Component.root]
        root.appendChild(clone)
        self._element = document[type(self).__name__]
        self._default_display_style = self._element.style.display
        self.hide()

    def hide(self):
        self._element.style.display = 'none'

    def show(self):
        self._element.style.display = self._default_display_style
        self._element.focus()
