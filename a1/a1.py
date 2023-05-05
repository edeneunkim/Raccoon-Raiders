"""A1: Raccoon Raiders game objects (all tasks)

CSC148, Winter 2022

This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of this
code, whether as given or with any changes, are expressly prohibited.

Authors: Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver, and
Sophia Huynh.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver,
and Sophia Huynh.

=== Module Description ===
This module contains all of the classes necessary for a1_game.py to run.
"""

from __future__ import annotations

from random import shuffle
from typing import List, Tuple, Optional, Union

# Each raccoon moves every this many turns
RACCOON_TURN_FREQUENCY = 20

# Directions dx, dy
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [LEFT, UP, RIGHT, DOWN]


def get_shuffled_directions() -> List[Tuple[int, int]]:
    """
    Provided helper that returns a shuffled copy of DIRECTIONS.
    You should use this where appropriate
    """
    to_return = DIRECTIONS[:]
    shuffle(to_return)
    return to_return


class GameBoard:
    """A game board on which the game is played.

    === Public Attributes ===
    ended:
        whether this game has ended or not
    turns:
        how many turns have passed in the game
    width:
        the number of squares wide this board is
    height:
        the number of squares high this board is


    === Representation Invariants ===
    turns >= 0
    width > 0
    height > 0
    No tile in the game contains more than 1 character, except that a tile
    may contain both a Raccoon and an open GarbageCan.

    === Sample Usage ===
    See examples in individual method docstrings.
    """
    # === Private Attributes ===
    # _player: the player of the game
    # _c_garbage: a closed garbage bin
    # _o_garbage: an open garbage bin
    # _raccoon: a raccoon that moves randomly
    # _raccoon_in: a raccoon in a garbage bin
    # _smart: a smart raccoon that moves intelligently
    # _smart_in: a smart raccoon in a garbage bin
    # _recycling: a recycling bin
    # _list_of_char: a list of the characters in the game

    ended: bool
    turns: int
    width: int
    height: int
    _player: Optional[Player]
    _c_garbage: Optional[GarbageCan]
    _o_garbage: Optional[GarbageCan]
    _raccoon: Optional[Raccoon]
    _raccoon_in: Optional[Raccoon]
    _smart: Optional[SmartRaccoon]
    _smart_in: Optional[Raccoon]
    _recycling: Optional[RecyclingBin]
    _list_of_char: List[Union[Player, GarbageCan, Raccoon, RecyclingBin]]

    def __init__(self, w: int, h: int) -> None:
        """Initialize this Board to be of the given width <w> and height <h> in
        squares. A board is initially empty (no characters) and no turns have
        been taken.

        >>> b = GameBoard(3, 3)
        >>> b.width == 3
        True
        >>> b.height == 3
        True
        >>> b.turns == 0
        True
        >>> b.ended
        False
        """

        self.ended = False
        self.turns = 0

        self.width = w
        self.height = h

        self._player = None
        self._c_garbage = None
        self._o_garbage = None
        self._recycling = None
        self._raccoon = None
        self._smart = None
        self._raccoon_in = None
        self._smart_in = None
        self._list_of_char = []

    def place_character(self, c: Character) -> None:
        """Record that character <c> is on this board.

        This method should only be called from Character.__init__.

        The decisions you made about new private attributes for class GameBoard
        will determine what you do here.

        Preconditions:
        - c.board == self
        - Character <c> has not already been placed on this board.
        - The tile (c.x, c.y) does not already contain a character, with the
        exception being that a Raccoon can be placed on the same tile where
        an unlocked GarbageCan is already present.

        Note: The testing will depend on this method to set up the board,
        as the Character.__init__ method calls this method.

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)  # when a Raccoon is created, it is placed on b
        >>> b.at(1, 1)[0] == r  # requires GameBoard.at be implemented to work
        True
        """
        if isinstance(c, Player):
            self._player = c
        elif isinstance(c, SmartRaccoon):
            if c.inside_can:
                self._smart_in = c
            self._smart = c
        elif isinstance(c, Raccoon):
            if c.inside_can:
                self._raccoon_in = c
            self._raccoon = c
        elif isinstance(c, GarbageCan):
            if c.locked:
                self._c_garbage = c
            self._o_garbage = c
        elif isinstance(c, RecyclingBin):
            self._recycling = c
        self._list_of_char.append(c)

    def at(self, x: int, y: int) -> List[Character]:
        """Return the characters at tile (x, y).

        If there are no characters or if the (x, y) coordinates are not
        on the board, return an empty list.
        There may be as many as two characters at one tile,
        since a raccoon can climb into a garbage can.

        Note: The testing will depend on this method to allow us to
        access the Characters on your board, since we don't know how
        you have chosen to store them in your private attributes,
        so make sure it is working properly!

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)
        >>> b.at(1, 1)[0] == r
        True
        >>> p = Player(b, 0, 1)
        >>> b.at(0, 1)[0] == p
        True
        """
        char_at_tile = []
        for i in self._list_of_char:
            if i.x == x and i.y == y:
                char_at_tile.append(i)
        return char_at_tile

    def to_grid(self) -> List[List[chr]]:
        """
        Return the game state as a list of lists of chrs (letters) where:

        'R' = Raccoon
        'S' = SmartRaccoon
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        Each inner list represents one row of the game board.

        >>> b = GameBoard(3, 2)
        >>> _ = Player(b, 0, 0)
        >>> _ = Raccoon(b, 1, 1)
        >>> _ = GarbageCan(b, 2, 1, True)
        >>> b.to_grid()
        [['P', '-', '-'], ['-', 'R', 'C']]
        """
        grid_board = []
        for y in range(self.height):
            grid = []
            for x in range(self.width):
                if len(self.at(x, y)) <= 1 and not self.at(x, y):
                    grid.append('-')
                elif len(self.at(x, y)) <= 1 and self.at(x, y):
                    grid.append(self.char_type(x, y))
                else:
                    grid.append('@')
            grid_board.append(grid)
        return grid_board

    def char_type(self, x: int, y: int) -> str:
        """
        Return a symbol from the constants in the to_grid() docstring based on
        the type of the character at (x, y) of the board.

        >>> b = GameBoard(5, 5)
        >>> p = Player(b, 0, 0)
        >>> b.char_type(0, 0)
        'P'
        >>> r = Raccoon(b, 1, 1)
        >>> b.char_type(1, 1)
        'R'
        """
        character = ''
        if isinstance(self.at(x, y)[0], Player):
            character = self._player.get_char()
        elif isinstance(self.at(x, y)[0], SmartRaccoon):
            if self.at(x, y)[0].inside_can:
                character = '@'
            else:
                character = 'S'
        elif isinstance(self.at(x, y)[0], Raccoon):
            if self.at(x, y)[0].inside_can:
                character = '@'
            else:
                character = 'R'
        elif isinstance(self.at(x, y)[0], GarbageCan):
            if self.at(x, y)[0].locked:
                character = 'C'
            else:
                character = 'O'
        elif isinstance(self.at(x, y)[0], RecyclingBin):
            character = self._recycling.get_char()
        return character

    def __str__(self) -> str:
        """
        Return a string representation of this board.

        The format is the same as expected by the setup_from_grid method.

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 1)
        >>> print(b)
        ---
        -R-
        >>> _ = Player(b, 0, 0)
        >>> _ = GarbageCan(b, 2, 1, False)
        >>> print(b)
        P--
        -RO
        >>> str(b)
        'P--\\n-RO'
        """
        board = self.to_grid()
        board_str = ''
        for i in range(len(board)):
            for y in board[i]:
                board_str += y
            if i < len(board) - 1:
                board_str += '\n'
        return board_str

    def setup_from_grid(self, grid: str) -> None:
        """
        Set the state of this GameBoard to correspond to the string <grid>,
        which represents a game board using the following chars:

        'R' = Raccoon not in a GarbageCan
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        There is a newline character between each board row.

        >>> b = GameBoard(4, 4)
        >>> b.setup_from_grid('P-B-\\n-BRB\\n--BB\\n-C--')
        >>> str(b)
        'P-B-\\n-BRB\\n--BB\\n-C--'
        """
        lines = grid.split("\n")
        width = len(lines[0])
        height = len(lines)
        self.__init__(width, height)  # reset the board to an empty board
        y = 0
        for line in lines:
            x = 0
            for char in line:
                if char == 'R':
                    Raccoon(self, x, y)
                elif char == 'S':
                    SmartRaccoon(self, x, y)
                elif char == 'P':
                    Player(self, x, y)
                elif char == 'O':
                    GarbageCan(self, x, y, False)
                elif char == 'C':
                    GarbageCan(self, x, y, True)
                elif char == 'B':
                    RecyclingBin(self, x, y)
                elif char == '@':
                    GarbageCan(self, x, y, False)
                    Raccoon(self, x, y)  # always makes it a Raccoon
                    # Note: the order mattered above, as we have to place the
                    # Raccoon BEFORE the GarbageCan (see the place_character
                    # method precondition)
                x += 1
            y += 1

    # a helper method you may find useful in places
    def on_board(self, x: int, y: int) -> bool:
        """Return True iff the position x, y is within the boundaries of this
        board (based on its width and height), and False otherwise.
        """
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def give_turns(self) -> None:
        """Give every turn-taking character one turn in the game.

        The Player should take their turn first and the number of turns
        should be incremented by one. Then each other TurnTaker
        should be given a turn if RACCOON_TURN_FREQUENCY turns have occurred
        since the last time the TurnTakers were given their turn.

        After all turns are taken, check_game_end should be called to
        determine if the game is over.

        Precondition:
        self._player is not None

        >>> b = GameBoard(4, 3)
        >>> p = Player(b, 0, 0)
        >>> r = Raccoon(b, 1, 1)
        >>> b.turns
        0
        >>> for _ in range(RACCOON_TURN_FREQUENCY - 1):
        ...     b.give_turns()
        >>> b.turns == RACCOON_TURN_FREQUENCY - 1
        True
        >>> (r.x, r.y) == (1, 1)  # Raccoon hasn't had a turn yet
        True
        >>> (p.x, p.y) == (0, 0)  # Player hasn't had any inputs
        True
        >>> p.record_event(RIGHT)
        >>> b.give_turns()
        >>> (r.x, r.y) != (1, 1)  # Raccoon has had a turn!
        True
        >>> (p.x, p.y) == (1, 0)  # Player moved right!
        True
        """
        self._player.take_turn()
        self.turns += 1  # PROVIDED, DO NOT CHANGE

        if self.turns % RACCOON_TURN_FREQUENCY == 0:  # PROVIDED, DO NOT CHANGE
            for i in self._list_of_char:
                if isinstance(i, (Raccoon, SmartRaccoon)):
                    i.take_turn()

        self.check_game_end()  # PROVIDED, DO NOT CHANGE

    def handle_event(self, event: Tuple[int, int]) -> None:
        """Handle a user-input event.

        The board's Player records the event that happened, so that when the
        Player gets a turn, it can make the move that the user input indicated.
        """
        self._player.record_event(event)

    def check_game_end(self) -> Optional[int]:
        """Check if this game has ended. A game ends when all the raccoons on
        this game board are either inside a can or trapped.

        If the game has ended:
        - update the ended attribute to be True
        - Return the score, where the score is given by:
            (number of raccoons trapped) * 10 + the adjacent_bin_score
        If the game has not ended:
        - update the ended attribute to be False
        - return None

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 0)
        >>> _ = Player(b, 0, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> b.check_game_end() is None
        True
        >>> b.ended
        False
        >>> _ = RecyclingBin(b, 2, 0)
        >>> b.check_game_end()
        11
        >>> b.ended
        True
        """
        raccoons = 0
        trapped = 0
        inside = 0
        for i in self._list_of_char:
            if isinstance(i, Raccoon):
                raccoons += 1
                if i.check_trapped():
                    trapped += 1
                elif i.inside_can:
                    inside += 1
        if trapped + inside == raccoons:
            self.ended = True
            return trapped * 10 + self.adjacent_bin_score()
        else:
            return None

    def adjacent_bin_score(self) -> int:
        """
        Return the size of the largest cluster of adjacent recycling bins
        on this board.

        Two recycling bins are adjacent when they are directly beside each other
        in one of the four directions (up, down, left, right).

        See Task #5 in the handout for ideas if you aren't sure how
        to approach this problem.

        >>> b = GameBoard(3, 3)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> print(b)
        B--
        -B-
        --B
        >>> b.adjacent_bin_score()
        1
        >>> _ = RecyclingBin(b, 2, 1)
        >>> print(b)
        B--
        -BB
        --B
        >>> b.adjacent_bin_score()
        3
        >>> _ = RecyclingBin(b, 0, 1)
        >>> print(b)
        B--
        BBB
        --B
        >>> b.adjacent_bin_score()
        5
        """
        row = []
        col = []
        checked = []
        longest_chain = 1
        for y in range(len(self.to_grid())):
            for x in range(len(self.to_grid()[y])):
                if self.to_grid()[y][x] == 'B':
                    col.append(x)
                    row.append(y)
        for i in range(len(col)):
            beside = get_neighbours((col[i], row[i]))
            chain = self.check_adjacent(beside, checked)
            if chain[0] > longest_chain:
                longest_chain = chain[0] - 1
        return longest_chain

    def check_adjacent(self, beside: List[Tuple[int, int]],
                       checked: List[Tuple[int, int]])\
            -> Tuple[int, List[Tuple[int, int]]]:
        """Return a tuple containing the number of recycling bins at the
        coordinates in beside containing a recycling bin on a GameBoard
        and a list of recycling bins that have already been checked.

        NOTE: the minimum is always 1 since the point is a recycling bin itself.

        >>> b = GameBoard(3, 3)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> b.check_adjacent([(0, 0), (1, 1), (2, 2)], [])
        (4, [(0, 0), (1, 1), (2, 2)])
        """
        chain = 1
        for j in beside:
            if self.on_board(j[0], j[1]) and\
                    self.to_grid()[j[1]][j[0]] == 'B' and \
                    (j[0], j[1]) not in checked:
                chain += 1
                checked.append((j[0], j[1]))
                neighbours = get_neighbours((j[0], j[1]))
                chain += self.check_adjacent(neighbours, checked)[0] - 1
        return chain, checked


class Character:
    """A character that has (x,y) coordinates and is associated with a given
    board.

    This class is abstract and should not be directly instantiated.

    NOTE: To reduce the amount of documentation in subclasses, we have chosen
    not to repeat information about the public attributes in each subclass.
    Remember that the attributes are not inherited, but only exist once we call
    the __init__ of the parent class.

    === Public Attributes ===
    board:
        the game board that this Character is on
    x, y:
        the coordinates of this Character on the board

    === Representation Invariants ===
    x, y are valid coordinates in board (i.e. board.on_board(x, y) is True)
    """
    board: GameBoard
    x: int
    y: int

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Character with board <b>, and
        at tile (<x>, <y>).

        When a Character is initialized, it is placed on board <b>
        by calling the board's place_character method. Refer to the
        preconditions of place_character, which must be satisfied.
        """
        self.board = b
        self.x, self.y = x, y
        self.board.place_character(self)  # this associates self with the board!

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Move this character to the tile

        (self.x + direction[0], self.y + direction[1]) if possible. Each child
        class defines its own version of what is possible.

        Return True if the move was successful and False otherwise.

        """
        raise NotImplementedError

    def get_char(self) -> chr:
        """
        Return a single character (letter) representing this Character.
        """
        raise NotImplementedError


class TurnTaker(Character):
    """
    A Character that can take a turn in the game.

    This class is abstract and should not be directly instantiated.
    """

    def take_turn(self) -> None:
        """
        Take a turn in the game. This method must be implemented in any subclass
        """
        raise NotImplementedError


class RecyclingBin(Character):
    """A recycling bin in the game.

    === Sample Usage ===
    >>> rb = RecyclingBin(GameBoard(4, 4), 2, 1)
    >>> rb.x, rb.y
    (2, 1)
    """

    def move(self, direction: Tuple[int, int]) -> bool:
        """Move this recycling bin to tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return whether or not this move was successful.

        If the new tile is occupied by another RecyclingBin, push
        that RecyclingBin one tile away in the same direction and take
        its tile (as described in the Assignment 1 handout).

        If the new tile is occupied by any other Character or if it
        is beyond the boundaries of the board, do nothing and return False.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> rb = RecyclingBin(b, 0, 0)
        >>> rb.move(UP)
        False
        >>> rb.move(DOWN)
        True
        >>> b.at(0, 1) == [rb]
        True
        """
        if direction == UP:
            return self._rec_move_up()
        elif direction == DOWN:
            return self._rec_move_down()
        elif direction == RIGHT:
            return self._rec_move_right()
        else:
            return self._rec_move_left()

    def _rec_move_up(self) -> bool:
        """
        Move the recycling bin up if the player or another recycling bin
        pushes it up and if it is possible to move up. Return True if it moves
        and False otherwise.

        >>> b = GameBoard(3, 3)
        >>> re = RecyclingBin(b, 1, 1)
        >>> re._rec_move_up()
        True
        >>> re._rec_move_up()
        False
        """
        if 0 <= self.y - 1:
            if self.board.to_grid()[self.y - 1][self.x] == 'B':
                obj = self.board.at(self.x, self.y - 1)[0]
                if obj.move(UP):
                    self.y -= 1
                    return True
                return False
            elif self.board.to_grid()[self.y - 1][self.x] != '-':
                return False
            self.y -= 1
            return True
        else:
            return False

    def _rec_move_down(self) -> bool:
        """
        Move the recycling bin down if the player or another recycling bin
        pushes it down and if it is possible to move down. Return True if it
        moves and False otherwise.

        >>> b = GameBoard(3, 3)
        >>> re = RecyclingBin(b, 1, 1)
        >>> re._rec_move_down()
        True
        >>> re._rec_move_down()
        False
        """
        if self.board.height > self.y + 1:
            if self.board.to_grid()[self.y + 1][self.x] == 'B':
                obj = self.board.at(self.x, self.y + 1)[0]
                if obj.move(DOWN):
                    self.y += 1
                    return True
                return False
            elif self.board.to_grid()[self.y + 1][self.x] != '-':
                return False
            self.y += 1
            return True
        else:
            return False

    def _rec_move_right(self) -> bool:
        """
        Move the recycling bin right if the player or another recycling bin
        pushes it right if and it is possible to move down. Return True if it
        moves and False otherwise.

        >>> b = GameBoard(3, 3)
        >>> re = RecyclingBin(b, 1, 1)
        >>> re._rec_move_right()
        True
        >>> re._rec_move_right()
        False
        """
        if self.board.width > self.x + 1:
            if self.board.to_grid()[self.y][self.x + 1] == 'B':
                obj = self.board.at(self.x + 1, self.y)[0]
                if obj.move(RIGHT):
                    self.x += 1
                    return True
                return False
            elif self.board.to_grid()[self.y][self.x + 1] != '-':
                return False
            self.x += 1
            return True
        else:
            return False

    def _rec_move_left(self) -> bool:
        """
        Move the recycling bin left if the player or another recycling bin
        pushes it left and if it is possible to move down. Return True if it
        moves and False otherwise.

        >>> b = GameBoard(3, 3)
        >>> re = RecyclingBin(b, 1, 1)
        >>> re._rec_move_left()
        True
        >>> re._rec_move_left()
        False
        """
        if 0 <= self.x - 1:
            if self.board.to_grid()[self.y][self.x - 1] == 'B':
                obj = self.board.at(self.x - 1, self.y)[0]
                if obj.move(LEFT):
                    self.x -= 1
                    return True
                return False
            elif self.board.to_grid()[self.y][self.x - 1] != '-':
                return False
            self.x -= 1
            return True
        else:
            return False

    def get_char(self) -> chr:
        """
        Return the character 'B' representing a RecyclingBin.
        """
        return 'B'


class Player(TurnTaker):
    """The Player of this game.

    === Sample Usage ===
    >>> b = GameBoard(3, 1)
    >>> p = Player(b, 0, 0)
    >>> p.record_event(RIGHT)
    >>> p.take_turn()
    >>> (p.x, p.y) == (1, 0)
    True
    >>> g = GarbageCan(b, 0, 0, False)
    >>> p.move(LEFT)
    True
    >>> g.locked
    True
    """
    # === Private Attributes ===
    # _last_event:
    #   The direction corresponding to the last keypress event that the user
    #   made, or None if there is currently no keypress event left to process
    _last_event: Optional[Tuple[int, int]]

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Player with board <b>,
        and at tile (<x>, <y>)."""

        TurnTaker.__init__(self, b, x, y)
        self._last_event = None

    def record_event(self, direction: Tuple[int, int]) -> None:
        """Record that <direction> is the last direction that the user
        has specified for this Player to move. Next time take_turn is called,
        this direction will be used.
        Precondition:
        direction is in DIRECTIONS
        """
        self._last_event = direction

    def take_turn(self) -> None:
        """Take a turn in the game.

        For a Player, this means responding to the last user input recorded
        by a call to record_event.
        """
        if self._last_event is not None:
            self.move(self._last_event)
            self._last_event = None

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Player to the tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return True if the move is successful.

        If the new tile is occupied by a Raccoon, a locked GarbageCan, or if it
        is beyond the boundaries of the board, do nothing and return False.

        If the new tile is occupied by a movable RecyclingBin, the player moves
        the RecyclingBin and moves to the new tile.

        If the new tile is unoccupied, the player moves to that tile.

        If a Player attempts to move towards an empty, unlocked GarbageCan, the
        GarbageCan becomes locked. The player's position remains unchanged in
        this case. Also return True in this case, as the Player has performed
        the action of locking the GarbageCan.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> p = Player(b, 0, 0)
        >>> p.move(UP)
        False
        >>> p.move(DOWN)
        True
        >>> b.at(0, 1) == [p]
        True
        >>> _ = RecyclingBin(b, 1, 1)
        >>> p.move(RIGHT)
        True
        >>> b.at(1, 1) == [p]
        True
        """
        if direction == UP:
            return self._move_up()
        elif direction == DOWN:
            return self._move_down()
        elif direction == RIGHT:
            return self._move_right()
        else:
            return self._move_left()

    def _move_up(self) -> bool:
        """
        Move the player up if there is nothing on its up besides a recycling
        bin. If there is a recycling bin, then move the player up only if
        it is possible for the recycling bin to move up too. If there is a
        garbage can, then the player closes the garbage can but does not move.
        Return True if the player moves or closes a garbage can and False
        otherwise.

        >>> b = GameBoard(3, 3)
        >>> p = Player(b, 1, 1)
        >>> p._move_up()
        True
        >>> p._move_up()
        False
        """
        if 0 <= self.y - 1:
            if self.board.to_grid()[self.y - 1][self.x] == 'O':
                self.board.at(self.x, self.y - 1)[0].locked = True
                return True
            elif self.board.to_grid()[self.y - 1][self.x] == 'B':
                obj = self.board.at(self.x, self.y - 1)[0]
                if obj.move(UP):
                    self.y -= 1
                    return True
                return False
            elif self.board.to_grid()[self.y - 1][self.x] != '-':
                return False
            self.y -= 1
            return True
        else:
            return False

    def _move_down(self) -> bool:
        """
        Move the player down if there is nothing on its left besides a recycling
        bin. If there is a recycling bin, then move the player down only if
        it is possible for the recycling bin to move down too. If there is a
        garbage can, then the player closes the garbage can but does not move.
        Return True if the player moves or closes a garbage can and False
        otherwise.

        >>> b = GameBoard(3, 3)
        >>> p = Player(b, 1, 1)
        >>> p._move_down()
        True
        >>> p._move_down()
        False
        """
        if self.board.height > self.y + 1:
            if self.board.to_grid()[self.y + 1][self.x] == 'O':
                self.board.at(self.x, self.y + 1)[0].locked = True
                return True
            elif self.board.to_grid()[self.y + 1][self.x] == 'B':
                obj = self.board.at(self.x, self.y + 1)[0]
                if obj.move(DOWN):
                    self.y += 1
                    return True
                return False
            elif self.board.to_grid()[self.y + 1][self.x] != '-':
                return False
            self.y += 1
            return True
        else:
            return False

    def _move_right(self) -> bool:
        """
        Move the player right if there is nothing on its right besides a
        recycling bin. If there is a recycling bin, then move the player left
        only if it is possible for the recycling bin to move right too. If there
        is agarbage can, then the player closes the garbage can but does not
        move. Return True if the player moves or closes a garbage can and False
        otherwise.

        >>> b = GameBoard(3, 3)
        >>> p = Player(b, 1, 1)
        >>> p._move_right()
        True
        >>> p._move_right()
        False
        """
        if self.board.width > self.x + 1:
            if self.board.to_grid()[self.y][self.x + 1] == 'O':
                self.board.at(self.x + 1, self.y)[0].locked = True
                return True
            elif self.board.to_grid()[self.y][self.x + 1] == 'B':
                obj = self.board.at(self.x + 1, self.y)[0]
                if obj.move(RIGHT):
                    self.x += 1
                    return True
                return False
            elif self.board.to_grid()[self.y][self.x + 1] != '-':
                return False
            self.x += 1
            return True
        else:
            return False

    def _move_left(self) -> bool:
        """
        Move the player left if there is nothing on its left besides a recycling
        bin. If there is a recycling bin, then move the player left only if
        it is possible for the recycling bin to move left too. If there is a
        garbage can, then the player closes the garbage can but does not move.
        Return True if the player moves or closes a garbage can and False
        otherwise.

        >>> b = GameBoard(3, 3)
        >>> p = Player(b, 1, 1)
        >>> p._move_left()
        True
        >>> p._move_left()
        False
        """
        if 0 <= self.x - 1:
            if self.board.to_grid()[self.y][self.x - 1] == 'O':
                self.board.at(self.x - 1, self.y)[0].locked = True
                return True
            elif self.board.to_grid()[self.y][self.x - 1] == 'B':
                obj = self.board.at(self.x - 1, self.y)[0]
                if obj.move(LEFT):
                    self.x -= 1
                    return True
                return False
            elif self.board.to_grid()[self.y][self.x - 1] != '-':
                return False
            self.x -= 1
            return True
        else:
            return False

    def get_char(self) -> chr:
        """
        Return the character 'P' representing this Player.
        """
        return 'P'


class Raccoon(TurnTaker):
    """A raccoon in the game.

    === Public Attributes ===
    inside_can:
        whether or not this Raccoon is inside a garbage can

    === Representation Invariants ===
    inside_can is True iff this Raccoon is on the same tile as an open
    GarbageCan.

    === Sample Usage ===
    >>> r = Raccoon(GameBoard(11, 11), 5, 10)
    >>> r.x, r.y
    (5, 10)
    >>> r.inside_can
    False
    """
    inside_can: bool

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Raccoon with board <b>, and
        at tile (<x>, <y>). Initially a Raccoon is not inside
        of a GarbageCan, unless it is placed directly inside an open GarbageCan.

        >>> r = Raccoon(GameBoard(5, 5), 5, 10)
        """
        self.inside_can = False
        # since this raccoon may be placed inside an open garbage can,
        # we need to initially set the inside_can attribute
        # BEFORE calling the parent init, which is where the raccoon is actually
        # placed on the board.
        TurnTaker.__init__(self, b, x, y)

    def check_trapped(self) -> bool:
        """Return True iff this raccoon is trapped. A trapped raccoon is
        surrounded on 4 sides (diagonals don't matter) by recycling bins, other
        raccoons (including ones in garbage cans), the player, and/or board
        edges. Essentially, a raccoon is trapped when it has nowhere it could
        move.

        Reminder: A racooon cannot move diagonally.

        >>> b = GameBoard(3, 3)
        >>> r = Raccoon(b, 2, 1)
        >>> _ = Raccoon(b, 2, 2)
        >>> _ = Player(b, 2, 0)
        >>> r.check_trapped()
        False
        >>> _ = RecyclingBin(b, 1, 1)
        >>> r.check_trapped()
        True
        """
        neighbours = []
        trapped = 0
        if self.inside_can:
            return False
        for i in get_neighbours((self.x, self.y)):
            if self.board.on_board(i[0], i[1]):
                neighbours.append(self.board.to_grid()[i[1]][i[0]])
            else:
                trapped += 1
        for i in neighbours:
            if i in 'OC-':
                return False
            trapped += 1
        return trapped == len(get_neighbours((self.x, self.y)))

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Raccoon in <direction> and return whether
        or not this was successful.

        If the tile one tile over in that direction is occupied by the Player,
        a RecyclingBin, or another Raccoon, OR if the tile is not within the
        boundaries of the board, do nothing and return False.

        If the tile is occupied by an unlocked GarbageCan that has no Raccoon
        in it, this Raccoon moves there and we have two characters on one tile
        (the GarbageCan and the Raccoon). If the GarbageCan is locked, this
        Raccoon uses this turn to unlock it and return True.

        If a Raccoon is inside of a GarbageCan, it will not move. Do nothing and
        return False.

        Return True if the Raccoon unlocks a GarbageCan or moves from its
        current tile.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> r = Raccoon(b, 0, 0)
        >>> r.move(UP)
        False
        >>> r.move(DOWN)
        True
        >>> b.at(0, 1) == [r]
        True
        >>> g = GarbageCan(b, 1, 1, True)
        >>> r.move(RIGHT)
        True
        >>> r.x, r.y  # Raccoon didn't change its position
        (0, 1)
        >>> not g.locked  # Raccoon unlocked the garbage can!
        True
        >>> r.move(RIGHT)
        True
        >>> r.inside_can
        True
        >>> len(b.at(1, 1)) == 2  # Raccoon and GarbageCan are both at (1, 1)!
        True
        """
        if self.check_trapped():
            return False
        else:
            if direction == UP:
                return self._rac_move_up()
            elif direction == DOWN:
                return self._rac_move_down()
            elif direction == RIGHT:
                return self._rac_move_right()
            else:
                return self._rac_move_left()

    def _rac_move_up(self) -> bool:
        """
        Move the raccoon up if there is nothing or an open garbage can on its
        up. If there is a closed garbage can, then the raccoon opens the
        garbage can. Return True if the raccoon moves or opens a garbage can and
        False otherwise.

        >>> b = GameBoard(3, 3)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1._rac_move_up()
        False
        >>> r2 = Raccoon(b, 2, 2)
        >>> r2._rac_move_up()
        True
        """
        if self.y - 1 < 0:
            return False
        tile = self.board.to_grid()[self.y - 1][self.x]
        if tile in 'O-':
            if tile == 'O':
                self.inside_can = True
            self.y -= 1
            return True
        elif tile == 'C':
            self.board.at(self.x, self.y - 1)[0].locked = False
            return True
        else:
            return False

    def _rac_move_down(self) -> bool:
        """
        Move the raccoon down if there is nothing or an open garbage can on its
        down. If there is a closed garbage can, then the raccoon opens the
        garbage can. Return True if the raccoon moves or opens a garbage can and
        False otherwise.

        >>> b = GameBoard(3, 3)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1._rac_move_down()
        True
        >>> r2 = Raccoon(b, 2, 2)
        >>> r2._rac_move_down()
        False
        """
        if self.y + 1 >= self.board.height:
            return False
        tile = self.board.to_grid()[self.y + 1][self.x]
        if tile in 'O-':
            if tile == 'O':
                self.inside_can = True
            self.y += 1
            return True
        elif tile == 'C':
            self.board.at(self.x, self.y + 1)[0].locked = False
            return True
        else:
            return False

    def _rac_move_right(self) -> bool:
        """
        Move the raccoon right if there is nothing or an open garbage can on its
        right. If there is a closed garbage can, then the raccoon opens the
        garbage can. Return True if the raccoon moves or opens a garbage can and
        False otherwise.

        >>> b = GameBoard(3, 3)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1._rac_move_right()
        True
        >>> r2 = Raccoon(b, 2, 2)
        >>> r2._rac_move_right()
        False
        """
        if self.x + 1 >= self.board.width:
            return False
        tile = self.board.to_grid()[self.y][self.x + 1]
        if tile in 'O-':
            if tile == 'O':
                self.inside_can = True
            self.x += 1
            return True
        elif tile == 'C':
            self.board.at(self.x + 1, self.y)[0].locked = False
            return True
        else:
            return False

    def _rac_move_left(self) -> bool:
        """
        Move the raccoon left if there is nothing or an open garbage can on its
        left. If there is a closed garbage can, then the raccoon opens the
        garbage can. Return True if the raccoon moves or opens a garbage can and
        False otherwise.

        >>> b = GameBoard(3, 3)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1._rac_move_left()
        False
        >>> r2 = Raccoon(b, 2, 2)
        >>> r2._rac_move_left()
        True
        """
        if self.x - 1 < 0:
            return False
        tile = self.board.to_grid()[self.y][self.x - 1]
        if tile in 'O-':
            if tile == 'O':
                self.inside_can = True
            self.x -= 1
            return True
        elif tile == 'C':
            self.board.at(self.x - 1, self.y)[0].locked = False
            return True
        else:
            return False

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a Raccoon is in a GarbageCan, it stays where it is.

        Otherwise, it randomly attempts (if it is not blocked) to move in
        one of the four directions, with equal probability.

        >>> b = GameBoard(3, 4)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1.take_turn()
        >>> (r1.x, r1.y) in [(0, 1), (1, 0)]
        True
        >>> r2 = Raccoon(b, 2, 1)
        >>> _ = RecyclingBin(b, 2, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> r2.take_turn()  # Raccoon is trapped
        >>> r2.x, r2.y
        (2, 1)
        """
        if not self.inside_can and not self.check_trapped():
            cannot_move = False
            direction = get_shuffled_directions()
            while not cannot_move:
                cannot_move = self._random_move(direction)
                direction = get_shuffled_directions()

    def _random_move(self, direction: List[Tuple[int, int]]) -> bool:
        """Return True if the raccoon can not move in any direction.

        >>> b = GameBoard(3, 3)
        >>> r = Raccoon(b, 0, 0)
        >>> p = Player(b, 0, 1)
        >>> _ = RecyclingBin(b, 1, 0)
        >>> r._random_move(DIRECTIONS)
        False
        """
        can_move = False
        directions = 0
        while not can_move:
            if direction[directions] == LEFT:
                if self._rac_move_left():
                    can_move = True
                    return True
                directions += 1
            elif direction[directions] == UP:
                if self._rac_move_up():
                    can_move = True
                    return True
                directions += 1
            elif direction[directions] == RIGHT:
                if self._rac_move_right():
                    can_move = True
                    return True
                directions += 1
            else:
                if self._rac_move_down():
                    can_move = True
                    return True
                directions += 1

    def get_char(self) -> chr:
        """
        Return '@' to represent that this Raccoon is inside a garbage can
        or 'R' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'R'


class SmartRaccoon(Raccoon):
    """A smart raccoon in the game.

    Behaves like a Raccoon, but when it takes a turn, it will move towards
    a GarbageCan if it can see that GarbageCan in its line of sight.
    See the take_turn method for details.

    SmartRaccoons move in the same way as Raccoons.

    === Sample Usage ===
    >>> b = GameBoard(8, 1)
    >>> s = SmartRaccoon(b, 4, 0)
    >>> s.x, s.y
    (4, 0)
    >>> s.inside_can
    False
    """

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a SmartRaccoon is in a GarbageCan, it stays where it is.

        A SmartRaccoon checks along the four directions for
        the closest non-occupied GarbageCan that has nothing blocking
        it from reaching that GarbageCan (except possibly the Player).

        If there is a tie for the closest GarbageCan, a SmartRaccoon
        will prioritize the directions in the order indicated in DIRECTIONS.

        If there are no GarbageCans in its line of sight along one of the four
        directions, it moves exactly like a Raccoon. A GarbageCan is in its
        line of sight if there are no other Raccoons, RecyclingBins, or other
        GarbageCans between this SmartRaccoon and the GarbageCan. The Player
        may be between this SmartRaccoon and the GarbageCan though.

        >>> b = GameBoard(8, 2)
        >>> s = SmartRaccoon(b, 4, 0)
        >>> _ = GarbageCan(b, 3, 1, False)
        >>> _ = GarbageCan(b, 0, 0, False)
        >>> _ = GarbageCan(b, 7, 0, False)
        >>> s.take_turn()
        >>> s.x == 5
        True
        >>> s.take_turn()
        >>> s.x == 6
        True
        """
        if not self.inside_can and not self.check_trapped():
            y = self._closest_y()
            x = self._closest_x()
            if x != 0 and y == 0 or x == 0 and y != 0:
                if y == 0:
                    self._move_x(x)
                elif x == 0:
                    self._move_y(y)
            elif x != 0 and y != 0:
                if y > x and self.x - x >= 0 and\
                        self.board.to_grid()[self.y][self.x - x] == 'O':
                    self.move(LEFT)
                elif x > y and self.y - y >= 0 and\
                        self.board.to_grid()[self.y - y][self.x] == 'O':
                    self.move(UP)
                elif y > x and self.x + x < self.board.width and \
                        self.board.to_grid()[self.y][self.x + x] == 'O':
                    self.move(RIGHT)
                elif x > y and self.y + y < self.board.height and \
                        self.board.to_grid()[self.y + y][self.x] == 'O':
                    self.move(DOWN)
            else:
                direction = get_shuffled_directions()
                self._random_move(direction)

    def _closest_x(self) -> int:
        """Return the number of spaces it takes to get to the closest garbage
        can in the x-axis. If an obstacle(s) is closer than the closest garbage
        can, then return 0.

        >>> b = GameBoard(3, 3)
        >>> s = SmartRaccoon(b, 2, 0)
        >>> g = GarbageCan(b, 0, 0, False)
        >>> s._closest_x()
        2
        """
        to_remove = []
        closest = []
        garbage_x = self._row()[0]
        obstacles_x = self._row()[1]
        for i in obstacles_x:
            for j in garbage_x:
                if j < self.x and self.x > i > j:
                    to_remove.append(j)
                elif j > self.x and j > i > self.x:
                    to_remove.append(j)
        for i in to_remove:
            if garbage_x and i in garbage_x:
                garbage_x.remove(i)
        for i in garbage_x:
            if garbage_x:
                closest.append(abs(self.x - i))
        if closest:
            return min(closest)
        return 0

    def _row(self) -> List[List[int]]:
        """Return a list of x-coordinates of garbage cans and obstacles in the
        same y-axis as self.

        >>> b = GameBoard(3, 3)
        >>> s = SmartRaccoon(b, 0, 0)
        >>> _ = GarbageCan(b, 2, 0, False)
        >>> s._row()
        [[2], []]
        """
        obstacles_x = []
        garbage_x = []
        same_row = self.board.to_grid()[self.y]
        for x in enumerate(same_row):
            if x[1] in 'OP-S':
                if x[1] == 'O':
                    garbage_x.append(x[0])
            else:
                obstacles_x.append(x[0])
        return [garbage_x, obstacles_x]

    def _closest_y(self) -> int:
        """Return the number of spaces it takes to get to the closest garbage
        can in the y-axis. If an obstacle(s) is closer than the closest garbage
        can, then return 0.

        >>> b = GameBoard(3, 3)
        >>> s = SmartRaccoon(b, 0, 2)
        >>> g = GarbageCan(b, 0, 0, False)
        >>> s._closest_y()
        2
        """
        to_remove = []
        closest = []
        garbage_y = self._col()[0]
        obstacles_y = self._col()[1]
        for i in obstacles_y:
            for j in garbage_y:
                if j < self.y and j < i < self.y:
                    to_remove.append(j)
                elif j > self.y and j > i > self.y:
                    to_remove.append(j)
        for i in to_remove:
            if garbage_y and i in garbage_y:
                garbage_y.remove(i)
        for i in garbage_y:
            if garbage_y:
                closest.append(abs(self.y - i))
        if closest:
            return min(closest)
        return 0

    def _col(self) -> List[List[int]]:
        """Return a list of y-coordinates of garbage cans and obstacles in the
        same x-axis as self.

        >>> b = GameBoard(3, 3)
        >>> s = SmartRaccoon(b, 0, 0)
        >>> _ = GarbageCan(b, 0, 2, False)
        >>> s._col()
        [[2], []]
        """
        obstacles_y = []
        garbage_y = []
        same_col = []
        for y in range(len(self.board.to_grid())):
            for x in range(len(self.board.to_grid()[y])):
                if x == self.x:
                    same_col.append(self.board.to_grid()[y][x])
        for y in enumerate(same_col):
            if y[1] in 'OP-S':
                if y[1] == 'O':
                    garbage_y.append(y[0])
            else:
                obstacles_y.append(y[0])
        return [garbage_y, obstacles_y]

    def _move_x(self, x: int) -> None:
        """Indicate which x direction the raccoon is closer to the garbage can.

        >>> b = GameBoard(3, 3)
        >>> s = SmartRaccoon(b, 0, 0)
        >>> s._move_x(1)
        """
        if self.x - x >= 0 and \
                self.board.to_grid()[self.y][self.x - x] == 'O':
            self.move(LEFT)
        elif self.x + x < self.board.width and \
                self.board.to_grid()[self.y][self.x + x] == 'O':
            self.move(RIGHT)

    def _move_y(self, y: int) -> None:
        """Indicate which y direction the raccoon is closer to the garbage can.

        >>> b = GameBoard(3, 3)
        >>> s = SmartRaccoon(b, 0, 0)
        >>> s._move_y(1)
        """
        if self.y - y >= 0 and \
                self.board.to_grid()[self.y - y][self.x] == 'O':
            self.move(UP)
        elif self.y + y < self.board.height and \
                self.board.to_grid()[self.y + y][self.x] == 'O':
            self.move(DOWN)

    def get_char(self) -> chr:
        """
        Return '@' to represent that this SmartRaccoon is inside a Garbage Can
        and 'S' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'S'


class GarbageCan(Character):
    """A garbage can in the game.

    === Public Attributes ===
    locked:
        whether or not this GarbageCan is locked.

    === Sample Usage ===
    >>> b = GameBoard(2, 2)
    >>> g = GarbageCan(b, 0, 0, False)
    >>> g.x, g.y
    (0, 0)
    >>> g.locked
    False
    """
    locked: bool

    def __init__(self, b: GameBoard, x: int, y: int, locked: bool) -> None:
        """Initialize this GarbageCan to be at tile (<x>, <y>) and store
        whether it is locked or not based on <locked>.
        """
        self.locked = locked
        Character.__init__(self, b, x, y)

    def get_char(self) -> chr:
        """
        Return 'C' to represent a closed garbage can and 'O' to represent
        an open garbage can.
        """
        if self.locked:
            return 'C'
        return 'O'

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Garbage cans cannot move, so always return False.
        """
        return False


# A helper function you may find useful for Task #5, depending on how
# you implement it.
def get_neighbours(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Return the coordinates of the four tiles adjacent to <tile>.

    This does NOT check if they are valid coordinates of a board.

    >>> ns = set(get_neighbours((2, 3)))
    >>> {(2, 2), (2, 4), (1, 3), (3, 3)} == ns
    True
    """
    rslt = []
    for direction in DIRECTIONS:
        rslt.append((tile[0] + direction[0], tile[1] + direction[1]))
    return rslt


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': [],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', '__future__', 'math'],
        'disable': ['E1136'],
        'max-attributes': 15,
        'max-module-lines': 1600
    })
