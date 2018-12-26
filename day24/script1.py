import re
import functools


class Group:
    def __init__(self, army, units, hp, weak, immune, dmg, dmg_type, initiative):
        GLOBS['last_id'] += 1
        self.id = GLOBS['last_id']
        self.army = army
        self.units = units
        self.hp = hp
        self.weak = weak
        self.immune = immune
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.initiative = initiative

    def to_str(self):
        return 'Group(' + str(self.id) + ', ' + self.army + ', ' + str(self.units) + ')'


GROUPS: [Group] = []
GLOBS = {'last_id': -1}


def parse(lines):
    army = ''
    while lines:
        line = lines.pop(0).strip()
        if not line:
            continue
        elif 'Immune System' in line:
            army = 'Immune System'
        elif 'Infection' in line:
            army = 'Infection'
        else:
            m = re.match(r'(\d+) units each with (\d+) hit points (.*)with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)', line)
            units, hp, weak_immune, dmg, dmg_type, initiative = m.groups()
            units, hp, dmg, initiative = int(units), int(hp), int(dmg), int(initiative)
            weak = []
            immune = []
            if 'weak' in weak_immune:
                m = re.match(r'\(.*weak to ([a-z, ]+)', weak_immune)
                weak.extend(m.group(1).replace(' ', '').split(','))
            if 'immune' in weak_immune:
                m = re.match(r'\(.*immune to ([a-z, ]+)', weak_immune)
                immune.extend(m.group(1).replace(' ', '').split(','))
            GROUPS.append(Group(army, units, hp, weak, immune, dmg, dmg_type, initiative))


def order_by_effective_power(id1, id2):
    group1 = GROUPS[id1]
    group2 = GROUPS[id2]
    if group1.units * group1.dmg > group2.units * group2.dmg:
        return 1
    elif group1.units * group1.dmg < group2.units * group2.dmg:
        return -1
    elif group1.initiative > group2.initiative:
        return 1
    elif group1.initiative < group2.initiative:
        return -1
    else:
        raise SyntaxError('ERROR - Still a tie !!')


def target_selection():
    attackers = [id for id in range(len(GROUPS)) if GROUPS[id].units > 0]
    attackers = sorted(attackers, key=functools.cmp_to_key(order_by_effective_power), reverse=True)
    selected_targets = []
    for group_id in attackers:
        attacker = GROUPS[group_id]
        best_target = None
        dmg_to_best = 0
        for defender in GROUPS:
            new_best = False
            if defender.army == attacker.army:          # friend
                continue
            elif defender.units <= 0:                     # ennemy already dead
                continue
            elif attacker.dmg_type in defender.immune:    # ennemy immuned
                continue
            elif defender.id in [y for (x, y) in selected_targets]:
                continue                                    # ennemy already targeted

            dmg = attacker.units * attacker.dmg
            if attacker.dmg_type in defender.weak:
                dmg *= 2

            if dmg < dmg_to_best:
                continue                                # not the best target
            elif best_target is None or dmg > dmg_to_best:
                new_best = True
            elif dmg == dmg_to_best:                    # if Tie, compare eff poser
                eff_pow = defender.units * defender.dmg
                eff_pow_best = GROUPS[best_target].units * GROUPS[best_target].dmg
                if eff_pow < eff_pow_best:
                    continue
                elif eff_pow > eff_pow_best:
                    new_best = True
                elif eff_pow == eff_pow_best:           # if Tie again compare initiative
                    init_best = GROUPS[best_target].initiative
                    if defender.initiative < init_best:
                        continue
                    elif defender.initiative > init_best:
                        new_best = True
                    else:
                        raise SyntaxError('Still a tie !!')

            if new_best:
                best_target = defender.id
                dmg_to_best = dmg

        if best_target is not None:
            selected_targets.append((group_id, best_target))
    return selected_targets


def order_by_init(battle1, battle2):
    group1 = GROUPS[battle1[0]]
    group2 = GROUPS[battle2[0]]
    if group1.initiative > group2.initiative:
        return 1
    elif group1.initiative < group2.initiative:
        return -1
    else:
        raise SyntaxError('ERROR - Still a tie !!')


def attack(battles):
    battles = sorted(battles, key=functools.cmp_to_key(order_by_init), reverse=True)
    for battle in battles:
        attacker = GROUPS[battle[0]]
        defender = GROUPS[battle[1]]
        if attacker.units <= 0 or defender.units <= 0:
            continue
        eff_power = attacker.units * attacker.dmg
        if attacker.dmg_type in defender.weak:
            eff_power *= 2
        frags = min(int(eff_power / defender.hp), defender.units)
        # print(attacker.id, ' killed ', frags, '/', defender.units, ' of group ', defender.id)
        defender.units -= frags
    return 0


def over():
    armies = []
    for group in GROUPS:
        if group.units > 0 and group.army not in armies:
            armies.append(group.army)
    if len(armies) == 1:
        print(armies[0], ' won the battle !')
    return len(armies) == 1


def state():
    for group in GROUPS:
        print(group.to_str())
    print()


def process():
    # state()
    while not over():
        battles = target_selection()
        attack(battles)
        # state()
    return sum([group.units for group in GROUPS])


def compute(file_name):
    with open(file_name, "r") as file:
        parse(file.readlines())
        return process()


if __name__ == '__main__':
    print("Units of survivors  = ", compute("data.txt"))
