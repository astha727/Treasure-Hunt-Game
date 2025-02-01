import time
import sys
import os
import random

keys_collected = 0
days_left = 7

inventory = {
    "Keys Collected": 0,
    "Boat Pass": "❌ (Not yet found)",
    "Torch": "❌ (Not yet found)",
    "Compass": "❌ (Not yet found)",
    "Amulet": "❌ (Not yet found)",
    "Magical Orb": "❌ (Not yet found)",
    "Sword": "❌ (Not yet found)"
}


# ANSI escape codes for color and text styles
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

#clear screen
def clear_screen():
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def check_days_left():
    global days_left
    if days_left <= 0:
        print_slow("You have run out of time! The tsunami hits before you could collect all the keys.", color=RED)
        game_over()

def print_section_border():
    print("=" * 40)

def print_bold(text):
    print(BOLD + text + RESET)

def print_colored(text, color = RESET):
    print(color + text + RESET)

def print_slow(text, delay = 0.10, color = RESET ):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(RESET)

def game_over():
    print_slow('You are Dead! Game Over!', color=RED)
    print_slow(f"Keys Collected: {keys_collected}", color=YELLOW)
    if input("Do you want to play again? (y/n) ").lower() == 'y':
        introduction()
    else:
        print_slow("Thank you for playing", color=CYAN)
        exit()

def print_choices(options):
    for key, value in options.items():
        print_slow(f"{key}: {value}", color = CYAN)
    return get_user_choice("Choose: ", options.keys())

def get_user_choice(prompt, valid_choices, choice_type = str):
    while True:
        try:
            choice = choice_type(input(prompt))
            if choice in valid_choices:
                return choice
            else:
                print_slow("Invalid choice! Please select a valid option.", color=RED)
        except ValueError:
            print_slow("Invalid input! Please enter a valid choice.", color=RED)

def combat(enemy_name, player_health=100, enemy_health=100):
    global inventory
    print_slow(f"A wild {enemy_name} appears!", color=RED)

    while player_health > 0 and enemy_health > 0:
        print_slow(f"Your Health: {player_health} | {enemy_name}'s Health: {enemy_health}", color=YELLOW)

        options = {'1': "Attack", '2': "Dodge", '3': "Run"}
        choice = print_choices(options)

        if choice == '1':  # Attack
            if inventory["Sword"] == "✅ (Found)":
                damage = random.randint(20, 40)  # Stronger attack with a sword
            else:
                damage = random.randint(5, 20)  # Weaker attack

            enemy_health -= damage
            print_slow(f"You attack! {enemy_name} takes {damage} damage.", color=GREEN)

        elif choice == '2':  # Dodge
            success = random.choice([True, False])
            if success:
                print_slow(f"You dodge successfully!", color=CYAN)
            else:
                damage = random.randint(10, 25)
                player_health -= damage
                print_slow(f"You failed to dodge! {enemy_name} hits you for {damage} damage.", color=RED)

        elif choice == '3':  # Run
            success = random.choice([True, False])
            if success:
                print_slow("You escaped successfully!", color=CYAN)
                return
            else:
                print_slow("You failed to escape!", color=RED)

        if enemy_health > 0:
            damage = random.randint(10, 25)
            player_health -= damage
            print_slow(f"{enemy_name} attacks! You take {damage} damage.", color=RED)

    if player_health <= 0:
        game_over()
    else:
        print_slow(f"You defeated {enemy_name}!", color=GREEN)

def shadow_riddle():
    global days_left
    print_slow("A voice whispers from the darkness: 'Answer this riddle, and you may pass unharmed...'", color=MAGENTA)

    print_slow("""Riddle:  
        I am not alive, but I grow.  
        I don't have lungs, but I need air.  
        I don't have a mouth, but water kills me.  
        What am I?""", color=YELLOW)

    answer = get_user_choice("Your answer: ", ['fire'])

    if answer == "fire":
        print_slow("The darkness fades, and you feel lighter. You have escaped unharmed!", color=GREEN)
    else:
        print_slow("The darkness tightens around you... You feel your strength fading.", color=RED)
        print_slow("You struggle for hours before breaking free... You **lose 1 day**.", color=RED)
        days_left -= 1  # Player loses a day if they fail the riddle


def display_map_and_inventory():
    """Displays the updated map, inventory, and remaining days."""
    global days_left, keys_collected, inventory  # Use the global inventory

    # Track which locations have been visited
    visited = {
        "The Village": "🏠" if keys_collected == 0 else "✅",
        "Waterfall Isle": "🏠" if keys_collected == 1 else "✅" if keys_collected > 1 else "❌",
        "Island of Komoro": "🏠" if keys_collected == 2 else "✅" if keys_collected > 2 else "❌",
        "Island of Mystical Glows": "🏠" if keys_collected == 3 else "✅" if keys_collected > 3 else "❌",
        "Island of Echoes": "🏠" if keys_collected == 4 else "✅" if keys_collected > 4 else "❌",
        "Island of Shadows": "🏠" if keys_collected == 5 else "✅" if keys_collected > 5 else "❌"
    }

    print("\n" + "=" * 40)
    print("          🌍 MAP OVERVIEW")
    print("=" * 40)

    map_layout = f"""
           [{visited['The Village']} The Village] --- [{visited['Waterfall Isle']} Waterfall Isle] --- [{visited['Island of Komoro']} Island of Komoro]
                 |                   |                         |
           [{visited['Island of Mystical Glows']} Island of Mystical Glows] --- [{visited['Island of Echoes']} Island of Echoes] --- [{visited['Island of Shadows']} Island of Shadows]
    """
    print(map_layout)

    print("\n" + "=" * 40)
    print("          🎒 INVENTORY")
    print("=" * 40)


    for item, status in inventory.items():
        print(f"{item}: {status}")

    print("\n" + "=" * 40)
    print("       🕒 DAYS LEFT: ", days_left)
    print("=" * 40)

    print("       🗺️ LOCATION LEGEND")
    print("=" * 40)
    print("🏠 - Current Location")
    print("✅ - Visited")
    print("❌ - Not Yet Visited")
    print("🔑 - Key Collected")
    print("=" * 40 + "\n")



def introduction():
    print("Treasure Hunt: A Text-Based Adventure Game")
    print("Copyright © 2024 Astha Sharma. All Rights Reserved.")
    print("Unauthorized copying, modification, or distribution is prohibited.")
    print("--------------------------------------------------------------")

    narrative = [

        "Welcome to the game!",
        "It's the 4th of July night. While the country celebrates, you’re in your library, searching for a book with a hidden treasure map.",
        "The map points to islands in New Zealand, connected by a boat that leaves daily at 7 AM.",
        "You must find all 6 keys before a great tsunami hits the last island..."
    ]

    for line in narrative:
        print_slow(line, color=YELLOW)

    display_map_and_inventory()
    travel_options()

def travel_options():
    print_slow("Choose a way to travel", color=YELLOW)
    options = {'1': 'Borrow a private jet', '2': 'Take a commercial flight'}
    choice = print_choices(options)
    if choice == '1':
        private_jet()
    else:
        commercial_flight()

def private_jet():
    print_slow("You decide to borrow your friend's private jet. Suddenly, a strange noise shakes the jet.",
               color=YELLOW)
    options = {'g': 'Press Green Button', 'b': 'Press Blue Button'}
    choice = print_choices(options)
    
    if choice == 'g':
        game_over()
    elif choice == 'b':
        print_slow(
            "The jet stabilizes. It seems the 'Blue' button activated a backup system, preventing a potential disaster.",
            color=GREEN)
        print_slow("You safely land in New Zealand.", color=CYAN)
        
        clear_screen()
        first_chapter()  # Start Chapter 1
    else:
        print_slow("Invalid choice! Please select a valid option.", color=RED)
        private_jet()

def commercial_flight():
    print_slow("You took a commercial flight, arriving 3 hours late.", color=YELLOW)
    clear_screen()
    first_chapter()

def first_chapter():
    global days_left, keys_collected, inventory
    days_left -= 1
    check_days_left()

    print_section_border()
    print_slow("Chapter 1: The Journey Begins", color=BLUE)
    print_section_border()

    display_map_and_inventory()

    print_slow("Another choice comes your way!", color=CYAN)
    options = {'1': "Explore the forest", '2': "Visit the village"}
    choice = print_choices(options)

    if choice == '1':
        explore_forest()
    elif choice == '2':
        visit_local_village()

def explore_forest():
    global days_left, keys_collected, inventory
    print_slow("You venture into the dark forest, entranced by a strange sound coming from somewhere close. After hours, you meet a man sitting on a giant rock.", color=GREEN)
    options = {'1': 'Talk to the man', '2': 'Investigate the sound'}
    choice = print_choices(options)
    if choice == '1':
        man_on_rock()
    else:
        investigate_sound()

def investigate_sound():
    global keys_collected, days_left, inventory
    print_slow("You follow the mysterious sound deeper into the dense, aromatic forest.", color=YELLOW)
    print_slow("The sound leads you to a riddle inscribed on a stone altar.", color=MAGENTA)
    print_slow("""Beneath the canopy, where shadows play,
                     Seek the entrance to the hidden way.
                     Mossy stones or ancient tree,
                     Mark the path that sets keys free.""", color=CYAN)
    print_slow("Which path do you choose: Mossy stones or ancient tree?", color=WHITE)

    choice = {'1': 'for mossy stones', '2': 'for ancient tree'}
    choice = print_choices(choice)
    if choice == '1':
        print_slow("You get eaten by a giant lion.", color=RED)
        game_over()
    elif choice == '2':
        print_slow(
            "You find the cave entrance and retrieve the key from beneath a carved stone. Now, head to the shore to catch the boat to the next island.",
            color=GREEN)
        print_slow("Inside, you discover an old but sharp sword. This might be useful!", color=YELLOW)

        inventory["Sword"] = "✅ (Found)"
        keys_collected += 1
        inventory["Keys Collected"] += 1
        days_left -= 1
        print_slow(f"Keys collected: {keys_collected}", color=YELLOW)
        clear_screen()
        second_chapter()

def man_on_rock():
    global days_left, keys_collected
    print_slow(
        "The man says – Ah, what a strange fellow you are. Answer my riddle correctly and I will show you the path to the cave. Answer wrong and.....",
        color=MAGENTA)
    print_slow("""Here comes the riddle: 
                 Who makes it, has no need of it.
                 Who buys it, has no use for it.
                 Who uses it can neither see nor feel it.
                 What is it?""", color=CYAN)

    choice = get_user_choice("Answer: ", ['coffin', 'a coffin'])
    if choice in ['coffin', 'a coffin']:
        print_slow("Correct! Follow the path with ancient trees.", color=GREEN)
        
        keys_collected += 1
        inventory["Keys Collected"] += 1
        days_left -= 1
        print_slow(f"Keys collected: {keys_collected}", color=YELLOW)
        clear_screen()
        second_chapter()
    else:
        game_over()

def explore_nz():
    print_slow("The man says: 'Welcome, traveler. There’s an ancient cave nearby with historical significance. It’s worth exploring if you’re interested in local history.", color = BLUE)
    explore_forest()

def know_about_treasure_hunt():
    print_slow("The man grins and says: 'A treasure hunter? There's an old map rumored to lead to something valuable, but it’s a tough path. Not everyone succeeds.'", color = BLUE)
    explore_forest()

def visit_local_village():
    global inventory
    print_slow("A strange man approaches and asks, 'What brings you here?'", color = YELLOW)
    print_slow("The villager notices your confusion and hands you a small but sturdy compass.", color=CYAN)
    inventory["Compass"] = "✅ (Found)"
    options = {'1': "Ask about the area", '2': "Reveal you're on a treasure hunt"}
    choice = print_choices(options)
    if choice == '1':
        explore_nz()
    else:
        know_about_treasure_hunt()

def second_chapter():
    global days_left, keys_collected
    check_days_left()
    print_section_border()
    print_slow("Chapter 2: Waterfall Isle", color=BLUE)
    print_section_border()

    print_slow("You've successfully retrieved one key, but the adventure continues...", color=CYAN)

    display_map_and_inventory()

    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")

    print_slow("The map says that the next key is behind a waterfall, in a small hole. ", color=YELLOW)

    options = {'1': "Swim towards the waterfall", '2': "Go around it (adds 1 hour)"}
    choice = print_choices(options)

    if choice == '1':
        sea_demon()
    else:
        go_around()


def sea_demon():
    global keys_collected, days_left, inventory
    combat("Sea Demon")
    inventory["Magical Orb"] = "✅ (Found)"
    print_slow("The demon drops a magical orb. You take it.", color=YELLOW)
    inventory["Keys Collected"] += 1
    keys_collected += 1
    days_left -= 1

    clear_screen()
    third_chapter()


def go_around():
    global keys_collected, days_left
    print(
        "You found the key but you got lost and wasted 2 hours finding the correct way. You only have 1 hour to reach the boat.")
    keys_collected += 1
    inventory["Keys Collected"] += 1
    days_left -= 1
    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")
    clear_screen()
    third_chapter()

def third_chapter():
    global keys_collected, days_left
    check_days_left()
    print_section_border()
    print("Chapter 3: The lighthouse island.")
    print_section_border()

    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")
    
    display_map_and_inventory()

    print_slow("You stand by the waterfall, key in hand, with the boat departure time ticking away.",color=YELLOW)
    print_slow("A weathered sailor catches your eye.", color=YELLOW)

    options = {'1': "Talk to the Sailor", '2': "Board the Boat"}
    choice = print_choices(options)
    if choice == '1':
        talk_to_sailor()
    else:
        board_boat()


def talk_to_sailor():
    print_slow(
        """The sailor speaks: 'The island of Komoro was ravaged by war. 
        A volcanic eruption followed, engulfing the land. 
        Now, it is slowly recovering but has developed unique defense mechanisms.'""", color=BLUE)
    board_boat()  # Move to the next decision after talking to the sailor


def board_boat():
    print_slow("The boat sails towards the island. The map shows the key is hidden in the lighthouse.", color=BLUE)

    options = {'1': "Attempt to Sail Through", '2': "Change Course"}
    choice = print_choices(options)

    if choice == '1':
        attempt_to_sail_through()
    else:
        change_course()


def attempt_to_sail_through():
    print_slow("You skillfully maneuver the boat through the rocky waters, but you wasted time.", color=YELLOW)
    print_slow("You reach the lighthouse, but the time is running short!",color = YELLOW)

    explore_lighthouse_or_forest()


def change_course():
    print_slow("You changed the course and safely reached the lighthouse early. It's time to explore.", color=YELLOW)
    explore_lighthouse_or_forest()


def explore_lighthouse_or_forest():
    options = {'1': "Enter lighthouse", '2': "Explore the forest"}
    choice = print_choices(options)

    if choice == '1':
        enter_lighthouse()
    else:
        explore_dense_forest()


def enter_lighthouse():
    print_slow("The lighthouse reeks of something rotten. You stumble in the dark but find the stairs.", color = YELLOW)

    options = {'1': "Climb the stairs", '2': "Look for a source of light"}
    choice = print_choices(options)

    if choice == '1':
        climb_stairs()
    else:
        find_light()


def climb_stairs():
    print_slow("You climb the stairs in the dark and accidentally find a hidden passage!", color = YELLOW)
    secret_corridor()


def find_light():
    global inventory
    print_slow("You find a torch and light it. The stairs are now visible, revealing a hidden passage.", color = YELLOW)
    inventory["Torch"] = "✅ (Found)"
    secret_corridor()


def secret_corridor():
    print_slow("The corridor leads to a strange door with the inscription: 'Only the pure of heart shall pass.'", color = YELLOW)
    print_slow("You proceed and find the secret chamber where the third key is hidden.", color = YELLOW)
    retrieve_key()


def retrieve_key():
    print_slow("You take the third key from the pedestal and head back to the boat.",color = YELLOW)
    rush_back_to_boat()


def explore_dense_forest():
    print_slow("You venture into the dense forest, but strange noises make you uneasy.",color = YELLOW)

    options = {'1': "Investigate the noises", '2': "Return to the lighthouse"}
    choice = print_choices(options)

    if choice == '1':
        investigate_noises()
    else:
        return_to_lighthouse()


def investigate_noises():
    print_slow("You stumble upon a hidden animal den, but decide it's too risky and retreat.", color = YELLOW)
    return_to_lighthouse()


def return_to_lighthouse():
    print_slow("You return to the lighthouse, the sense of urgency pushing you forward.", color = YELLOW)
    explore_lighthouse_or_forest()


def rush_back_to_boat():
    global keys_collected, days_left
    print_slow("You make it back to the boat just in time, with the key in hand.", color = YELLOW)
    print_slow("The journey to the next island continues.", color = YELLOW)
    keys_collected += 1
    days_left -= 1
    print(f"Keys collected: {keys_collected}")
    clear_screen()
    fourth_chapter()

def fourth_chapter():
    global keys_collected, days_left
    check_days_left()
    print_section_border()
    print("Chapter 4: The Island of Mystical Glows")
    print_section_border()

    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")
    
    display_map_and_inventory()
    
    print_slow(
        "You arrive at the island, where bioluminescent plants light the jungle. The fourth key is hidden in an ancient temple.", color = BLUE)

    options = {'1': "Explore the Bioluminescent Jungle", '2': "Head to the Village"}
    choice = print_choices(options)

    if choice == '1':
        explore_jungle()
    else:
        head_to_village()

def explore_jungle():
    print_slow("You venture into the jungle, guided by glowing plants. Soon, you find an ancient stone path.", color = YELLOW)

    options = {'1': "Follow the Path", '2': "Blaze Your Own Trail"}
    choice = print_choices(options)

    if choice == '1':
        enter_temple()
    else:
        find_temple_after_detour()


def find_temple_after_detour():
    print_slow("After a tough detour, you finally find the temple hidden in the jungle.", color = BLUE)
    enter_temple()

def head_to_village():
    global inventory
    print_slow("At the village, an elderly villager shares a tale of the temple's guardian spirit.", color = WHITE)
    print_slow("She gives you a protective amulet.", color = WHITE)

    inventory["Amulet"] = "✅ (Found)"
    print_slow("The Amulet glows faintly. You feel safer already.", color=GREEN)

    options = {'1': "Ask More About the Temple", '2': "Head to the Temple"}
    choice = print_choices(options)

    if choice == '1':
        print("The villager warns that only the worthy can enter, but the amulet will protect you.")

    print_slow("You head to the temple.", color=YELLOW)  # Combine the steps to avoid redundancy
    enter_temple()

def enter_temple():
    print_slow("You enter the temple, its air thick with mystical energy. The fourth key rests on a pedestal.", color = BLUE)
    print_slow("A tremor shakes the temple as you take the key.", color = YELLOW)
    rush_back_to_chap4_boat()

def rush_back_to_chap4_boat():
    global keys_collected, days_left
    print_slow(
        "With the key secured, you rush through the glowing jungle to the boat. Dawn breaks, and you're just in time to board.", color = MAGENTA)
    print_slow("You have 24 hours to rest before the boat departs again.", color = MAGENTA)
    keys_collected += 1
    days_left -= 1
    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")
    clear_screen()
    fifth_chapter()

def fifth_chapter():
    global keys_collected, days_left
    check_days_left()
    print_section_border()
    print("Chapter 5: The Island of Echoes")
    print_section_border()
    
    display_map_and_inventory()
    
    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")

    print_slow(
        "You arrive at the fifth island as the sun sets. Known for its strange acoustics, every sound reverberates endlessly.", color = YELLOW)
    print_slow("The fifth key is said to be hidden in an ancient amphitheater at the center of the island.", color=YELLOW)

    options = {'1': "Head to the Amphitheater", '2': "Visit the Tavern for Information"}
    choice = print_choices(options)
    if choice == '1':
        amphitheater_path()
    else:
        tavern_path()


def amphitheater_path():
    global days_left

    print_slow("You head straight to the amphitheater. The sound of your footsteps echoes eerily in the air.",
               color=BLUE)

    if inventory["Compass"] == "✅ (Found)":
        print_slow("Thanks to your Compass, you easily navigate through the confusing echoes.", color=GREEN)
    else:
        print_slow("Without a Compass, you struggle to find the way as echoes distort your sense of direction!",
                   color=RED)
        print_slow("You lose 1 day trying to find the correct path.", color=RED)
        days_left -= 1  # Player loses 1 day

    print_slow("You finally reach the amphitheater, with its stone seats partially overgrown by vines.", color=BLUE)

    options = {'1': "Explore the Amphitheater", '2': "Look for Hidden Passages"}
    choice = print_choices(options)

    if choice == '1':
        explore_amphitheater()
    else:
        hidden_passage()


def tavern_path():
    print_slow("You visit the local tavern. The villagers warn you about the confusing acoustics of the amphitheater.", color = YELLOW)
    print_slow("One of them gives you a charm to help navigate the echoes.", color=YELLOW)

    options = {'1': "Thank the Villager and Head to the Amphitheater", '2': "Ask for a Guide"}
    choice = print_choices(options)

    if choice == '1':
        thank_villager()
    else:
        guide_path()


def explore_amphitheater():
    print_slow("The acoustics of the amphitheater amplify every sound. A faint whisper guides you to a hidden compartment.", color = BLUE)
    print_slow("Inside, you find the fifth key.", color = YELLOW)
    final_chapter()


def hidden_passage():
    print_slow(
        "You discover a hidden passage beneath the amphitheater. Following it, you find the key resting on a pedestal.", color = BLUE)
    final_chapter()


def thank_villager():
    print_slow("You thank the villager for the charm and head directly to the amphitheater.", color = YELLOW)
    print_slow("The charm helps you navigate the echoes, and you find the hidden compartment with the fifth key.", color = YELLOW)
    final_chapter()


def guide_path():
    print_slow(
        "A local agrees to guide you through the echoing paths. With their help, you avoid confusion and find the key in a hidden passage.", color = BLUE)
    final_chapter()


def final_chapter():
    global keys_collected, days_left
    print_slow("With the fifth key secured, you return to the boat, ready to sail toward the final island.", color = MAGENTA)
    keys_collected += 1
    days_left -= 1
    print(f"Keys collected: {keys_collected}")
    print_slow("The journey back is swift, and you're prepared for the final challenge ahead.", color = YELLOW)
    clear_screen()
    sixth_chapter()

def sixth_chapter():
    global keys_collected, days_left
    check_days_left()
    print_section_border()
    print("Chapter 6: The Final Showdown on the Island of Shadows")
    print_section_border()

    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")

    display_map_and_inventory()

    print_slow(
        "You step onto the final island. A heavy darkness fills the air, and an unnatural chill runs down your spine.",
        color=RED)

    if inventory["Amulet"] == "✅ (Found)":
        print_slow("Your Amulet glows softly, creating a protective barrier against the dark energy.", color=GREEN)
    else:
        print_slow("Without protection, the island's dark forces drain your energy.", color=RED)
        print_slow("You struggle to move and feel an unseen presence sapping your strength.", color=MAGENTA)
        print_slow("A mysterious whisper echoes in your mind: 'Only the worthy shall pass...'", color=YELLOW)

        # Give the player a chance to escape the trap instead of losing a day
        options = {'1': "Solve the Riddle", '2': "Attempt to Run Through the Darkness"}
        choice = print_choices(options)

        if choice == '1':
            shadow_riddle()  # Call the riddle challenge function
        else:
            print_slow("You attempt to run, but the shadows twist around you, slowing your movement.", color=RED)
            print_slow("It takes time to break free... You **lose 1 day**.", color=RED)
            days_left -= 1  # Player loses a day if they fail the side quest

    print_slow("The final key is hidden within the ruins ahead. Your journey is almost complete...", color=YELLOW)

    options = {'1': 'Enter the Cave', '2': 'Seek Help from the Spirits'}
    choice = print_choices(options)
    if choice == '1':
        enter_sixth_cave()
    else:
        seek_spirits()


def enter_sixth_cave():
    print_slow("You gather your courage and enter the dark cave. The air is cold, and the shadows seem to move around you.", color=MAGENTA)
    print_slow("You reach a large cavern, where the ancient guardian awaits, its eyes glowing in the dark.", color = MAGENTA)

    options = {'1': "Confront the Guardian", '2': "Try to Sneak Around"}
    choice = print_choices(options)

    if choice == '1':
        confront_guardian()
    else:
        print(
            "The guardian notices your attempt to sneak around and attacks. The battle is over before it begins. Game Over.")
        game_over()


def confront_guardian():
    print_slow("The Guardian of Shadows stands before you!", color=RED)
    combat("Ancient Guardian")
    print_slow("The guardian falls, revealing the final key!", color=GREEN)
    return_to_boat()


def seek_spirits():
    print_slow("You decide to visit the island's shrine first. The spirits bless you with protection and wisdom.", color = YELLOW)
    print_slow("Armed with their blessings, you feel more confident as you enter the cave.", color = YELLOW)

    options = {'1': "Enter the Cave with Blessings", '2': "Leave the island and Head Back to the Boat"}
    choice = print_choices(options)

    if choice == '1':
        enter_cave_with_blessings()
    else:
        print_slow("You decide to leave the island and head back to the boat. The treasure quest ends here.", color = RED)
        game_over()


def enter_cave_with_blessings():
    print_slow("With the spirits' blessings, the shadows part before you, and you easily reach the guardian.", color = MAGENTA)
    print_slow(
        "The guardian challenges you with the same riddle: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'", color = MAGENTA)

    correct_answer = "An echo"
    answer = input("Your answer: ").strip().lower()

    if answer == correct_answer:
        print_slow("The guardian nods and steps aside, revealing the final key. You take it and rush back to the boat.", color = BLUE)
        return_to_boat()
    else:
        print_slow("The guardian attacks, and despite your best efforts, you are overpowered. Game Over.", color = YELLOW)
        game_over()


def return_to_boat():
    global keys_collected, days_left
    print_slow("With all six keys in hand, you head back to the boat.", color = YELLOW)
    keys_collected += 1
    days_left -= 1
    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")
    print_slow(
        "The journey has been long and full of challenges, but you've overcome them all. The treasure awaits on the final island.", color = GREEN)
    clear_screen()
    seventh_chapter()

def seventh_chapter():
    global keys_collected, days_left
    check_days_left()
    print_section_border()
    print("Chapter 7: The Final Challenge and the Treasure")
    print_section_border()

    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")

    display_map_and_inventory()

    print_slow("You return to New York and head to the library where your journey began.", color = GREEN)

    options = {'1': "Return to the Library", '2': "Seek Guidance"}
    choice = print_choices(options)

    if choice == '1':
        return_to_library()
    else:
        seek_final_guidance()


def return_to_library():
    print_slow("At the library, you follow the final clue leading to a hidden chamber.", color = YELLOW)
    enter_hidden_chamber()


def seek_final_guidance():
    print_slow("The final riddle reads: \"Where knowledge sleeps, the key to wealth lies buried.\"", color = YELLOW)
    print_slow("This confirms that the library holds the secret entrance to the treasure chamber.", color = YELLOW)
    enter_hidden_chamber()


def enter_hidden_chamber():
    print_slow("You descend into a secret chamber where a chest with six keyholes awaits.", color = BLUE)

    options = {'1': "Insert the Keys", '2': "Examine the Chest"}
    choice = print_choices(options)

    if choice == '1':
        unlock_treasure()
    else:
        print_slow("After confirming no traps, you insert the keys and open the chest.", color = YELLOW)
        unlock_treasure()


def unlock_treasure():
    print_slow(
        "The chest clicks open, revealing gold, gems, and an ancient parchment with a map to an even greater treasure.", color=BLUE)
    final_challenge()


def final_challenge():
    print_slow("As you reach for the treasure, a guardian spirit appears, testing your worthiness.", color = MAGENTA)

    options = {'1': "Face the Guardian", '2': "Escape with the Treasure"}
    choice = print_choices(options)

    if choice == '1':
        answer_guardian_questions()
    else:
        escape_with_treasure()


def answer_guardian_questions():
    global keys_collected, days_left
    questions = [
        ("What is the most valuable treasure a person can possess?", "knowledge"),
        ("What is stronger than steel but can break with a word?", "trust"),
        ("What can travel around the world while staying in a corner?", "a stamp")
    ]

    for question, correct_answer in questions:
        answer = input(question + " ").strip().lower()
        if answer != correct_answer:
            print_slow("The guardian shakes its head. You have failed. Game Over.", color = RED)
            game_over()

    print_slow("The guardian nods in approval and vanishes, leaving you with the treasure.", color = RED)
    keys_collected += 1
    days_left -= 1
    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")
    end_game()


def escape_with_treasure():
    global keys_collected, days_left
    check_days_left()
    print_slow("You grab the treasure and run as the chamber collapses behind you. You barely escape in time!", color = GREEN)
    keys_collected += 1
    days_left -= 1
    print(f"Keys collected: {keys_collected}")
    print(f"Days left: {days_left}")
    end_game()


def end_game():
    print_slow(
        "You walk out of the library into the bustling streets of New York, treasure in hand, knowing your adventure is only beginning.", color = GREEN)
    print_slow("Congratulations! You have completed the treasure hunt.", color = GREEN)

introduction()
    


