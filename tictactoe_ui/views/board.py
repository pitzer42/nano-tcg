from tictactoe_ui.component import UIComponent


class BoardView(UIComponent):
    children = [
        'board_table'
    ]

    def display(self, board):
        self.board_table.innerHTML = None

        for row in board:
            tr = self.doc.createElement('tr')
            for cell in row:
                td = self.doc.createElement('td')
                if cell == '*':
                    cell_input = self.doc.createElement('button')
                    td.appendChild(cell_input)
                else:
                    td.innerText = cell
                tr.appendChild(td)
            self.board_table.appendChild(tr)
