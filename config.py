import random
import sys
import os

# The following stats need to be accessed by just about everything, so they might as well be global.
stats = ['Strength', 'Dexterity', 'Endurance', 'Intelligence', 'Education', 'Social Standing']
physical_stats = stats[:3]
mental_stats = stats[3:]
values = {}
mods = {}
age = 18
careers = []
terms = 0
event_log = []
prior_careers = 0
drafted = False
previously_drafted = False
basic_training = True
draft_options = {
        "Navy" : 1,
        "Army" : 2,
        "Marines" : 3,
        "Merchant Marine" : 4,
        "Scouts" : 5,
        "Agent (Law Enforcement)" : 6
    }
allies = 0
enemies = 0
rivals = 0
contacts = 0
qual = False
qual_bonus = 0
benefit_bonus = []
advance_bonus = 0
advancement_tuple = ()
survive_bonus = 0
survival_tuple = ()
psionic_strength = 0
char_name = ""
starting_cash = 0
starting_items = []
ship_shares = 0
auto_advance = False
must_continue = False
not_ejected = False
keep_bonus = False
lose_all_benefits = False
drifter_terms = 0
drifter_rank = 0
agent_terms = 0
agent_rank = 0
army_terms = 0
army_rank = 0
army_nco_rank = 0
army_officer_rank = 0
citizen_terms = 0
citizen_rank = 0
entertainer_terms = 0
entertainer_rank = 0
marines_terms = 0
marines_rank = 0
marines_nco_rank = 0
marines_officer_rank = 0
merchants_terms = 0
merchants_rank = 0
navy_terms = 0
navy_rank = 0
navy_nco_rank = 0
navy_officer_rank = 0
rogue_terms = 0
rogue_rank = 0
rogue_auto_qualify = False
spec_name = None
spec_table = None

skills = {
    "Admin": None, 
    "Advocate": None,
    "Animals": None,
    "Athletics": None, 
    "Art": None, 
    "Astrogation": None, 
    "Battle Dress": None,
    "Broker": None, 
    "Carouse": None, 
    "Comms": None, 
    "Computers": None, 
    "Deception": None,
    "Diplomat": None,
    "Drive": None, 
    "Engineer": None, 
    "Explosives": None, 
    "Flyer": None, 
    "Gambler": None, 
    "Gunner": None, 
    "Gun Combat": None, 
    "Heavy Weapons": None, 
    "Investigate": None,
    "Jack of all Trades": None,
    "Language": None, 
    "Leadership": None,
    "Life Sciences": None, 
    "Mechanic": None, 
    "Medic": None, 
    "Melee": None,
    "Navigation": None,
    "Persuade": None, 
    "Pilot": None, 
    "Physical Sciences": None, 
    "Recon": None, 
    "Remote Operations": None, 
    "Seafarer": None, 
    "Sensors": None,
    "Social Sciences": None, 
    "Space Sciences": None, 
    "Stealth": None, 
    "Steward": None, 
    "Streetwise": None, 
    "Survival": None, 
    "Tactics": None, 
    "Trade": None, 
    "Vacc Suit": None, 
    "Zero-G": None
}


def name_char():
    global char_name
    while True:
        char_name = input("Name your character: ")
        choice = safe_choice("You sure about that name? y/n\n", ("y", "n"))
        if choice == "y":
            return char_name

def print_event_log():
    print("\nEvent Log:")
    for entry in event_log:
        print(entry)

def log_and_print(message):
    event_log.append(message)
    print(message)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def roll_2d6():
    return random.randint(1, 6) + random.randint(1, 6)

def roll_1d6():
    return random.randint(1, 6)

def roll_1d3():
    return random.randint(1, 3)

def roll_dd():
    return (roll_1d6() * 10) + roll_1d6()

# This rolls character stats and assigns them.
def roll_stats():
    for stat in stats:
        values[stat] = roll_2d6()
    return values

# This calculates and updates the modifiers for stats.
def get_mods():
    mods.clear()
    for mod in values:
        if values[mod] <= 2:
            mods[mod] = -2          
        elif values[mod] <= 5:
            mods[mod] = -1
        elif values[mod] <= 8:
            mods[mod] = 0
        elif values[mod] <= 11:
            mods[mod] = 1
        elif values[mod] <= 14:
            mods[mod] = 2
        else:
            mods[mod] = 3
    return mods

# This checks if the character has died.
def check_death():
    for k, v in values.items():
        if v <= 0:
            print(f"\033[31mYour {k} has dropped below 0!\033[0m")
            print("\033[31mYou have died in character creation, a true Traveller experience.\033[0m")
            print("ACHIEVEMENT UNLOCKED:  THIS IS TRAVELLER!!!")
            input("Press ENTER to exit.")
            sys.exit()

def update_char():
    mods.clear()
    get_mods()
    print_stats()
    check_death()
    input("\nPress ENTER to continue.")
    clear_screen()  

# This displays the stat section of the charactere sheet.
def print_stats():
    print(f"Strength: {values['Strength']}, Mod: {mods['Strength']}")
    print(f"Dexterity: {values['Dexterity']}, Mod: {mods['Dexterity']}")
    print(f"Endurance: {values['Endurance']}, Mod: {mods['Endurance']}")
    print(f"Intelligence: {values['Intelligence']}, Mod: {mods['Intelligence']}")
    print(f"Education: {values['Education']}, Mod: {mods['Education']}")
    print(f"Social Standing: {values['Social Standing']}, Mod: {mods['Social Standing']}")

# This checks for aging penalties and applies them.
def check_aging(debug=False):
    if age < 34:
        return age
    age_roll = roll_2d6()
    age_penalty = age_roll - terms
    if debug:
        age_penalty = safe_int_input("Test which age result?\n", (-6, 0))
    print(f"You roll {age_roll} and subract {terms} for an age penalty score of {age_penalty}.")
    if age_penalty >= 1:
        return age
    print("\n\n\033[31mWARNING: Your character is beginning to incur age penalties!\033[0m\n\n")
    if age_penalty == 0:
        print("One of your physical characteristics is reduced by 1.")
        print("Choose:")
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 3))
        if choice == 1:
            values["Strength"] -= 1
        
        if choice == 2:
            values["Dexterity"] -= 1
        
        if choice == 3:
            values["Endurance"] -= 1

    if age_penalty == -1:
        print("Two of your physical characteristics are reduced by 2.")
        print("Choose first stat to lower:")
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 3))
        if choice == 1:
            values["Strength"] -= 2
            print("Choose second stat to lower:")
            print("1 - Dexterity")
            print("2 - Endurance")
            choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 2))

            if choice == 1:
                values["Dexterity"] -= 2
               
            if choice == 2:
                values["Endurance"] -= 2

        elif choice == 2:
            values["Dexterity"] -= 2
            print("Choose second stat to lower:")
            print("1 - Strength")
            print("2 - Endurance")
            choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 2))

            if choice == 1:
                values["Strength"] -= 2
               
            if choice == 2:
                values["Endurance"] -= 2
               
        elif choice == 3:
            values["Endurance"] -= 2
            print("Choose second stat to lower:")
            print("1 - Strength")
            print("2 - Dexterity")
            choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 2))

            if choice == 1:
                values["Strength"] -= 2
               
            if choice == 2:
                values["Dexterity"] -= 2
               
    if age_penalty == -2:
        print("All of your physical stats have gone down by one.")
        values["Strength"] -= 1
        values["Dexterity"] -= 1
        values["Endurance"] -= 1

    if age_penalty == -3:
        print("All of your physical stats have gone down by one.  One of them goes down by two.  Maybe it's time to retire.")
        values["Strength"] -= 1
        values["Dexterity"] -= 1
        values["Endurance"] -= 1
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 3))
        if choice == 1:
            values["Strength"] -= 1
                  
        elif choice == 2:
            values["Dexterity"] -= 1
               
        elif choice == 3:
            values["Endurance"] -= 1       
            
    if age_penalty == -4:
        print("Age hits you hard.  Two physical stats are reduced by two.  You get to pick which one is only reduced by one.")
        values["Strength"] -= 2
        values["Dexterity"] -= 2
        values["Endurance"] -= 2
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 3))
        if choice == 1:
            values["Strength"] += 1
                  
        if choice == 2:
            values["Dexterity"] += 1
               
        if choice == 3:
            values["Endurance"] += 1

    if age_penalty == -5:
        print("Your health declines catastrophically.  All physical stats are reduced by two.")
        values["Strength"] -= 2
        values["Dexterity"] -= 2
        values["Endurance"] -= 2

    if age_penalty <= -6:
        print("Oh, joy.  Your body is wrecked AND your mind is failing.  All physical stats are reduced by two.")
        print("Additionally, one mental stat is reduced by one.")
        values["Strength"] -= 2
        values["Dexterity"] -= 2
        values["Endurance"] -= 2
        print("1 - Intelligence")
        print("2 - Education")
        print("3 - Social Standing (People don't want to stand next to your loaded adult diaper)")
        choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 3))
        if choice == 1:
            values["Intelligence"] -= 1
                  
        if choice == 2:
            values["Education"] -= 1

               
        if choice == 3:
            values["Social Standing"] -= 1
    mods.clear()
    get_mods()        

# Functions related to careers start here.

def injury_roll_twice():
    roll1 = roll_1d6()
    roll2 = roll_1d6()
    if roll1 < roll2:
        injury(roll1)
    else:
        injury(roll2)

def injury(forced_roll=None):
    global char_name
    if forced_roll:
        result = forced_roll
    else:
        result = roll_1d6()
    print("\n\n\033[31mWARNING: Your character has sustained an injury!\033[0m\n\n")
    if result == 1:
        penalty = roll_1d6()
        event_log.append(f"{char_name} was nearly killed and suffered lasting injuries.")
        print("Nearly killed. Reduce one physical characteristic by 1d6,")
        print("reduce both other physical characteristics by 2 (or one by 4).")

        print("Choose a stat to reduce by 1d6:")
        for i, stat in enumerate(physical_stats, start=1):
            print(f"{i}. {stat}")
        choice = safe_int_input("Your choice (1, 2, 3)?\n", (1, 3))

        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= penalty

        other_stats = [s for s in physical_stats if s != chosen_stat]

        print("How do you want to apply the remaining injury?")
        print(f"1. -2 to both {other_stats[0]} and {other_stats[1]}")
        print(f"2. -4 to one of them")
        option = safe_int_input("Your choice (1, 2, 3)?\n", (1, 2))

        if option == 1:
            for s in other_stats:
                values[s] -= 2
        else:
            print("Which stat takes -4?")
            for i, stat in enumerate(other_stats, start=1):
                print(f"{i}. {stat}")
            sub_choice = int(input("(1 or 2)? "))
            values[other_stats[sub_choice - 1]] -= 4

    if result == 2:
        penalty = roll_1d6()
        print("Severely injured.  Reduce one physical characteristic by 1d6.")
        event_log.append(f"{char_name} received a severe injury.")
        choice = safe_int_input("Choose: 1. Strength, 2. Dexterity, 3. Endurance)", (1, 3))
        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= penalty

    if result == 3:
        print("Missing eye or limb.")
        event_log.append(f"{char_name} lost an eye or limb.")
        choice = safe_int_input("Reduce 1. Strength, or 2. Dexterity, by two.", (1, 2))
        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= 2

    if result == 4:
        print("Scarred.  You are scarred and injured.  Reduce any one physical characteristic by two.")
        event_log.append(f"{char_name} was horribly scarred.")
        choice = safe_int_input("Choose: 1. Strength, 2. Dexterity, 3. Endurance:", (1, 3))
        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= 2

    if result == 5:
        print("Injured.  Reduce any physical characteristic by 1.")
        event_log.append(f"{char_name} was injured.")
        choice = safe_int_input("Choose: 1. Strength, 2. Dexterity, 3. Endurance:", (1, 3))  
        chosen_stat = physical_stats[choice - 1]  
        values[chosen_stat] -= 1    

    if result == 6:
        print("Lightly injured.  No permanent effect.")
        event_log.append(f"{char_name} was slightly injured.  Barely a scratch, really.")

    update_char()

def life_events(forced_roll=None):
    global contacts, allies, rivals, enemies, psionic_strength, qual_bonus, benefit_bonus, char_name
    print("\nYou experience random life events...\n")
    if forced_roll:
        event = forced_roll
    else:
        event = roll_2d6()
    if event == 2:
        print("You experience a severe sickness or injury!")
        event_log.append(f"{char_name} became seriously ill or injured.")
        injury()

    if event == 3:
        print("There was a birth or death in the family.")
        event_log.append(f"{char_name} experienced a birth or death in the family.")

    if event == 4:
        print("A romantic relationship ended in tears, accusations, drunk-dialing, and general awfulness.")
        event_log.append(f"{char_name} had a romantic relationship end poorly.")

    if event == 5:
        print("A romantic relationship improved, perhaps involving wedding bells.")
        event_log.append(f"{char_name} had a deepening romantic relationship and possibly marriage, hopefully to the same person.")

    if event == 6:
        print("You gain a new romantic partner.  You probably like them.")
        event_log.append(f"{char_name} experienced new love.")

    if event == 7:
        print("\nYou have gained a new contact.")
        event_log.append(f"{char_name} gained a new contact.")
        contacts += 1

    if event == 8:
        print("\n\n\033[31mBETRAYAL!!!\033[0m\n\n")
        contact_or_ally = roll_1d6()
        rival_or_enemy = roll_1d6()
        if contact_or_ally < 4 and contacts > 0:
            contacts -= 1
            if rival_or_enemy < 4:
                rivals += 1
                print("\nOne of your contacts has become a rival!")
                event_log.append(f"One of {char_name}'s contacts became a rival.")
            if rival_or_enemy >= 4:
                enemies += 1
                print("\nOne of your contacts has become a sworn enemy, out for your credits, blood, credits, dignity, and credits.")
                event_log.append(f"One of {char_name}'s contacts became an enemy!")
        elif contact_or_ally >= 4 and allies > 0:
            allies -= 1
            if rival_or_enemy < 4:
                rivals += 1
                print("\nOne of your allies, someone you would've let petsit your flargbeast, has become a rival!")
                event_log.append(f"One of {char_name}'s allies became a rival.")
            if rival_or_enemy >= 4:
                enemies += 1
                print("\nOne of your allies has become a sworn enemy, out for your credits, blood, credits, dignity, and credits.")
                event_log.append(f"One of {char_name}'s contacts became an enemy!")
        else:
            if rival_or_enemy < 4:
                rivals += 1
                print("\nSomeone has appointed themselves your rival.")
                event_log.append(f"{char_name} gained a rival.")
            if rival_or_enemy >= 4:
                enemies += 1
                print("\nSomeone is hunting you like you killed their puppy.  We're going to assume you didn't.")
                event_log.append(f"{char_name} gained a deadly enemy!")

    if event == 9:
        print("\nYou resettle on a new world and make contacts that would ease any change in careers.")
        event_log.append(f"{char_name} moved to new world.")
        qual_bonus += 2

    if event == 10:
        print("\nYou have good luck coming your way.  The cookie says so.  (+2 to a Benefit roll in the future)")
        event_log.append(f"{char_name} had a stroke... of good luck!")
        benefit_bonus += 2

    if event == 11:
        print("\nYou have been accused of a crime.  This may be because you committed a crime.  We don't judge.")
        print("Your Social Standing has been decreased by one to match your newly sinister reputation.")
        event_log.append(f"{char_name} was accused of a dastardly crime.")
        values["Social Standing"] -= 1

    if event == 12:
        unusual = roll_1d6()
        if unusual == 1:
            print("\nA man and a small green creature in brown robes approach you.")
            print("The man says he senses potential in you, but the green thing insists you are too old.")
            psionic_strength = roll_2d6() - len(careers)
            if psionic_strength > 0:
                print(f"The man says, he has a psi potential of {psionic_strength}.  He should seek us out later.  The green thing grumbles.")
                event_log.append(f"{char_name} was tested for psi potential and scored a {psionic_strength}.")
            else:
                print('The green thing yells "TOO OLD!" and the two of them walk off.')
                event_log.append(f"{char_name} was approached by probably dangerous cultists who fortunately left.")

        if unusual == 2:
            print("You spend some time associating with aliens and learning their ways.  You get a friendly alien contact.")
            event_log.append(f"{char_name} spent time among an alien race.")
            contacts += 1
            increase_skill("Life Sciences")

        if unusual == 3:
            print("You obtain an alien artifact of uncertain purpose or importance.")
            event_log.append(f"{char_name} obtained an alien artifact.")

        if unusual == 4:
            print("\nWhat happened?  You don't remember.  Something happened, but what?")
            event_log.append(f"{char_name} suffered a bout of amnesia.")

        if unusual == 5:
            print("You had a brief, but seemingly significant encounter with a highly placed official. He had a lot of titles.")
            event_log.append(f"{char_name} had an encounter with a powerful government official.")

        if unusual == 6:
            print("\nYou found something that you probably shouldn't tell anyone about.  It might be older than humanity.")
            event_log.append(f"{char_name} obtained a truly ancient artifact of uncertain purpose.")

    update_char()
    input("Press ENTER to continue.")

def increase_stat(stat_name, amount=1):
    if stat_name in values:
        old = values[stat_name]
        values[stat_name] += amount
        print(f"\033[32m{stat_name} improved from {old} to {values[stat_name]}\033[0m")
        event_log.append(f"{stat_name} improved from {old} to {values[stat_name]}")
        get_mods()
    else:
        print(f"Error: No stat named '{stat_name}'")


def increase_skill(skill, set_rank=None):
    if basic_training:
        skills[skill] = 0
        print(f"\033[32mYou gain basic proficiency in {skill}.\033[0m")
        event_log.append(f"You gained basic proficiency in {skill}.")
        
    elif set_rank is not None and not skills[skill]:
        skills[skill] = set_rank
        print(f"\033[32mYou gain {skill} at rank {set_rank}.\033[0m")
        event_log.append(f"You gained {skill} at rank {set_rank}.")

    elif set_rank is not None and skills[skill] >= 1:
        print(f"You receive training in {skills[skill]} but it doesn't add anything of value.")
    
    elif skills[skill] == None:
        skills[skill] = 0
        print(f"\033[32mYou gained base proficiency in {skill}.\033[0m")
        event_log.append(f"You gained base proficiency in {skill}.")

    else:
        skills[skill] += 1
        print(f"\033[32mYour skill in {skill} increased by one.\033[0m")
        event_log.append(f"Your skill in {skill} increased by one.")

    return skills

def increase_any_skill(setrank=None):
    number = 0
    skill_list = []
    if setrank is not None:
        for skill, value in skills.items():
            if not value:
                number += 1
                print(f"{number}: {skill}: {value}")
                skill_list.append(skill)
    for skill, value in skills.items():
        number += 1
        print(f"{number}: {skill}: {value}")
        skill_list.append(skill)
    if not setrank:
        choice = safe_int_input("Choose which skill, by number, to improve:\n", (1, number))
    else:
        choice = safe_int_input(f"Choose which skill, by number, to gain at Rank {setrank}:\n", (1, number))
    increase_skill(skill_list[choice - 1], setrank)

def increase_existing_skill():
    print("You may improve a skill you already have.")
    number = 0
    skill_list = []
    for skill, value in skills.items():
        if value is not None:
            number += 1
            print(f"{number}: {skill}: {value}")
            skill_list.append(skill)
    choice = safe_int_input("Choose which skill, by number, to improve:\n", (1, number))
    increase_skill(skill_list[choice - 1])

def skill_check(skill, mod):
    skill_bonus = 0
    skill_result = 0
    rolled = roll_2d6()
    stat_bonus = mods[mod]
    if skills[skill] == None:
        skill_bonus -= 3
        if skills["Jack of all Trades"] is not None:
            if skills["Jack of all Trades"] > 0 and skills["Jack of all Trades"] < 3:
                skill_bonus += skills["Jack of all Trades"]
            elif skills["Jack of all Trades"] >= 3:
                skill_bonus += 3
        print(f"Adding {skill} skill bonus of {skill_bonus}, {mod} bonus of {stat_bonus}, and dice roll of {rolled}")
        skill_result += skill_bonus + stat_bonus + rolled
        return skill_result
    skill_bonus += skills[skill]
    print(f"Adding {skill} skill bonus of {skill_bonus}, {mod} bonus of {stat_bonus}, and dice roll of {rolled}")
    skill_result += skill_bonus + stat_bonus + rolled
    return skill_result    

def safe_int_input(prompt, valid_range=None):
    """
    Ask for an integer, keep asking until valid.
    valid_range can be a tuple like (1, 3) or None (any int allowed).
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if valid_range is None or valid_range[0] <= value <= valid_range[1]:
                return value
            else:
                print(f"Please enter a number between {valid_range[0]} and {valid_range[1]}.")
        except ValueError:
            print("That's not a valid number. Please enter a number.")

def safe_choice(prompt, options, error_msg="Invalid choice. Try again."):
    while True:
        try:
            value = input(prompt).strip().lower()
            if value in options:
                return value
            print(error_msg)
        except ValueError:
            print(error_msg)

def weapon_benefit(type="Weapon"):
    if type == "Weapon":
        if "Weapon" in starting_items:
            skillup = safe_int_input("You get some practice time with your previously awarded weapon.\n"
                    "Will that be:\n1. Sparring with a melee weapon\n2. Range time with a firearm\n", (1, 2))
            if skillup == 1:
                increase_skill("Melee")
            else:
                increase_skill("Gun Combat")
        else:
            log_and_print("You got a weapon.")
            starting_items.append("Weapon")
    elif type == "Blade":
        if "Blade" in starting_items:
            increase_skill("Melee")
        else:
            log_and_print("You gain a Blade.")
            starting_items.append("Blade")
    elif type == "Gun":
        if "Gun" in starting_items:
            increase_skill("Gun Combat")
        else:
            log_and_print("You gain a Gun.")
            starting_items.append("Gun")


def armour_benefit():
    if "Armour" in starting_items:
        skillup = safe_int_input("You get some practice time with your previously awarded armour.\n"
                "Will that be:\n1. Careful maneuvers in a Vacc Suit\n2. Laughing and stomping through live fire in Battle Dress\n", (1, 2))
        if skillup == 1:
            increase_skill("Vacc Suit")
        else:
            increase_skill("Battle Dress")
    else:
        log_and_print("You received a suit of armour.")
        starting_items.append("Armour")

def best_mental():
    best = None
    highest = float('-inf')
    for stat in mental_stats:
        if mods[stat] > highest:
            best = stat
            highest = mods[stat]
    return best

def best_physical():
    best = None
    highest = float('-inf')
    for stat in physical_stats:
        if mods[stat] > highest:
            best = stat
            highest = mods[stat]
    return best

def best_of_two(stat1, stat2):
    best = stat1
    if mods[stat2] > mods [stat1]:
        best = stat2
    return best

def choose_science_skill():
    print("Choose which Science skill to improve:")
    print("1. Physical Sciences")
    print("2. Life Sciences")
    print("3. Social Sciences")
    print("4. Space Sciences")
    
    choice = safe_int_input("1–4? ", (1, 4))
    science_skills = [
        "Physical Sciences",
        "Life Sciences",
        "Social Sciences",
        "Space Sciences"
    ]
    selected = science_skills[choice - 1]
    increase_skill(selected)
    event_log.append(f"Increased {selected} via Science (any)")

def tas_member():
    if "TAS Membership" in starting_items:
        log_and_print("You gain 2 Ship Shares.")
        ship_shares += 2
    else:
        log_and_print("You are invited to join the Traveller's Aid Society")
        starting_items.append("TAS Membership")

def retire():
    update_char()
    print_event_log()
    sys.exit()