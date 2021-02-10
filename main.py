from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Iteam
import random

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


# Create Items
potion = Iteam("Potion", "potion", "Heals 50 hp", 50)
hi_potion = Iteam("High Potion", "potion", "Heals 100 hp", 100)
super_potion = Iteam("Super potion", "potion", "Heals 200 hp", 200)
elixir = Iteam("Elixir", "elixir", "Fully restores HP/MP of one member", 9999)
hi_elixir = Iteam("High Elixir", "elixir", "Fully restores party's HP/Mp", 9999)

grenade = Iteam("Grenade", "attack", "Deals 500 damage", 500)


# Create List/Dictionary for Spells/Items
player_spells = [fire, thunder, meteor, blizzard, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hi_potion, "quantity": 5}, {"item": super_potion, "quantity":5},
                {"item": elixir, "quantity": 5}, {"item": hi_elixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Initialize People
player1 = Person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Adam :", 4160, 188, 290, 34, player_spells, player_items)
player3 = Person("Eman :", 3089, 174, 288, 34, player_spells, player_items)

enemy2 = Person("Hench1  ", 1250, 130, 560, 325, enemy_spells, [])
enemy1 = Person("Margwa", 12000, 221, 500, 25, enemy_spells, [])
enemy3 = Person("Hench2  ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]

# Alive
running = True
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("==========================")
    print("\n\n")
    print("NAME              HP                                    MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Chose action: ")
        index = int(choice) - 1

        # chose attack
        if index == 0:
            dmg = player.generate_damage()
            enemy, chosen = player.choose_target(enemies)
            enemy.take_damage(dmg)
            print("You attacked " + enemy.name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemy.get_hp() == 0:
                print(enemy.name.replace(" ", "") + " has died.")
                del enemies[chosen]

        # chose spells
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Chose Magic:")) - 1

            if magic_choice == -1:
                continue

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
                enemy, chosen = player.choose_target(enemies)
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", magic_dmg, "points of damage. To "
                      + enemy.name.replace(" ", "") + bcolors.ENDC)
                if enemy.get_hp() == 0:
                    print(enemy.name.replace(" ", "") + " has died.")
                    del enemies[chosen]

        # chose Items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Chose Item: ")) - 1

            if item_choice == -1:
                continue

            item = (player.get_item(item_choice))
            quantity = player.get_quantity(item_choice)

            if quantity > 0:
                player.items[item_choice]["quantity"] = quantity - 1
            else:
                print(bcolors.FAIL + "\n" + "None Left..." + bcolors.ENDC)
                continue

            if item.get_type() == "potion":
                player.heal(item.get_property())
                print(bcolors.OKGREEN + "\n" + item.get_name() + " heals for", item.get_property(), "HP" + bcolors.ENDC)
            elif item.get_type() == "elixir":

                if item.name == "High Elixir":
                    for i in players:
                        i.set_hp(i.get_maxhp())
                        i.mp = i.maxmp
                else:
                    player.set_hp(player.get_maxhp())
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.get_name() + "fully restores HP/MP" + bcolors.ENDC)
            elif item.get_type() == "attack":
                enemy, chosen = player.choose_target(enemies)
                enemy.take_damage(item.get_property())
                print(bcolors.FAIL + "\n" + item.get_name(), "Does", item.get_property(), "points of damage. To " +
                      enemy.name.replace(" ", "") + bcolors.ENDC)

                if enemy.get_hp() == 0:
                    print(enemy.name.replace(" ", "") + " has died.")
                    del enemies[chosen]

# Checks if battle is over
    defeated_enemies = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    dead_players = 0
    for player in players:
        if player.get_hp() == 0:
            dead_players += 1
# Win/Lose check
    if dead_players == 3:
        print(bcolors.FAIL + bcolors.BOLD + "YOU LOSE :(" + bcolors.ENDC)
        running = False
    elif defeated_enemies == 3:
        print(bcolors.OKGREEN + bcolors.BOLD + "YOU WIN!!" + bcolors.ENDC)
        running = False

    print("\n")
# Enemy Attack
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, len(players))
            dmg = enemies[0].generate_damage()
            players[target].take_damage(dmg)
            print(enemy.name.replace(" ", "") + " attacked", players[target].name.replace(":", ""), "for:",
                  dmg, "points of damage.")
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.FAIL + spell.name + " heals " + enemy.name.replace(" ", "") + " for:", magic_dmg, "HP." + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(players))

                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", magic_dmg, "points of damage to "
                      + players[target].name.replace(":", "") + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
