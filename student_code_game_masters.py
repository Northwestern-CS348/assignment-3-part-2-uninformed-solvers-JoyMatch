from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3,4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        Bindings_list_peg1 = self.kb.kb_ask(parse_input('fact: (on ?x peg1)'))
        if Bindings_list_peg1:
            ind = []
            for i in range(len(Bindings_list_peg1)):
                ind.append(int(Bindings_list_peg1[i].bindings_dict["?x"][4]))
            ind.sort()
            p1 = tuple(ind)
        else:
            p1 = ()

        Bindings_list_peg2 = self.kb.kb_ask(parse_input('fact: (on ?x peg2)'))
        if Bindings_list_peg2:
            ind = []
            for i in range(len(Bindings_list_peg2)):
                ind.append(int(Bindings_list_peg2[i].bindings_dict["?x"][4]))
            ind.sort()
            p2 = tuple(ind)
        else:
            p2 = ()

        Bindings_list_peg3 = self.kb.kb_ask(parse_input('fact: (on ?x peg3)'))
        if Bindings_list_peg3:
            ind = []
            for i in range(len(Bindings_list_peg3)):
                ind.append(int(Bindings_list_peg3[i].bindings_dict["?x"][4]))
            ind.sort()
            p3 = tuple(ind)
        else:
            p3 = ()

        return (p1, p2, p3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = movable_statement.terms

        retract_facts = []
        new_facts = []

        retract_facts.append(parse_input('fact: (on '+str(sl[0])+' '+str(sl[1])+')'))
        new_facts.append(parse_input('fact: (on '+str(sl[0])+' '+str(sl[2])+')'))
        retract_facts.append(parse_input('fact: (top '+str(sl[0])+' '+str(sl[1])+')'))
        new_facts.append(parse_input('fact: (top '+str(sl[0])+' '+str(sl[2])+')'))

        onsl1 = self.kb.kb_ask(parse_input('fact: (above '+str(sl[0])+' ?x)'))
        if onsl1:
            retract_facts.append(parse_input('fact: (above '+str(sl[0])+' '+onsl1[0]['?x']+')'))
            new_facts.append(parse_input('fact: (top '+onsl1[0]['?x']+' '+str(sl[1])+')'))
        else:
            new_facts.append(parse_input('fact: (empty '+str(sl[1])+')'))

        onsl2 = self.kb.kb_ask(parse_input('fact: (top ?x '+str(sl[2])+')'))
        if onsl2:
            retract_facts.append(parse_input('fact: (top '+onsl2[0]['?x']+' '+str(sl[2])+')'))
            new_facts.append(parse_input('fact: (above '+str(sl[0])+' '+onsl2[0]['?x']+')'))
        else:
            retract_facts.append(parse_input('fact: (empty '+str(sl[2])+')'))

        for _ in retract_facts:
            self.kb.kb_retract(_)
        for _ in new_facts:
            self.kb.kb_assert(_)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        Bindings_list = []
        for j in range(1,4):
            for i in range(1,4):
                Bindings_list.append(self.kb.kb_ask(parse_input('fact: (on ?tile pos' + str(i) +' pos'+str(j))))
        result = []
        for _ in range(len(Bindings_list)):
            if Bindings_list[_][0].bindings_dict["?tile"] == "empty":
                result.append(int(-1))
            else:
                result.append(int(Bindings_list[_][0].bindings_dict["?tile"][4]))
        return ((result[0],result[1],result[2]), (result[3],result[4],result[5]), (result[6],result[7],result[8]))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = movable_statement.terms
        new_fact_0 = ["on", sl[0], sl[3], sl[4]]
        new_fact_1 = ["on", "empty", sl[1], sl[2]]
        retracted_fact_0 = ["on", sl[0], sl[1], sl[2]]
        retracted_fact_1 = ["on", "empty", sl[3], sl[4]]
        self.kb.kb_retract(Fact(Statement(retracted_fact_0)))
        self.kb.kb_retract(Fact(Statement(retracted_fact_1)))
        self.kb.kb_assert(Fact(Statement(new_fact_0)))
        self.kb.kb_assert(Fact(Statement(new_fact_1)))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))