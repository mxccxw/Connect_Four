import random


class Board:
    """A data type representing a Connect-4 board
    with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[" "] * width for row in range(height)]

        # We hoeven niets terug te geven vanuit een constructor!

    def __repr__(self):
        """This method returns a string representation
        for an object of type Board.
        """
        s = ""  # de string om terug te geven
        for row in range(0, self.height):
            s += "|"
            for col in range(0, self.width):
                s += self.data[row][col] + "|"
            s += "\n"

        s += (2 * self.width + 1) * "-"  # onderkant van het bord

        # hier moeten de nummers nog onder gezet worden
        s += "\n"
        for i in range(self.width):
            s += " " + str(i % 10)

        return s  # het bord is compleet, geef het terug

    def add_move(self, col, ox):
        """Adds a stone for player ox to column col"""
        i = 0
        while i < self.height and self.data[i][col] == " ":
            i += 1
        self.data[i - 1][col] = ox

    def clear(self):
        """Clears the board"""
        self.data = [[" "] * self.width for _ in range(self.height)]

    def set_board(self, move_string):
        """Accepts a string of columns and places
        alternating checkers in those columns,
        starting with 'X'.

        For example, call b.set_board('012345')
        to see 'X's and 'O's alternate on the
        bottom row, or b.set_board('000000') to
        see them alternate in the left column.

        move_string must be a string of one-digit integers.
        """
        next_checker = "X"  # we starten door een 'X' te spelen
        for col_char in move_string:
            col = int(col_char)
            if 0 <= col <= self.width:
                self.add_move(col, next_checker)
            if next_checker == "X":
                next_checker = "O"
            else:
                next_checker = "X"

    def allows_move(self, col):
        """Checks whether column col can be played"""
        return 0 <= col < self.width and self.data[0][col] == " "

    def is_full(self):
        """Checks whether the board is full"""
        for col in range(self.width):
            if self.allows_move(col):
                return False
        return True

    def del_move(self, col):
        """Removes a stone from column col"""
        i = 0
        while i < self.height and self.data[i][col] == " ":
            i += 1
        if i < self.height:
            self.data[i][col] = " "

    def wins_for(self, ox):
        """Checks whether player ox wins the game"""
        for y in range(self.height):
            for x in range(self.width):
                if (
                    in_a_row_n_east(ox, y, x, self.data, 4)
                    or in_a_row_n_south(ox, y, x, self.data, 4)
                    or in_a_row_n_southeast(ox, y, x, self.data, 4)
                    or in_a_row_n_northeast(ox, y, x, self.data, 4)
                ):
                    return True
        return False

    def host_game(self):
        """Plays a game of Connect Four"""
        ox = "O"
        while True:
            # druk het bord af
            print(self)

            # controleer of het spel afgelopen is
            if self.wins_for(ox):
                print(ox, "heeft gewonnen!")
                break
            elif self.is_full():
                print("Gelijkspel!")
                break

            # verander de huidige speler
            if ox == "O":
                ox = "X"
            else:
                ox = "O"

            # laat de speler een kolom kiezen
            col = -1
            while not self.allows_move(col):
                col = int(input("Kolom voor " + ox + ": "))

            # voer de zet uit
            self.add_move(col, ox)

    def play_game(self, px, po, show_scores=False):
        """
        Plays a game of Connect Four between players px and po.
        If show_scores is True, the player's board evaluations are printed each turn.
        """
        ox = "O"
        while True:
            # druk het bord af
            print(self)

            # controleer of het spel afgelopen is
            if self.wins_for(ox):
                print(f"{ox} heeft gewonnen!")
                break
            elif self.is_full():
                print("Gelijkspel!")
                break

            # verander de huidige speler
            if ox == "O":
                ox = "X"
                player = px
            else:
                ox = "O"
                player = po

            if player == "human":
                # laat de menselijke speler een kolom kiezen
                col = -1
                while not self.allows_move(col):
                    col = int(input("Kolom voor " + ox + ": "))
            else:
                # de computerspeler berekent een zet
                if show_scores:
                    scores = player.scores_for(self)
                    print("Scores voor ", ox, ":", [int(sc) for sc in scores])
                    col = player.tiebreak_move(scores)
                else:
                    col = player.next_move(self)

            # voer de zet uit
            self.add_move(col, ox)


def in_a_row_n_east(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going east"""
    if r_start < 0 or r_start >= len(a) or c_start < 0 or c_start >= len(a[0]) - n + 1:
        return False
    for i in range(0, n):
        if a[r_start][c_start + i] != ch:
            return False
    return True


def in_a_row_n_south(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going south"""
    if r_start < 0 or r_start >= len(a) - n + 1 or c_start < 0 or c_start >= len(a[0]):
        return False
    for i in range(0, n):
        if a[r_start + i][c_start] != ch:
            return False
    return True


def in_a_row_n_southeast(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going southeast"""
    if (
        r_start < 0
        or r_start >= len(a) - n + 1
        or c_start < 0
        or c_start >= len(a[0]) - n + 1
    ):
        return False
    for i in range(0, n):
        if a[r_start + i][c_start + i] != ch:
            return False
    return True


def in_a_row_n_northeast(ch, r_start, c_start, a, n):
    """Checks whether ch has n in a row starting at r_start, c_start going northeast"""
    if (
        r_start < n - 1
        or r_start >= len(a)
        or c_start < 0
        or c_start >= len(a[0]) - n + 1
    ):
        return False
    for i in range(0, n):
        if a[r_start - i][c_start + i] != ch:
            return False
    return True


class Player:
        """Een AI-speler voor Connect Four."""
        
        def __init__(self, ox, tbt, ply):
            """Creëert een speler voor een gegeven checker, tie-breaking type, en ply.
            """
            self.ox = ox
            self.tbt = tbt
            self.ply = ply
        
        def __repr__(self):
            """Maakt een string representatie van de speler.
            """
            s = "Player: ox = " + self.ox + ", "
            s += "tbt = " + self.tbt + ", "
            s += "ply = " + str(self.ply)
            return s
        
        def opp_ch(self):
            """Geeft de steen van de tegenstander terug. 
            De steen die de tegenstander zal gebruiken.
            """
            if self.ox == 'X':
                return 'O'
            else:
                return 'X'
        
        def score_board(self, b):
            """Geeft een enkele float-waarde van de invoer b. 
            b is een object van het type bord.
            """
            if b.wins_for(self.ox):
                return 100.0
            elif b.wins_for(self.opp_ch()):
                return 0.0
            else:
                return 50.0
        
        def tiebreak_move(self, scores):
            """Accepteert een reeks scores, een niet-lege lijst met komma getallen. 
            De hoogste score in de kolom van de opgegeven strategie wordt teruggegeven (LINKS/RECHTS). 
            Bij de RANDOM strategie wordt een willekeurige hoogste score kolom teruggegeven.
            """
            index = 0
            max_score = 0
            # Maakt een lijst met indexen.
            max_indices = []
            for i, score in enumerate(scores):
                # Geeft de kolom terug met de hoogste score.
                if score > max_score:
                    index = i
                    max_score = score
                    if self.tbt == 'RANDOM':
                        max_indices = [index]
                # Geeft de kolom terug met de hoogste score aan de hand van de keuze strategie van de speler. 
                elif score == max_score:
                    if self.tbt == 'RIGHT':
                        index = i
                        max_score = score
                    elif self.tbt == 'RANDOM':
                        max_indices.append(i)
            # Geeft een willekeurige kolom met de hoogste score terug.
            if self.tbt == 'RANDOM':
                index = random.choice(max_indices)
            return index
        
        def scores_for(self, b):
            """Geeft een lijst met scores. 
            In deze lijst geeft de score-index c aan hoe "goed" het bord is nadat de speler een stuk in kolom c heeft gespeeld. 
            Deze "goedheid" wordt berekend met wat er gebeurt na zelf gespeeld te hebben.
            """
            # Maakt een lijst waarbij elk element de waarde 50 heeft en lengte gelijk is aan het bord
            scores = [50.0] * b.width
            
            # Basisgeval 1: Als de ply van het object 0 is, wordt er geen zet gedaaan.
            if self.ply == 0:
                return scores
            
            # Lust over alle kolommen.
            for x, score in enumerate(scores):
                # Basisgeval 2: Als self al heeft gewonnen geef kolom waarde (100.0).
                if b.wins_for(self.ox):
                    scores[x] = 100.0
                # Basisgeval 3: Als self.opp_ch heeft gewonnen geef kolom waarde (0.0).
                elif b.wins_for(self.opp_ch()):
                    scores[x] = 0.0
                
                if b.allows_move(x):
                    # Maakt een tegenstander.
                    b.add_move(x, self.ox)
                    if b.wins_for(self.ox):
                        scores[x] = 100.0
                    elif b.wins_for(self.opp_ch()):
                        scores[x] = 0.0
                    else:
                        # Berekent de score van op en zet het in de huidige kolom.
                        op = Player(self.opp_ch(), self.tbt, self.ply - 1)
                        opp_scores = max(op.scores_for(b))
                        scores[x] = 100.0 - opp_scores
                    
                    # Verwijderd de steen die gezet was om de kolom te evalueren.
                    b.del_move(x)
                
                elif b.is_full():
                    scores[x] = 50.0
                else:
                    scores[x] = -1.0
            return scores
        
        def next_move(self, b):
            """Accepteert argument b, een object van het type Bord. 
            Bepaalt de best mogelijke zet van de huidige bordstatus en geeft deze terug.
            """
            scores = self.scores_for(b)
            best_move = self.tiebreak_move(scores)
            return best_move


# TESTS: __repr__(self)            
p = Player('X', 'LEFT', 2)
assert repr(p) == 'Player: ox = X, tbt = LEFT, ply = 2'
p = Player('O', 'RANDOM', 0)
assert repr(p) == 'Player: ox = O, tbt = RANDOM, ply = 0'

# TESTS: opp_ch(self)
p = Player('X', 'LEFT', 3)
assert p.opp_ch() == 'O'
assert Player('O', 'LEFT', 0).opp_ch() == 'X'

# TESTS: score_board(self, b)
b = Board(7, 6)
b.set_board('01020305')
p = Player('X', 'LEFT', 0)
assert p.score_board(b) == 100.0
assert Player('O', 'LEFT', 0).score_board(b) == 0.0
assert Player('O', 'LEFT', 0).score_board(Board(7, 6)) == 50.0

# TESTS: tiebreak_move(self, scores)
scores = [0, 0, 50, 0, 50, 50, 0]
p = Player('X', 'LEFT', 1)
p2 = Player('X', 'RIGHT', 1)
assert p.tiebreak_move(scores) == 2
assert p2.tiebreak_move(scores) == 5

# TESTS: scores_for(self, b)
b = Board(7, 6)
b.set_board('1211244445')
assert Player('X', 'LEFT', 0).scores_for(b) == [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0]
assert Player('O', 'LEFT', 1).scores_for(b) == [50.0, 50.0, 50.0, 100.0, 50.0, 50.0, 50.0]
assert Player('X', 'LEFT', 2).scores_for(b) == [0.0, 0.0, 0.0, 50.0, 0.0, 0.0, 0.0]
assert Player('X', 'LEFT', 3).scores_for(b) == [0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0]
assert Player('O', 'LEFT', 3).scores_for(b) == [50.0, 50.0, 50.0, 100.0, 50.0, 50.0, 50.0]
assert Player('O', 'LEFT', 4).scores_for(b) == [0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0]

# TEST: next_move(self, b)
b = Board(7, 6)
b.set_board('1211244445')
assert Player('X', 'LEFT', 1).next_move(b) == 0
assert Player('X', 'RIGHT', 1).next_move(b) == 6
assert Player('X', 'LEFT', 2).next_move(b) == 3
assert Player('X', 'RIGHT', 2).next_move(b) == 3
assert Player('X', 'RANDOM', 2).next_move(b) == 3

# PLAY GAME: Computer vs. Computer
b = Board(7,6)
computer = Player('O', 'RANDOM', 4)
computer2 = Player('X', 'RANDOM', 4)
b.play_game(computer2, computer, True)