"""
A tree class.
Helper class for Iterative Minimax
"""
from typing import List, Union

from a2_battle_queue import BattleQueue

class TOS:
    """
    A tree that indicates all possible states after one root state.

    battle_q - Current game state, represented by a BattleQueue.
    caster - Current player.
    children - A TOS node's children.
    possible_paths - All possible path from end state to origin.
    snppc - Split node path position counter.
    last_round - A TOS node's parent.
    last_round_caster - Represent the last round caster.
    last_round_taken_action - Represent the action taken in last round.
    score - A list of score for the state.
    """
    battle_q: 'BattleQueue'
    caster: 'Character'
    children: List['TOS'] = None
    possible_paths: list
    snppc: dict
    last_round: Union['TOS', None]
    last_round_caster: Union[str, None]
    last_round_taken_action: Union[str, None]
    score: list

    def __init__(self, battle_q: 'BattleQueue', 
                 children: List['TOS'] = None) -> None:
        """
        Initialization of TOS.
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> from a2_playstyle import ManualPlaystyle
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
        >>> t = TOS(bq1)
        >>> t.possible_paths
        []
        >>> t.score
        []
        >>> type(t.caster) == Mage
        True
        >>> t.children == []
        True
        """
        self.battle_q = battle_q
        self.caster = battle_q.peek()
        self.children = children[:] if children is not None else []
        self.possible_paths = []
        self.snppc = {}
        self.last_round = None
        self.last_round_caster = None
        self.last_round_taken_action = None
        self.score = []


def get_children_and_update(battle_q: Union['Battlequeue', TOS]) -> TOS:
    """
    Create a tree for any given state.
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> from a2_playstyle import ManualPlaystyle
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
    >>> t = TOS(bq1)
    >>> len(get_children_and_update(t).children) == 2
    True
    """
    t = TOS(battle_q) if type(battle_q) is BattleQueue else battle_q
    if not t.battle_q.is_over():
        root_caster_name = t.caster.get_name()
        for action in t.caster.get_available_actions():
            bq_copy = t.battle_q.copy()
            if action == 'A':
                bq_copy.peek().attack()
            if action == 'S':
                bq_copy.peek().special_attack()
            if not bq_copy.is_over() and \
                bq_copy.peek().get_available_actions() and \
               bq_copy.peek().enemy.get_available_actions():
                bq_copy.remove()
            c = TOS(bq_copy)
            c.last_round = t
            c.last_round_caster = root_caster_name
            c.last_round_taken_action = action
            if c.battle_q.get_winner() and c.battle_q.get_winner() == c.caster:
                c.score = [c.battle_q.get_winner().get_hp()]
                t.children.append(c)
            elif c.battle_q.is_over() and not c.battle_q.get_winner():
                c.score = [0]
                t.children.append(c)
            elif c.battle_q.get_winner() and c.battle_q.get_winner() != \
                    c.caster:
                c.score = [-c.battle_q.get_winner().get_hp()]
                t.children.append(c)
            elif not c.battle_q.is_over():
                c.score = []
                t.children.append(c)
    return t


def get_children(lot: Union[List[TOS], TOS]) -> List[TOS]:
    """
    Return a list of children based on given state(s).
    Mutate given state's(s)' children before returning.
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> from a2_playstyle import ManualPlaystyle
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
    >>> t = TOS(bq1)
    >>> len(get_children(t)) == 2
    True
    """
    list_of_children = []
    if type(lot) == list:
        for t in lot:
            t.children = get_children_and_update(t).children if not \
                t.battle_q.is_over() else []
            for child_child in t.children:
                list_of_children.append(child_child)
    else:
        t = get_children_and_update(lot.battle_q)
        for child_child in t.children:
            list_of_children.append(child_child)
    return list_of_children


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
