from Classes.game import Person, bcolors
from Classes.magic import Spell

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Initialize People
player = Person(460, 65, 60, 34, [fire, thunder, meteor, blizzard, cure, cura])
enemy = Person(1200, 65, 45, 25, [])

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("======================")
    player.choose_action()
    choice = input("Chose action: ")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for:", dmg, "points of damage.")
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Chose magic:")) - 1

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot Enough MP.\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for: ", magic_dmg, "HP." + bcolors.ENDC)
        elif spell.type == "black":
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", magic_dmg, "points of damage." + bcolors.ENDC )

    enemy_choice = 1
    dmg = enemy.generate_damage()
    player.take_damage(dmg)
    print("Enemy attacked for:", dmg, "points of damage.")

    print("____________________________")
    print("Enemy HP:" + bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_maxhp()) + bcolors.ENDC +
          "\nPlayer HP:" + bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_maxhp()) + bcolors.ENDC )
    print("Player MP:" + bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_maxmp()) + bcolors.ENDC)
    print("\n")

    if player.get_hp() == 0:
        print(bcolors.FAIL + bcolors.BOLD + "YOU LOSE :(" + bcolors.ENDC)
        running = False
    elif enemy.get_hp() == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "YOU WIN!!" + bcolors.ENDC)
        running = False