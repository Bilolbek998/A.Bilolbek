import tkinter as tk
from tkinter import messagebox
import math
import random

# ── Ranglar ──────────────────────────────────────────────
BG       = "#1E1E2E"
PANEL    = "#2A2A3E"
CELL_BG  = "#2E2E42"
CELL_HOV = "#383850"
X_COLOR  = "#7EB8F7"
O_COLOR  = "#F4886C"
WIN_CLR  = "#A6E3A1"
TEXT_PRI = "#CDD6F4"
TEXT_SEC = "#6C7086"
ACCENT   = "#CBA6F7"
BTN_BG   = "#313244"
BTN_HOV  = "#45475A"

WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

# ── Minimax + Alpha-Beta ──────────────────────────────────
def check_winner(board, p):
    return any(board[a]==p and board[b]==p and board[c]==p for a,b,c in WINS)

def get_win_line(board, p):
    for line in WINS:
        if all(board[i]==p for i in line):
            return line
    return None

def is_draw(board):
    return all(c is not None for c in board)

def minimax(board, is_max, alpha, beta, depth):
    if check_winner(board, 'O'): return 10 - depth
    if check_winner(board, 'X'): return depth - 10
    if is_draw(board): return 0
    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] is None:
                board[i] = 'O'
                best = max(best, minimax(board, False, alpha, beta, depth+1))
                board[i] = None
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] is None:
                board[i] = 'X'
                best = min(best, minimax(board, True, alpha, beta, depth+1))
                board[i] = None
                beta = min(beta, best)
                if beta <= alpha: break
        return best

def best_ai_move(board, difficulty):
    empty = [i for i in range(9) if board[i] is None]
    if not empty: return None
    if difficulty == 'Oson':
        return random.choice(empty)
    if difficulty == "O'rta" and random.random() < 0.45:
        return random.choice(empty)
    best_s, best_i = -math.inf, empty[0]
    for i in empty:
        board[i] = 'O'
        s = minimax(board, False, -math.inf, math.inf, 0)
        board[i] = None
        if s > best_s: best_s, best_i = s, i
    return best_i

# ── Asosiy ilova ─────────────────────────────────────────
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe — Minimax AI")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.board      = [None]*9
        self.game_over  = False
        self.current    = 'X'
        self.difficulty = tk.StringVar(value='Qiyin')
        self.first_move = tk.StringVar(value='Siz (X)')
        self.two_player = False
        self.scores     = {'X':0,'O':0,'D':0}

        self._build_ui()
        self._new_game()

    # ── UI qurilishi ──────────────────────────────────────
    def _build_ui(self):
        # Sarlavha
        tk.Label(self.root, text="Tic Tac Toe", font=("Helvetica",22,"bold"),
                 bg=BG, fg=ACCENT).pack(pady=(20,4))
        tk.Label(self.root, text="Minimax AI bilan o'ynang",
                 font=("Helvetica",11), bg=BG, fg=TEXT_SEC).pack(pady=(0,16))

        # Hisoblar paneli
        score_frame = tk.Frame(self.root, bg=PANEL, padx=20, pady=10)
        score_frame.pack(padx=24, fill='x')

        for col, (label, key, color) in enumerate([
            ("Siz (X)", 'X', X_COLOR),
            ("Durrang", 'D', TEXT_SEC),
            ("AI (O)",  'O', O_COLOR),
        ]):
            f = tk.Frame(score_frame, bg=PANEL)
            f.grid(row=0, column=col, padx=20)
            tk.Label(f, text=label, font=("Helvetica",10), bg=PANEL, fg=TEXT_SEC).pack()
            lbl = tk.Label(f, text="0", font=("Helvetica",28,"bold"), bg=PANEL, fg=color)
            lbl.pack()
            setattr(self, f'score_{key}', lbl)

        score_frame.columnconfigure((0,1,2), weight=1)

        # Status
        self.status_var = tk.StringVar(value="Tayyor")
        self.status_lbl = tk.Label(self.root, textvariable=self.status_var,
                                   font=("Helvetica",13,"bold"),
                                   bg=BG, fg=TEXT_PRI, pady=10)
        self.status_lbl.pack()

        # O'yin taxtasi
        board_frame = tk.Frame(self.root, bg=BG)
        board_frame.pack(padx=24, pady=4)

        self.cells = []
        for i in range(9):
            btn = tk.Button(board_frame, text="", font=("Helvetica",34,"bold"),
                            width=3, height=1,
                            bg=CELL_BG, fg=TEXT_PRI,
                            activebackground=CELL_HOV,
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=lambda idx=i: self._on_click(idx))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, ipadx=10, ipady=10)
            self.cells.append(btn)

        # Sozlamalar
        settings = tk.Frame(self.root, bg=BG)
        settings.pack(padx=24, pady=(10,0), fill='x')

        # Qiyinlik
        tk.Label(settings, text="Qiyinlik:", font=("Helvetica",10),
                 bg=BG, fg=TEXT_SEC).grid(row=0, column=0, sticky='w', pady=4)
        diff_frame = tk.Frame(settings, bg=BG)
        diff_frame.grid(row=0, column=1, sticky='w', padx=(8,0))
        self.diff_btns = {}
        for d in ['Oson', "O'rta", 'Qiyin', '2 Kishi']:
            b = tk.Button(diff_frame, text=d, font=("Helvetica",10),
                          bg=BTN_BG, fg=TEXT_PRI, relief='flat', bd=0,
                          padx=10, pady=4, cursor='hand2',
                          command=lambda x=d: self._set_diff(x))
            b.pack(side='left', padx=3)
            self.diff_btns[d] = b

        # Birinchi hamla
        self.first_row = tk.Frame(settings, bg=BG)
        self.first_row.grid(row=1, column=0, columnspan=2, sticky='w', pady=4)
        tk.Label(self.first_row, text="Birinchi hamla:", font=("Helvetica",10),
                 bg=BG, fg=TEXT_SEC).pack(side='left')
        self.fm_btns = {}
        for opt in ['Siz (X)', 'AI (O)']:
            b = tk.Button(self.first_row, text=opt, font=("Helvetica",10),
                          bg=BTN_BG, fg=TEXT_PRI, relief='flat', bd=0,
                          padx=10, pady=4, cursor='hand2',
                          command=lambda x=opt: self._set_first(x))
            b.pack(side='left', padx=(8,3))
            self.fm_btns[opt] = b

        # Tugmalar
        btn_row = tk.Frame(self.root, bg=BG)
        btn_row.pack(pady=16)
        tk.Button(btn_row, text="Qaytadan boshlash ↺",
                  font=("Helvetica",11,"bold"),
                  bg=ACCENT, fg="#1E1E2E",
                  relief='flat', bd=0, padx=20, pady=8,
                  cursor='hand2',
                  command=self._new_game).pack(side='left', padx=6)
        tk.Button(btn_row, text="Hisobni tozalash",
                  font=("Helvetica",11),
                  bg=BTN_BG, fg=TEXT_PRI,
                  relief='flat', bd=0, padx=16, pady=8,
                  cursor='hand2',
                  command=self._reset_scores).pack(side='left', padx=6)

        # Boshlang'ich holat
        self._set_diff('Qiyin')
        self._set_first('Siz (X)')

    def _set_diff(self, d):
        self.difficulty.set(d)
        self.two_player = (d == '2 Kishi')
        for k, b in self.diff_btns.items():
            b.config(bg=ACCENT if k==d else BTN_BG,
                     fg="#1E1E2E" if k==d else TEXT_PRI)
        if self.two_player:
            self.first_row.grid_remove()
        else:
            self.first_row.grid()
        self._new_game()

    def _set_first(self, opt):
        self.first_move.set(opt)
        for k, b in self.fm_btns.items():
            b.config(bg=ACCENT if k==opt else BTN_BG,
                     fg="#1E1E2E" if k==opt else TEXT_PRI)
        self._new_game()

    # ── O'yin logikasi ────────────────────────────────────
    def _new_game(self):
        self.board = [None]*9
        self.game_over = False
        self.current = 'X'
        for btn in self.cells:
            btn.config(text="", bg=CELL_BG, fg=TEXT_PRI, state='normal')
        if self.two_player:
            self._set_status("X ning navbati", X_COLOR)
        elif self.first_move.get() == 'AI (O)':
            self._set_status("AI o'ylayapti...", O_COLOR)
            self.root.after(500, self._ai_turn)
        else:
            self._set_status("Sizning navbatingiz (X)", X_COLOR)

    def _set_status(self, msg, color=TEXT_PRI):
        self.status_var.set(msg)
        self.status_lbl.config(fg=color)

    def _on_click(self, idx):
        if self.game_over or self.board[idx] is not None:
            return
        if not self.two_player and self.current == 'O':
            return
        self._place(idx, self.current)

        if not self.game_over:
            if self.two_player:
                self.current = 'O' if self.current=='X' else 'X'
                color = O_COLOR if self.current=='O' else X_COLOR
                self._set_status(f"{self.current} ning navbati", color)
            else:
                self.current = 'O'
                self._set_status("AI o'ylayapti...", O_COLOR)
                self.root.after(400, self._ai_turn)

    def _ai_turn(self):
        if self.game_over: return
        idx = best_ai_move(self.board, self.difficulty.get())
        if idx is not None:
            self._place(idx, 'O')
        if not self.game_over:
            self.current = 'X'
            self._set_status("Sizning navbatingiz (X)", X_COLOR)

    def _place(self, idx, player):
        self.board[idx] = player
        color = X_COLOR if player=='X' else O_COLOR
        self.cells[idx].config(text=player, fg=color, state='disabled',
                                disabledforeground=color)

        win_line = get_win_line(self.board, player)
        if win_line:
            self.game_over = True
            for i in win_line:
                self.cells[i].config(bg=WIN_CLR, fg="#1E1E2E",
                                     disabledforeground="#1E1E2E")
            if self.two_player:
                self._set_status(f"🎉 {player} yutdi!", WIN_CLR)
            elif player=='X':
                self._set_status("🎉 Siz yutdingiz!", WIN_CLR)
            else:
                self._set_status("🤖 AI yutdi!", O_COLOR)
            self.scores[player] += 1
            self._update_scores()
        elif is_draw(self.board):
            self.game_over = True
            self._set_status("🤝 Durrang!", TEXT_SEC)
            self.scores['D'] += 1
            self._update_scores()

    def _update_scores(self):
        self.score_X.config(text=str(self.scores['X']))
        self.score_O.config(text=str(self.scores['O']))
        self.score_D.config(text=str(self.scores['D']))

    def _reset_scores(self):
        self.scores = {'X':0,'O':0,'D':0}
        self._update_scores()
        self._new_game()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
