"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
from typing import Any
import random
from a2_tree_of_states import TOS, get_children


class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue 
        new_battle_queue.
        """
        raise NotImplementedError


class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the 
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)


class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the 
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    >>> bq1 = BattleQueue()
    >>> r1 = Rogue("r", bq1, ManualPlaystyle(bq1))
    >>> m1 = Mage("m", bq1, ManualPlaystyle(bq1))
    >>> r1.enemy = m1
    >>> m1.enemy = r1
    >>> bq1.add(m1)
    >>> bq1.add(r1)
    >>> r1.set_hp(40)
    >>> r1.set_sp(6)
    >>> m1.set_hp(14)
    >>> m1.set_sp(35)
    >>> get_state_score(bq1)
    7
    """
    # TODO: Implement the get_state_score function (which will be used in
    #                  recursive minimax)
    if battle_queue.is_over():
        if battle_queue.get_winner():
            if battle_queue.peek().get_name() == \
                    battle_queue.get_winner().get_name():
                return battle_queue.peek().get_hp()
            if battle_queue.peek().get_name() != \
                    battle_queue.get_winner().get_name():
                return -1 * battle_queue.get_winner().get_hp()
        return 0
    new_bq_list = []
    if battle_queue.peek().get_available_actions():
        for action in battle_queue.peek().get_available_actions():
            bq = battle_queue.copy()
            if action == 'A':
                bq.peek().attack()
            elif action == 'S':
                bq.peek().special_attack()
            if not bq.is_empty():
                bq.remove()
            new_bq_list.append(bq)
    return max(-1 * get_state_score(bq) if 
               battle_queue.peek().get_name() != bq.peek().get_name() 
               else get_state_score(bq) for bq in new_bq_list if new_bq_list)

# TODO: Implement classes for Recursive Minimax and Iterative Minimax


class RecursiveMinimax(Playstyle):
    """
    The Minimax playstyle. Inherits from Playstyle.
    Implemented recursively.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RecursiveMinimaxPlaystyle with BattleQueue as its 
        battle queue.
        >>> 
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Select the action that can guarantee the highest state score for the 
        character.
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq1 = BattleQueue()
        >>> r1 = Rogue("r", bq1, RecursiveMinimax(bq1))
        >>> m1 = Mage("m", bq1, RecursiveMinimax(bq1))
        >>> r1.enemy = m1
        >>> m1.enemy = r1
        >>> bq1.add(m1)
        >>> bq1.add(r1)
        >>> r1.set_hp(40)
        >>> r1.set_sp(6)
        >>> m1.set_hp(14)
        >>> m1.set_sp(35)
        >>> type(r1.playstyle) == RecursiveMinimax
        True
        """
        actions = self.battle_queue.peek().get_available_actions()
        if not actions:
            return 'X'
        current_player = self.battle_queue.peek().get_name()
        current_state_score = get_state_score(self.battle_queue)
        for action in actions:
            a_copy = self.battle_queue.copy()
            if action == 'A':
                a_copy.peek().attack()
                if not a_copy.is_over():
                    a_copy.remove()
                if a_copy.peek().get_name() == current_player:
                    return 'A' if get_state_score(a_copy) == \
                                  current_state_score else \
                                  'S' if 'S' in actions else 'X'
                if a_copy.peek().get_name() != current_player:
                    return 'A' if -get_state_score(a_copy) == \
                           current_state_score else 'S' if 'S' in actions else \
                        'X'
            elif action == 'S':
                a_copy.peek().special_attack()
                if not a_copy.is_empty():
                    a_copy.remove()
                if a_copy.peek().get_name() == current_player:
                    return 'S' if get_state_score(a_copy) == \
                                  current_state_score \
                                  else 'A' if 'A' in actions else 'X'
                if a_copy.peek().get_name() != current_player:
                    return 'S' if -get_state_score(a_copy) == \
                           current_state_score \
                           else 'A' if 'A' in actions else 'X'
        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'RecursiveMinimax':
        """
        Return a copy of this RandomPlaystyle which uses the 
        BattleQueue new_battle_queue.
        """
        return RecursiveMinimax(new_battle_queue)


class IterativeMinimax(Playstyle):
    """
    The Minimax playstyle. Inherits from Playstyle.
    Implemented iteratively.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def helper_get_the_whole_tree(self) -> TOS:
        """
        This is a helper function for IterativeMinimax select_attack method.
        It uses one given battle_queue(state) to get all possible states 
        afterwards.
        It also get all paths from the end states to the given state, each node
        in the path is stored in the form of a list with four attributes.
        """
        current_battle_queue = self.battle_queue.copy()
        t = TOS(current_battle_queue)
        tloc = get_children(t)
        t.children = tloc
        if tloc:
            for c in tloc:
                if c.battle_q.is_over():
                    path = [[c.caster, c.last_round_caster,
                             c.last_round_taken_action, c.score],
                            [c.last_round.caster,
                             c.last_round.last_round_caster,
                             c.last_round.last_round_taken_action,
                             c.last_round.score]]
                    t.possible_paths.append(path)
                    if len(c.last_round.caster.get_available_actions()) == 2:
                        t.snppc[c.last_round_caster] = [(0, 1)]
        while tloc != []:
            tloc = get_children(tloc)
            for c in tloc:
                if c.battle_q.is_over():
                    path = [[c.caster, c.last_round_caster,
                             c.last_round_taken_action, c.score]]
                    while c.last_round:
                        path.append([c.last_round.caster,
                                     c.last_round.last_round_caster,
                                     c.last_round.last_round_taken_action,
                                     c.last_round.score])
                        if len(c.last_round.caster.get_available_actions()) \
                                == 2:
                            if c.last_round.caster in \
                                    t.snppc:
                                t.snppc[c.last_round.caster].append(
                                    (len(t.possible_paths), len(path) - 1))
                            elif c.last_round.caster not in t.snppc:
                                t.snppc[c.last_round.caster] = [
                                    (len(t.possible_paths), len(path) - 1)]
                        c = c.last_round
                    t.possible_paths.append(path)
        return t

    def helper_assign_all_scores(self):
        """
        This is a helper function for assigning all the scores correctly for
        the tree of states.

        The efficiency of this function is SUPER LOW!!!
        If got time out error on unittest, Please consider re-run it for about 
        6 more min, it will work.(Given unittest took 221s last time)
        """
        t = self.helper_get_the_whole_tree()
        for path in t.possible_paths:
            for i in range(len(path) - 1):
                if path[i][3] and path[i + 1][3] and \
                        type(path[i + 1][3]) == list:
                    if len(path[i + 1][0].get_available_actions()) == 2:
                        if path[i][0].get_name() == path[i + 1][0].get_name():
                            path[i + 1][3].append(path[i][3][0])
                        if path[i][0].get_name() != path[i + 1][0].get_name():
                            path[i + 1][3].append(-path[i][3][0])
                        if len(path[i + 1][3]) > 1:
                            path[i + 1][3] = [max(path[i + 1][3])]
                    if path[i][0].get_name() == path[i + 1][0].get_name():
                        path[i + 1][3].append(path[i][3][0])
                    if path[i][0].get_name() != path[i + 1][0].get_name():
                        path[i + 1][3].append(-path[i][3][0])
                if path[i][3] and not path[i + 1][3]:
                    if len(path[i + 1][0].get_available_actions()) == 2:
                        if path[i][0].get_name() == path[i + 1][0].get_name():
                            path[i + 1][3] = path[i][3][:]
                        if path[i][0].get_name() != path[i + 1][0].get_name():
                            path[i + 1][3] = [-path[i][3][0]]
                        for node in t.snppc:
                            if node == path[i + 1][0]:
                                for pos in t.snppc[node]:
                                    t.possible_paths[pos[0]][pos[1]][3] = \
                                     path[i + 1][3][:]
                        break
                    if path[i][0].get_name() == path[i + 1][0].get_name():
                        path[i + 1][3] = path[i][3][:]
                    if path[i][0].get_name() != path[i + 1][0].get_name():
                        path[i + 1][3] = [-path[i][3][0]]
        return t

    def select_attack(self, parameter: Any = None) -> str:
        """
        Select the action that can guarantee the highest state score for the 
        character.
        """
        t = self.helper_assign_all_scores()
        if t.children == []:
            return 'X'
        if len(t.children) == 1:
            return t.possible_paths[0][-2][2]
        score = t.possible_paths[-1][-1][3][0]
        for path in t.possible_paths:
            if path[-2][0].get_name() == t.caster.get_name():
                if path[-2][3] and path[-2][3][0] == score:
                    return path[-2][2]
            elif path[-2][0].get_name() != t.caster.get_name():
                if path[-2][3] and path[-2][3][0] == -score:
                    return path[-2][2]
        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'IterativeMinimax':
        """
        Return a copy of this RandomPlaystyle which uses the 
        BattleQueue new_battle_queue.
        """
        return IterativeMinimax(new_battle_queue)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
