import json

class Internal:

    last_damage = 0

    def __init__(self, *, health_points: int = 50, attack_power: int, level: int) -> None:
        self.level = level
        self.health_points = health_points * level
        self.attack_power = attack_power * level

    def attack(self, *, target: "Internal") -> int:
        target.got_damage(damage=self.attack_power)
        return self.attack_power

    def got_damage(self, *, damage: int) -> None:
        damage = damage * (100 - self.defence) / 100
        damage = round(damage)
        self.last_damage = damage
        self.health_points -= damage

    def is_alive(self) -> bool:
        return self.health_points > 0

    @property
    def defence(self) -> int:
        defence = self.base_defence * self.level
        return defence

    @property
    def max_health_points(self) -> int:
        return self.level * self.health_points

    def health_points_percent(self):
        return 100 * self.health_points / self.max_health_points

    def level_up(self):
            self.level += 1
            self.health_points += int(self.max_health_points / 2)

    def __str__(self) -> str:
        return f"{self.internal_name} (level: {self.level}, hp: {self.health_points})"


class Warrior(Internal):
    internal_name = "Warrior"
    base_defence = 15

    @property
    def defence(self) -> int:
        defence = super().defence
        if self.health_points < 50:
            defence *= 3

        return defence


class Monster(Internal):
    internal_name = "Monstr"
    base_defence = 10

    def attack(self, *, target: "Internal") -> None:
        attack_power = self.attack_power
        if target.health_points_percent() < 30:
            attack_power = self.attack_power * 3
        target.got_damage(damage=attack_power)

file = open('data/heroes.json', 'r')
heroes_data = json.load(file)
file.close()

warrior_heroes = []
monster_heroes =[]
for hero in heroes_data:
    if hero['internal_name'] == 'warrior':
        warrior_heroes.append(Warrior(level=hero['level'], health_points=hero['health_points'], attack_power=hero['attack_power']))
    elif hero['internal_name'] == 'monster':
       monster_heroes.append(Monster(level=hero['level'], health_points=hero['health_points'], attack_power=hero['attack_power']))

print(len(warrior_heroes))
print(len(monster_heroes))


def fight(*, internal_1: Internal, internal_2: Internal) -> None:
    print("Fight started", internal_1, internal_2)
    while internal_1.is_alive() and internal_2.is_alive():
        attack = internal_1.attack(target=internal_2)
        print(f'{internal_1.internal_name} attacks with {attack} damage')
        print(f'{internal_2.internal_name} got damage { internal_2.last_damage }')

        if internal_2.is_alive():
            internal_2.attack(target=internal_1)
            print(f'{internal_2.internal_name} attacks with {attack} damage')
            print(f'{internal_1.internal_name} got damage { internal_1.last_damage }')

    print(f"{internal_1.internal_name} is {'alive' if internal_1.is_alive() else 'dead'}, ", internal_1)
    print(f"{internal_2.internal_name} is {'alive' if internal_2.is_alive() else 'dead'},", internal_2)

def arena() -> None:
    while len(warrior_heroes) > 0 and len(monster_heroes) > 0:
        print('\n\n--------NEW FIGHT -------')
        fight(internal_1=warrior_heroes[0], internal_2=monster_heroes[0])

        if warrior_heroes[0].is_alive():
            monster_heroes.pop(0)
        elif monster_heroes[0].is_alive():
            warrior_heroes.pop(0)

    if len(warrior_heroes) > 0:
        print('----------------------------')
        print("|  Warrior's team are won. |")
        print('----------------------------')
    else:
        print('----------------------------')
        print("|  Monster's team are won. |")
        print('----------------------------')
arena()
