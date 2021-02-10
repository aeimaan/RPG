import random
from .magic import Spell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.action = ["Attack", "Magic", "Item"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def set_hp(self, heal):
        self.hp = heal

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def choose_action(self):
        i = 1
        print("\n    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    Actions" + bcolors.ENDC)
        for item in self.action:
            print("        " + str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    Magic" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    Item" + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ": " + item["item"].get_name() + " --> " + item["item"].get_description(), " (x"+ str(item["quantity"])+ ")")
            i += 1

    def get_item(self, index):
        return self.items[index]["item"]

    def get_quantity(self, index):
        return self.items[index]["quantity"]

    def get_stats(self):
        # █
        HPbar = ""
        MPbar = ""
        bar_amount = (self.hp/self.maxhp) * 25

        while bar_amount > 0:
            HPbar += "█"
            bar_amount -= 1

        while len(HPbar) < 25:
            HPbar += " "

        MPbar_amount = (self.mp/self.maxmp) * 10

        while MPbar_amount > 0:
            MPbar += "█"
            MPbar_amount -= 1

        while len(MPbar) < 10:
            MPbar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decrease = 9 - len(hp_string)

            while decrease > 0:
                current_hp += " "
                decrease -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decrease = 7 - len(mp_string)
            while decrease > 0:
                current_mp += " "
                decrease -= 1
            current_mp += mp_string
        else:
            current_mp = mp_string

        print("                    _________________________               __________")
        print(bcolors.BOLD + self.name + "    " + current_hp + "|" + bcolors.OKGREEN + HPbar
              + bcolors.ENDC
              + "|    " + current_mp + "  |" + bcolors.OKBLUE + MPbar +
              bcolors.ENDC +
              "|")

    def get_enemy_stats(self):
        hp_bar = ""
        amount_hp = (self.hp / self.maxhp) * 50

        mp_bar = ""
        amount_mp = (self.mp / self.maxmp) * 10

        while amount_hp > 0:
            hp_bar += "█"
            amount_hp -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decrease = 9 - len(hp_string)

            while decrease > 0:
                current_hp += " "
                decrease -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                    __________________________________________________")
        print(bcolors.BOLD + self.name + "  " + current_hp + "|" + bcolors.FAIL + hp_bar
              + bcolors.ENDC
              + "|")

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() == 0:
                continue
            print("       " + str(i) + ": " + enemy.name)
            i += 1
        chosen = (int(input("    Choose Enemy: ")) -1)
        return enemies[chosen], chosen

    def choose_enemy_spell(self):

        magic = self.magic[random.randrange(0, len(self.magic))]
        dmg = magic.generate_damage()

        percent = self.get_hp() / self.get_maxhp() * 100

        if (self.get_mp() < magic.cost) or ((magic.type == "white") and (percent > 50)):
            self.choose_enemy_spell()
        else:
            return magic, dmg
