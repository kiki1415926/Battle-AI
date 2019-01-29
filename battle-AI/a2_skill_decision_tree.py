"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill', 
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None) -> None:
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []

    def helper_get_all_path(self, caster: 'Character', target: 'Character')\
            -> list:
        """
        Return a list of skills that all skills in the list are condition 
        fulfilled.
        >>> t = create_default_tree()
        >>> from a2_skills import MageSpecial
        >>> from a2_characters import Mage, Rogue
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> caster = Mage('s', bq, ManualPlaystyle)
        >>> target = Rogue('r', bq, ManualPlaystyle)
        >>> caster._hp = 100
        >>> caster._sp = 40
        >>> target._hp = 50
        >>> target._sp = 30
        >>> t.helper_get_all_path(caster, target)[0][0][0] == 5
        True
        >>> type(t.helper_get_all_path(caster, target)[0][0][1]) == MageSpecial
        False
        >>> t.helper_get_all_path(caster, target)[0][0][2]
        True
        >>> caster.set_hp(10)
        >>> caster.get_hp()
        10
        >>> t.helper_get_all_path(caster, target)[0][0][2]
        False
        >>> t.helper_get_all_path(caster, target)[0][1][2]
        True
        >>> t.helper_get_all_path(caster, target)[0][2][2]
        False
        """
        if self.children == []:
            return [[[self.priority, self.value, 
                      self.condition(caster, target)]]]
        all_paths = []
        for child in self.children:
            p = child.helper_get_all_path(caster, target)
            for p2 in p:
                p2.insert(0, [self.priority, self.value, 
                              self.condition(caster, target)])
                all_paths.append(p2)
        return all_paths

    # Implement a method called pick_skill which takes in a caster and target
    # and returns a skill.

    def pick_skill(self, caster: 'Character', target: 'Character') -> 'Skill':
        """
        Return a skill for caster to use based on conditions and priority.
        >>> t = create_default_tree()
        >>> from a2_skills import MageSpecial, RogueSpecial
        >>> from a2_characters import Mage, Rogue
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> bq = BattleQueue()
        >>> caster = Mage('s', bq, ManualPlaystyle)
        >>> target = Rogue('r', bq, ManualPlaystyle)
        >>> caster._hp = 100
        >>> caster._sp = 40
        >>> target._hp = 50
        >>> target._sp = 30
        >>> type(t.pick_skill(caster, target)) == MageSpecial
        True
        >>> caster._hp = 100
        >>> caster._sp = 100
        >>> target._hp = 100
        >>> target._sp = 100
        >>> type(t.pick_skill(caster, target)) == RogueSpecial
        True
        """
        waiting_list = self.helper_get_all_path(caster, target)
        skills = []
        skills_priority = []
        for path in waiting_list:
            if path[0][2] is False:
                skills.append(path[0][1])
                skills_priority.append(path[0][0])
                break
            for skill in path:
                if skill[2] is False and skill[0] not in skills_priority and \
                        skill[1] not in skills:
                    skills_priority.append(skill[0])
                    skills.append(skill[1])
                    break
        position = 0
        for i in range(len(skills_priority)):
            if skills_priority[i] == min(skills_priority):
                position = i
        return skills[position]


def caster_hp_more_than_50(caster: 'Character', _) -> bool:
    """
    Return True if caster has more than 50 hp.
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> caster = Mage('s', bq, ManualPlaystyle)
    >>> target = Rogue('r', bq, ManualPlaystyle)
    >>> caster._hp = 100
    >>> caster._sp = 40
    >>> target._hp = 50
    >>> target._sp = 30
    >>> caster_hp_more_than_50(caster, target)
    True
    >>> caster._hp = 10
    >>> caster_hp_more_than_50(caster, target)
    False
    """
    return caster.get_hp() > 50


def caster_sp_more_than_20(caster: 'Character', _) -> bool:
    """
    Return True if caster has more than 20 sp.
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> caster = Mage('s', bq, ManualPlaystyle)
    >>> target = Rogue('r', bq, ManualPlaystyle)
    >>> caster._hp = 100
    >>> caster._sp = 40
    >>> target._hp = 50
    >>> target._sp = 30
    >>> caster_sp_more_than_20(caster, target)
    True
    >>> caster._sp = 10
    >>> caster_sp_more_than_20(caster, target)
    False
    """
    return caster.get_sp() > 20


def target_hp_less_than_30(_, target: 'Character') -> bool:
    """Return True if target has less than 30 hp.
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> caster = Mage('s', bq, ManualPlaystyle)
    >>> target = Rogue('r', bq, ManualPlaystyle)
    >>> caster._hp = 100
    >>> caster._sp = 40
    >>> target._hp = 9
    >>> target._sp = 30
    >>> target_hp_less_than_30(caster, target)
    True
    >>> target = Rogue('r', bq, ManualPlaystyle)
    >>> caster._hp = 100
    >>> caster._sp = 40
    >>> target._hp = 100
    >>> target._sp = 30
    >>> target_hp_less_than_30(caster, target)
    False
    """
    return target.get_hp() < 30


def target_sp_more_than_40(_, target: 'Character') -> bool:
    """
    Return True if target has more than 40 sp.
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> caster = Mage('s', bq, ManualPlaystyle)
    >>> target = Rogue('r', bq, ManualPlaystyle)
    >>> caster._hp = 100
    >>> caster._sp = 40
    >>> target._hp = 50
    >>> target._sp = 30
    >>> target_sp_more_than_40(caster, target)
    False
    >>> target._sp = 50
    >>> target_sp_more_than_40(caster, target)
    True
    """
    return target.get_sp() > 40


def caster_hp_more_than_90(caster: 'Character', _) -> bool:
    """
    Return True if caster has more than 90 hp.
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> caster = Mage('s', bq, ManualPlaystyle)
    >>> target = Rogue('r', bq, ManualPlaystyle)
    >>> caster._hp = 100
    >>> caster._sp = 40
    >>> target._hp = 50
    >>> target._sp = 30
    >>> caster_hp_more_than_90(caster, target)
    True
    >>> caster._hp = 0
    >>> caster_hp_more_than_90(caster, target)
    False
    """
    return caster.get_hp() > 90


def just_want_return_false(_, __) -> bool:
    """
    Return False.
    """
    return False


def create_default_tree() -> SkillDecisionTree:
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    >>> from a2_skills import MageAttack
    >>> t = create_default_tree()
    >>> t.priority
    5
    >>> str(t.condition)[10:32]
    'caster_hp_more_than_50'
    >>> type(t.value) == MageAttack
    True
    """
    from a2_skills import MageAttack, MageSpecial, RogueAttack, RogueSpecial
    t1 = SkillDecisionTree(MageAttack(), caster_sp_more_than_20, 3)
    t2 = SkillDecisionTree(RogueSpecial(), target_hp_less_than_30, 4)
    t3 = SkillDecisionTree(RogueAttack(), just_want_return_false, 6)
    t4 = SkillDecisionTree(MageSpecial(), target_sp_more_than_40, 2)
    t5 = SkillDecisionTree(RogueAttack(), just_want_return_false, 8)
    t6 = SkillDecisionTree(RogueAttack(), caster_hp_more_than_90, 1)
    t7 = SkillDecisionTree(RogueSpecial(), just_want_return_false, 7)
    t1.children = [t2]
    t2.children = [t3]
    t4.children = [t5]
    t6.children = [t7]
    t = SkillDecisionTree(MageAttack(), caster_hp_more_than_50, 5, [t1, t4, t6])
    return t


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
