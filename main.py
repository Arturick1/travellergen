import sys
from skills import skills, increase_skill, skill_check
from config import roll_1d6, roll_2d6

# This is my attempt to make a character generator without AI assistance.

# The following stats need to be accessed by just about everything, so they might as well be global.
stats = ['Strength', 'Dexterity', 'Endurance', 'Intelligence', 'Education', 'Social Standing']
physical_stats = stats[:3]
mental_stats = stats[3:]
values = {}
mods = {}
age = 18
careers = []
event_log = []
drafted = False
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
char_name = ""
qual_bonus = 0
benefit_bonus = 0
advance_bonus = 0
survive_bonus = 0
psionic_strength = 0

# This rolls character stats and assigns them.
def roll_stats():
    for stat in stats:
        values[stat] = roll_2d6()
    return values

# This calculates and updates the modifiers for stats.
def get_mods():
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
            print(f"Your {k} has dropped below 0!")
            print("You have died in character creation, a true Traveller experience.")
            print("ACHIEVEMENT UNLOCKED:  THIS IS TRAVELLER!!!")
            input("Press ENTER to exit.")
            sys.exit()

def update_char():
        mods.clear()
        get_mods()
        print_stats()
        check_death()
        return values    

# This lets the character join the draft.
def join_draft():
    global drafted
    drafted = True
    event_log.append(f"{char_name} signed up for the draft.")
    selection = roll_1d6()
    if selection == 1:
        print("In the Navy, you can live a life of ease...\n")
    elif selection == 2:
        print("You're in the Army now!")
    elif selection == 3:
        print("Praise the Lord and pass the ammuntion, Marine!")
    elif selection == 4:
        print("You've joined the Merchant Marine to experience boredom or torpedoes.")
    elif selection == 5:
        print("With the Scouts, you will boldly go where others are smart enough not to.")
    elif selection == 6:
        print("You are...  THE LAW!!!")
        
# This displays the stat section of the charactere sheet.
def print_stats():
    print(f"Strength: {values['Strength']}, Mod: {mods['Strength']}")
    print(f"Dexterity: {values['Dexterity']}, Mod: {mods['Dexterity']}")
    print(f"Endurance: {values['Endurance']}, Mod: {mods['Endurance']}")
    print(f"Intelligence: {values['Intelligence']}, Mod: {mods['Intelligence']}")
    print(f"Education: {values['Education']}, Mod: {mods['Education']}")
    print(f"Social Standing: {values['Social Standing']}, Mod: {mods['Social Standing']}")

# This checks for aging penalties and applies them.
def check_aging():
    if age < 34:
        return age
    age_penalty = roll_2d6 - len(careers)
    if age_penalty >= 1:
        return age
    print("\n\n\033[31mWARNING: Your character is beginning to incur age penalties!\033[0m\n\n")
    if age_penalty == 0:
        print("One of your physical characteristics is reduced by 1.")
        print("Choose:")
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = input("Your choice (1, 2, 3)?").strip()
        if choice == "1":
            values["Strength"] -= 1
        
        if choice == "2":
            values["Dexterity"] -= 1
        
        if choice == "3":
            values["Endurance"] -= 1

    if age_penalty == -1:
        print("Two of your physical characteristics are reduced by 2.")
        print("Choose first stat to lower:")
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = input("Your choice (1, 2, 3)?").strip()
        if choice == "1":
            values["Strength"] -= 1

        if choice == "2":
            values["Dexterity"] -= 1
               
        if choice == "3":
            values["Endurance"] -= 1

        print("Choose second stat to lower:")
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = input("Your choice (1, 2, 3)?").strip()
        if choice == "1":
            values["Strength"] -= 1
                  
        if choice == "2":
            values["Dexterity"] -= 1
               
        if choice == "3":
            values["Endurance"] -= 1

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
        choice = input("Your choice (1, 2, 3)?").strip()
        if choice == "1":
            values["Strength"] -= 1
                  
        if choice == "2":
            values["Dexterity"] -= 1
               
        if choice == "3":
            values["Endurance"] -= 1       
            
    if age_penalty == -4:
        print("Age hits you hard.  Two physical stats are reduced by two.  You get to pick which one is only reduced by one.")
        values["Strength"] -= 2
        values["Dexterity"] -= 2
        values["Endurance"] -= 2
        print("1 - Strength")
        print("2 - Dexterity")
        print("3 - Endurance")
        choice = input("Your choice (1, 2, 3)?").strip()
        if choice == "1":
            values["Strength"] += 1
                  
        if choice == "2":
            values["Dexterity"] += 1
               
        if choice == "3":
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
        choice = input("Your choice (1, 2, 3)?").strip()
        if choice == "1":
            values["Intelligence"] -= 1
                  
        if choice == "2":
            values["Education"] -= 1

               
        if choice == "3":
            values["Social Standing"] -= 1

        update_char()          

# Functions related to careers start here.
def injury():
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
        choice = int(input("(1, 2, 3)? "))

        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= penalty

        other_stats = [s for s in physical_stats if s != chosen_stat]

        print("How do you want to apply the remaining injury?")
        print(f"1. -2 to both {other_stats[0]} and {other_stats[1]}")
        print(f"2. -4 to one of them")
        option = int(input("(1 or 2)? "))

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
        choice = int(input("Choose: 1. Strength, 2. Dexterity, 3. Endurance)"))
        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= penalty

    if result == 3:
        print("Missing eye or limb.")
        event_log.append(f"{char_name} lost an eye or limb.")
        choice = int(input("Reduce 1. Strength, or 2. Dexterity, by two."))
        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= 2

    if result == 4:
        print("Scarred.  You are scarred and injured.  Reduce any one physical characteristic by two.")
        event_log.append(f"{char_name} was horribly scarred.")
        choice = int(input("Choose: 1. Strength, 2. Dexterity, 3. Endurance:"))
        chosen_stat = physical_stats[choice - 1]
        values[chosen_stat] -= 2

    if result == 5:
        print("Injured.  Reduce any physical characteristic by 1.")
        event_log.append(f"{char_name} was injured.")
        choice = int(input("Choose: 1. Strength, 2. Dexterity, 3. Endurance:"))    
        chosen_stat = physical_stats[choice - 1]  
        values[chosen_stat] -= 1    

    if result == 6:
        print("Lightly injured.  No permanent effect.")
        event_log.append(f"{char_name} was slightly injured.  Barely a scratch, really.")

    update_char()

def life_events():
    global contacts, allies, rivals, enemies, psionic_strength, qual_bonus, benefit_bonus
    print("\nYou experience random life events...\n")
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

# The actual function starts here...
def main():
    global char_name, stats, physical_stats, mental_stats, values, mods, age, careers, event_log, drafted, draft_options 
    global allies, enemies, contacts, rivals, qual_bonus, advance_bonus, survive_bonus, benefit_bonus, psionic_strength

    print("Traveller Character Creation Kit by William Drell\nFor Mongoose Traveller 1e\nRolling Stats...")
    roll_stats()
    get_mods()
    print_stats()

    while True:
        reroll = input("Would you like to reroll these stats?(y/n)\n").strip().lower()
        if reroll == "y":
            roll_stats()
            get_mods()
            print_stats()

        else:
            break     #Exits reroll loop.

    char_name = input("Name your character: ")

    draft_choice = input("So, would you like to enlist in the draft?(y/n)").strip().lower()
    if draft_choice == "y":
        join_draft()

    print(event_log)

if __name__ == "__main__":
    main()