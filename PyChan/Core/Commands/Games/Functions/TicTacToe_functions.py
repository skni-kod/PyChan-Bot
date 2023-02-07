from random import choice

import select

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import View, StringSelect, Button


class Game:
    def __init__(self, difficulty: int, user: nextcord.User):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.difficulty = difficulty
        self.user = user
        self.winner = None
        self.win_filed = [[False for _ in range(3)] for _ in range(3)]

    def prepare_view(self):
        view = View()
        for row in range(1, 4):
            for column in range(1, 4):
                temp = self.board[row - 1][column - 1]
                button = Button(label="​",
                                style=nextcord.ButtonStyle.gray,
                                row=row,
                                custom_id=f"{row-1},{column-1}",
                                disabled=True if temp is not None or self.winner is not None else False)
                if temp is not None:
                    button.emoji = '🅾️' if temp=="user" else '❎'

                if self.winner =="user":
                    button.style = nextcord.ButtonStyle.red if self.win_filed[row-1][column-1] else nextcord.ButtonStyle.gray
                elif self.winner =="pc":
                    button.style = nextcord.ButtonStyle.green if self.win_filed[row-1][column-1] else nextcord.ButtonStyle.gray

                button.callback = self.button_callback
                view.add_item(button)

        return view

    async def button_callback(self, interaction: nextcord.Interaction):
        if self.user != interaction.user:
            await interaction.response.send_message("To nie twoja gra! Rozpocznij własną poleceniem `kik`", ephemeral=True)
            return

        position = [int(a) for a in interaction.data['custom_id'].split(',')]
        self.board[position[0]][position[1]] = "user"

        self.is_finished()

        if self.winner is None and not self.board_full():
            if self.difficulty == 1:
                self.choose_random()
            elif self.difficulty == 2:
                self.ai_move()
            self.is_finished()

        view = self.prepare_view()

        if self.winner is None:
            if self.board_full():
                await interaction.response.edit_message(content=f"Gra zakończona remisem.", view=view)
            else:
                await interaction.response.edit_message(content=f"Ruch gracza {self.user.mention}:", view=view)
        else:
            if self.winner == "user":
                await interaction.response.edit_message(content=f"Gratulacje {self.user.mention}, udało Ci się wygrać", view=view)
            elif self.winner == "pc":
                await interaction.response.edit_message(content=f"Niestety {self.user.mention}, tym razem przegrałeś", view=view)

    def is_finished(self, board=None, set_winner=True):
        if board is None:
            board = self.board

        for row in range(3):
            if board[row][0] is not None and board[row][0] == board[row][1] and board[row][1] == board[row][2]:
                if set_winner:
                    self.winner = board[row][0]
                    self.win_filed[row][0] = True
                    self.win_filed[row][1] = True
                    self.win_filed[row][2] = True
                return board[row][0]

        if board[0][0] is not None and board[0][0] == board[1][1] and board[0][0] == board[2][2]:
            if set_winner:
                self.winner = board[0][0]
                self.win_filed[0][0] = True
                self.win_filed[1][1] = True
                self.win_filed[2][2] = True
            return board[0][0]

        if board[0][2] is not None and board[0][2] == board[1][1] and board[0][2] == board[2][0]:
            if set_winner:
                self.winner = board[0][2]
                self.win_filed[0][2] = True
                self.win_filed[1][1] = True
                self.win_filed[2][0] = True
            return board[0][2]

        for col in range(3):
            if board[0][col] is not None and board[0][col] == board[1][col] and board[1][col] == board[2][col]:
                if set_winner:
                    self.winner = board[0][col]
                    self.win_filed[0][col] = True
                    self.win_filed[1][col] = True
                    self.win_filed[2][col] = True
                return board[0][col]

        return False

    def board_full(self):
        return not (any([self.board[r][c] is None for r in range(3) for c in range(3)]))

    def choose_random(self):
        row, column = choice(self.empty_indexes())

        self.board[row][column] = "pc"
        return

    def empty_indexes(self):
        indexes = []
        for r, row in enumerate(self.board):
            for c, field in enumerate(row):
                if field is None:
                    indexes.append((r, c))

        return indexes

    def minimax(self, board, depth, isMaximizing):
        player, pc = "user", "pc"
        win = self.is_finished(board, set_winner=False)
        if win == pc:
            return 10
        elif win == player:
            return -10
        elif self.board_full():
            return 0

        if isMaximizing:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = pc
                        best = max(best, self.minimax(board,
                                                 depth + 1,
                                                 not isMaximizing))
                        board[i][j] = None
            return best

        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = player
                        best = min(best, self.minimax(board, depth + 1, not isMaximizing))
                        board[i][j] = None
            return best

    def ai_move(self):
        board = self.board.copy()
        player, pc = "user", "pc"
        bestVal = -1000
        bestMove = (-1, -1)

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = pc
                    moveVal = self.minimax(board, 0, False)
                    board[i][j] = None
                    if (moveVal > bestVal):
                        bestMove = (i, j)
                        bestVal = moveVal

        self.board[bestMove[0]][bestMove[1]] = "pc"

async def start_game(interaction: nextcord.Interaction):
    game = Game(int(interaction.data['values'][0]), interaction.user)
    view = game.prepare_view()

    await interaction.response.edit_message(
        content=f"Ruch gracza {interaction.user.mention}:", view=view)

