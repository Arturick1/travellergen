import os
import sys
import config
from config import *
from careers import *

# This is my attempt to make a character generator without AI assistance.

# The actual function starts here...
def main():
    if sys.platform == "win32":
        os.system('color') 

    def homeworld_training():
        print("Choose an attribute of your homeworld that defined you.")
        num = 0
        trait_list = []
        skill_list = []
        for trait, skill in config.homeworld_skills.items():
            num += 1
            print(f"{num}. {trait}: {skill} (Current rank = {config.skills[skill]})")
            trait_list.append(trait)
            skill_list.append(skill)
        choice = safe_int_input("Your choice?\n>", (1, num))
        increase_skill(skill_list[choice - 1])
        config.homeworld_traits.append(trait_list[choice - 1])
        del config.homeworld_skills[trait_list[choice - 1]]

    def starting_skills():
        limit = 3 + config.mods["Education"]
        homeworld_training()
        limit -= 1
        if limit:
            choice = safe_int_input("Will you:\n1. Choose another Homeworld trait\n2. Pursue formal education\n>", (1, 2))
            if choice == 1:
                homeworld_training()
                limit -= 1
                if limit:
                    print("Your remaining education comes from the classroom.")
        while limit:
            limit -= 1
            num = 0
            skill_list = []
            for skill in config.education_skills:
                num += 1
                print(f"{num}. {skill} (Current rank = {config.skills[skill]})")
                skill_list.append(skill)
            choice = safe_int_input("Choose a skill to learn:\n>", (1, num))
            increase_skill(skill_list[choice - 1])
            config.education_skills.remove(skill_list[choice - 1])


    print("Traveller Character Creation Kit by William Drell\nFor Mongoose Traveller 1e\nRolling Stats...")
    roll_stats()
    get_mods()
    print_stats()

    while True:
        reroll = input("Would you like to reroll these stats?(y/n)\n>").strip().lower()
        if reroll == "y":
            roll_stats()
            get_mods()
            print_stats()

        else:
            break     #Exits reroll loop.

    name_char()
    config.basic_training = True
    starting_skills()

    draft_choice = safe_choice("So, would you like to enlist in the draft?(y/n)\n>", ["y", "n"])
    if draft_choice == "y":
        join_draft()

    else:
        attempt_career()

    print_event_log()

if __name__ == "__main__":
    main()