def instantiate_template(document, template_id):
    template = document[template_id]
    instance = template.content.cloneNode(True)
    if instance.firstElementChild.id:
        instance.firstElementChild.id = f'{instance.firstElementChild.id}_{id(instance)}'
    else:
        instance.firstElementChild.id = f'{template_id}_{id(instance)}'
    instance_id = instance.firstElementChild.id
    document.body.append(instance)
    return document[instance_id]


def swap_view(to_hide, to_show):
    def _swap_view(*args, **kwargs):
        to_hide.hide()
        to_show.show()

    return _swap_view()


class UIComponent:

    def __init__(self, document, template_id=None, parent_id='root'):
        self.doc = document

        template_id = template_id or type(self).__name__
        self.element = instantiate_template(document, template_id)

        if parent_id in document:
            parent = document[parent_id]
        else:
            parent = document.body
        parent.appendChild(self.element)

        if hasattr(type(self), 'children'):
            for child in type(self).children:
                self.__dict__[child] = self.get_child_element_by_name(child)

        self._default_style_display = self.element.style.display
        self.hide()

    def get_child_element_by_name(self, child_name: str):
        return self.element.querySelector(f'[name={child_name}]')

    def hide(self):
        self.element.style.display = 'none'

    def show(self):
        self.element.style.display = self._default_style_display
        self.element.focus()
