import sys
import config
from config import *
from careers import *

# This is my attempt to make a character generator without AI assistance.

# The actual function starts here...
def main():

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

    name_char()

    draft_choice = safe_choice("So, would you like to enlist in the draft?(y/n)", ["y", "n"])
    if draft_choice == "y":
        join_draft()

    else:
        attempt_career()

    print_event_log()

if __name__ == "__main__":
    main()