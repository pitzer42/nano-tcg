from . import View


class BoardView(View):
    children = [
        'board_table'
    ]

    def display(self, board):
        self.board_table.innerHTML = ''
        for row in board:
            tr = self.doc.createElement('tr')
            for cell in row:
                td = self.doc.createElement('td')
                td.innerText = cell
                tr.appendChild(td)
            self.board_table.appendChild(tr)

    def enable_play(self, options, on_play):

        def play_button_callback_factory(index, func):
            def callback(*args, **kwargs):
                return func(index)

            return callback

        for i, option in enumerate(options):
            row_index = int(option['row'])
            row = self.board_table.children[row_index]
            column_index = int(option['column'])
            cell = row.children[column_index]
            cell.innerText = ''
            button = self.doc.createElement('button')
            button.textContent = '*'
            button.onclick = play_button_callback_factory(i, on_play)
            cell.appendChild(button)
