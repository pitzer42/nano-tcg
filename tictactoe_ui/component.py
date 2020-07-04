def remove_children(element):
    for child in element.children:
        child.remove()


def create_table(doc, data_dicts, table=None, **header_aliases):
    table = table or doc.createElement('table')
    if len(data_dicts) == 0 and len(header_aliases) == 0:
        return table

    if len(header_aliases) == 0:
        header_aliases = {key: key for key in data_dicts[0].keys()}

    tr = doc.createElement('tr')
    for alias in header_aliases.values():
        th = doc.createElement('th')
        th.innerText = alias
        tr.appendChild(th)

    thead = doc.createElement('thead')
    thead.appendChild(tr)

    table.appendChild(thead)

    tbody = doc.createElement('tbody')
    for data in data_dicts:
        tr = doc.createElement('tr')
        for header in header_aliases.keys():
            td = doc.createElement('td')
            td.innerText = data[header]
            tr.appendChild(td)
        tbody.appendChild(tr)
    table.appendChild(tbody)

    return table


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
