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
    to_hide.hide()
    to_show.show()


def fill_table(document, data_dicts, table_element=None, **header_aliases):
    table_element = table_element or document.createElement('table')
    if len(data_dicts) == 0 and len(header_aliases) == 0:
        return table_element

    if len(header_aliases) == 0:
        header_aliases = {key: key for key in data_dicts[0].keys()}

    tr = document.createElement('tr')
    for alias in header_aliases.values():
        th = document.createElement('th')
        th.innerText = alias
        tr.appendChild(th)

    thead = document.createElement('thead')
    thead.appendChild(tr)

    table_element.appendChild(thead)

    tbody = document.createElement('tbody')
    for data in data_dicts:
        tr = document.createElement('tr')
        for header in header_aliases.keys():
            td = document.createElement('td')
            td.innerText = data[header]
            tr.appendChild(td)
        tbody.appendChild(tr)
    table_element.appendChild(tbody)

    return table_element


class View:
    _children_attr_name = 'children'

    def __init__(self,
                 document,
                 template_id=None,
                 parent_id='root'):

        view_type = type(self)

        default_template_id = view_type.__name__
        template_id = template_id or default_template_id
        element = instantiate_template(document, template_id)

        if parent_id in document:
            parent = document[parent_id]
        else:
            parent = document.body
        parent.appendChild(element)

        if hasattr(view_type, View._children_attr_name):
            self_attrs = self.__dict__
            view_type_attrs = view_type.__dict__
            for child in view_type_attrs[View._children_attr_name]:
                name_query = f'[name={child}]'
                child_element = element.querySelector(name_query)
                self_attrs[child] = child_element

        self.doc = document
        self.element = element
        self._default_style_display = element.style.display
        self.hide()

    def hide(self):
        self.element.style.display = 'none'

    def show(self):
        self.element.style.display = self._default_style_display
        self.element.focus()
