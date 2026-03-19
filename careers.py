import config
from config import *
import random
import sys
import math


career_funcs = {
    "Agent": lambda: car_agent(),
    "Army": lambda: car_army(),
    "Citizen": lambda: car_citizen(),
    "Drifter": lambda: car_drifter(),
    "Entertainer": lambda: car_entertainer(),
    "Marines": lambda: car_marines(),
    "Merchants": lambda: car_merchants(),
    "Navy": lambda: car_navy(),
    "Nobility": lambda: car_nobility(),
    "Rogue": lambda: car_rogue(),
    "Scholar": lambda: car_scholar(),
    "Scout": lambda: car_scout(),
}

available_careers = [
    "Agent",
    "Army",
    "Citizen",
    "Drifter",
    "Entertainer",
    "Marines",
    "Merchants",
    "Navy",
    "Nobility",
    "Rogue",
    "Scholar",
    "Scout",
]

#Citizen tables moved outside of career for Agent event.

CITIZEN_PERSONAL_DEVELOPMENT = {
    1: lambda: increase_stat("Education"),
    2: lambda: increase_stat("Intelligence"),
    3: lambda: increase_skill("Carouse"),
    4: lambda: increase_skill("Gambler"),
    5: lambda: increase_skill("Drive"),
    6: lambda: increase_skill("Jack of all Trades")
}

CITIZEN_SERVICE_SKILLS = {
    1: lambda: increase_skill("Drive"),
    2: lambda: increase_skill("Flyer"),
    3: lambda: increase_skill("Streetwise"),
    4: lambda: increase_skill("Melee"),
    5: lambda: increase_skill("Steward"),
    6: lambda: increase_skill("Trade"),
}

CITIZEN_ADVANCED_EDUCATION = {
    1: lambda: increase_skill("Art"),
    2: lambda: increase_skill("Advocate"),
    3: lambda: increase_skill("Diplomat"),
    4: lambda: increase_skill("Language"),
    5: lambda: increase_skill("Computers"),
    6: lambda: increase_skill("Medic"),
}   

CITIZEN_CORPORATE = {
    1: lambda: increase_skill("Advocate"),
    2: lambda: increase_skill("Admin"),
    3: lambda: increase_skill("Broker"),
    4: lambda: increase_skill("Computers"),
    5: lambda: increase_skill("Diplomat"),
    6: lambda: increase_skill("Leadership"),
}

CITIZEN_WORKER = {
    1: lambda: increase_skill("Drive"),
    2: lambda: increase_skill("Mechanic"),
    3: lambda: increase_skill("Trade"),
    4: lambda: increase_skill("Engineer"),
    5: lambda: increase_skill("Trade"),
    6: lambda: choose_science_skill(),
}

CITIZEN_COLONIST = {
    1: lambda: increase_skill("Animals"),
    2: lambda: increase_skill("Athletics"),
    3: lambda: increase_skill("Jack of all Trades"),
    4: lambda: increase_skill("Drive"),
    5: lambda: increase_skill("Survival"),
    6: lambda: increase_skill("Recon"),
}

CITIZEN_MUSTER_CASH = {
    1: 1000,
    2: 5000,
    3: 10000,
    4: 10000,
    5: 10000,
    6: 50000,
    7: 100000,
}    

def citizen_mishap():
    print("You have suffered a severe mishap.")
    if not config.agent_undercover:
        available_careers.remove("Citizen")
    roll = roll_1d6()
    if roll == 1:
        log_and_print("Injured on the job.")
        injury()

    elif roll == 2:
        log_and_print("You are harassed and your life is ruined by a criminal gang that you now consider an enemy.")
        config.enemies += 1

    elif roll == 3:
        log_and_print("Hard times caused by a lack of interstellar trade cost you your job.  Lose one Social Standing.")
        config.values["Social Standing"] -= 1
        update_char()

    elif roll == 4:
        log_and_print("Your business is investigated and shut down.")
        print("\nCooperate with the investigation and you will receive +2 to your next Qualification check.")
        print("Refuse to cooperate and you will gain an Ally.")
        choice = safe_int_input("Will you:\n1. Cooperate\n2. Refuse", (1, 2))
        if choice == 1:
            log_and_print("You cooperate with the investigators and get a recommendation for a job.")
            config.qual_bonus += 2
        elif choice == 2:
            log_and_print("You refuse to cooperate and a former business associate owes you big for your discretion.")
            config.allies += 1

    elif roll == 5:
        log_and_print("A revolution, attack, or other chaos forces you to leave the planet and turn your life upside down.")
        if skill_check("Streetwise", best_mental()):
            print("Hardship is a great teacher.  Increase any one skill you know.")
            print("Current skills (level 0+ only shown):")
            number = 0
            skill_list = []
            for skill, value in config.skills.items():
                if value is not None:
                    number += 1
                    print(f"{number}: {skill}: {value}")
                    skill_list.append(skill)
            choice = safe_int_input("Choose which skill, by number, to increase:\n", (1, number))
            increase_skill(skill_list[choice - 1])

    else:
        log_and_print("One of your coworkers develops a hatred of you and sabotages your life.  You gain a Rival.")
        config.rivals += 1

 

def citizen_events():
    roll = roll_2d6()
    if roll == 2:
        config.not_ejected = True     
        log_and_print("Disaster!  You have a mishap, but your career will survive.")
        citizen_mishap()
    elif roll == 3:
        log_and_print("Political upheaval strikes your homeworld, and you are caught up in the revolution.")
        print("Gain one of the following skills at rank 1:\n1. Advocate\n2. Persuade\n3.Explosives\n4. Streetwise\n")
        choice = safe_int_input("Your pick? (1-4)\n", (1, 4))
        result = 0
        if choice == 1:
            increase_skill("Advocate", set_rank=1)
            result = skill_check("Advocate", best_mental())
        elif choice == 2:
            increase_skill("Persuade", set_rank=1)
            result = skill_check("Persuade", best_mental())
        elif choice == 3:
            increase_skill("Explosives")
            result = skill_check("Explosives", best_of_two("Dexterity", "Intelligence"))
        else:
            increase_skill("Streetwise", set_rank=1)
            result = skill_check("Streetwise", best_mental())
        if result >= 8:
            log_and_print("You joined the right side and gained prestige.")
            config.advance_bonus += 2
        else:
            log_and_print("You picked the losing side and struggle to survive under the new order.")
            config.survive_bonus -= 2

    elif roll == 4:
        log_and_print("You spend time maintaining and using heavy vehicles, either as a job or a hobby.")
        choice = safe_int_input("Increase one of the following skills:\n1. Mechanic\n2. Drive\n3. Flyer\n4. Engineer", (1, 4))
        if choice == 1:
            increase_skill("Mechanic")
        elif choice == 2:
            increase_skill("Drive")
        elif choice == 3:
            increase_skill("Flyer")
        else:
            increase_skill("Engineer")

    elif roll == 5:
        log_and_print("Your business expands, your corporation grows, or your colony thrives.")
        config.benefit_bonus.append(1)

    elif roll == 6:
        log_and_print("You are given advanced training in a specialized field.")
        learning = roll_2d6() + config.mods["Education"]
        if learning < 10:
            log_and_print("The education doesn't really stick, but the teacher was very attractive.")
        else:
            print("You're an excellent student.  Gain any skill at Rank 1.")
            increase_any_skill(1)

    elif roll == 7:
        life_events()

    elif roll == 8:
        log_and_print("You learn something you shouldn't have -- a corporate secret, a political scandal...")
        print("If you choose to illegally profit from this info, you will gain several benefits:\n"
                "+1 DM to a Benefit Roll and Streetwise 1, Deception 1, or a Criminal Contact.")
        yes_no = safe_choice("Do you utilize this secret knowledge? (y/n)\n", ("y", "n"))
        if yes_no == "y":
            config.benefit_bonus.append(1)
            log_and_print("You're evidently not above blackmail.")
            choice = safe_int_input("Choose your benefit:\n1. Streetwise 1\n2. Deception 1\n3. Criminal Contact\n", (1, 3))
            if choice == 1:
                increase_skill("Streetwise", set_rank=1)
            elif choice == 2:
                increase_skill("Deception", set_rank=1)
            else:
                log_and_print("You gain a friend in the underworld.")
                config.contacts += 1
        else:
            log_and_print("You conduct yourself honorably; keeping your head high even if your funds are low.")

    elif roll == 9:
        log_and_print("You are rewarded for your diligence or cunning... or kneepads.")
        config.advance_bonus += 2

    elif roll == 10:
        log_and_print("You gain experience as a computer operator or survey technician.")
        skill_list = ["Comms", "Computers", "Engineer", "Sensors"]
        choice = safe_int_input("Increase one of the following skills:\n"
        "1. Comms\n2. Computers\n3. Engineer\n4. Sensors\n", (1, 4))
        increase_skill(skill_list[choice - 1])
    
    elif roll == 11:
        log_and_print("You befriend a superior in the corporation or colony.")
        config.allies += 1
        choice = safe_int_input("Choose either:\n1. Gain Diplomat 1\n2. +4 DM to your next Advancement roll\n", (1, 2))
        if choice == 1:
            increase_skill("Diplomat", set_rank=1)
        else:
            config.advance_bonus += 4

    else:
        log_and_print("You rise to a position of power in your colony or corporation.  You are automatically promoted.")
        config.auto_advance = True

#Rogue tables moved outside the function due to Agent event.

ROGUE_PERSONAL_DEVELOPMENT = {
    1: lambda: increase_skill("Carouse"),
    2: lambda: increase_stat("Dexterity"),
    3: lambda: increase_stat("Endurance"),
    4: lambda: increase_skill("Gambler"),
    5: lambda: increase_skill("Melee"),
    6: lambda: increase_skill("Gun Combat")
}

ROGUE_SERVICE_SKILLS = {
    1: lambda: increase_skill("Deception"),
    2: lambda: increase_skill("Recon"),
    3: lambda: increase_skill("Athletics"),
    4: lambda: increase_skill("Gun Combat"),
    5: lambda: increase_skill("Stealth"),
    6: lambda: increase_skill("Streetwise"),
}

ROGUE_ADVANCED_EDUCATION = {
    1: lambda: increase_skill("Computers"),
    2: lambda: increase_skill("Comms"),
    3: lambda: increase_skill("Medic"),
    4: lambda: increase_skill("Investigate"),
    5: lambda: increase_skill("Persuade"),
    6: lambda: increase_skill("Advocate"),
}   

ROGUE_THIEF = {
    1: lambda: increase_skill("Stealth"),
    2: lambda: increase_skill("Computers"),
    3: lambda: increase_skill("Remote Operations"),
    4: lambda: increase_skill("Streetwise"),
    5: lambda: increase_skill("Deception"),
    6: lambda: increase_skill("Athletics"),
}

ROGUE_ENFORCER = {
    1: lambda: increase_skill("Gun Combat"),
    2: lambda: increase_skill("Melee"),
    3: lambda: increase_skill("Streetwise"),
    4: lambda: increase_skill("Persuade"),
    5: lambda: increase_skill("Athletics"),
    6: lambda: increase_skill("Drive"),
}

ROGUE_PIRATE = {
    1: lambda: increase_skill("Pilot"),
    2: lambda: increase_skill("Astrogation"),
    3: lambda: increase_skill("Gunner"),
    4: lambda: increase_skill("Engineer"),
    5: lambda: increase_skill("Vacc Suit"),
    6: lambda: increase_skill("Melee"),
}

ROGUE_MUSTER_CASH = {
    1: 0,
    2: 0,
    3: 10000,
    4: 10000,
    5: 50000,
    6: 100000,
    7: 100000,
}    

def rogue_mishap():
    print("You have suffered a severe mishap.")
    if not config.agent_undercover:
        available_careers.remove("Rogue")
    roll = roll_1d6()
    if roll == 1:
        log_and_print("Severely injured.")
        choice = safe_int_input("Choose:\n1. A roll of '2' on the injury table\n2. Roll twice and take the lower result\n", (1, 2))
        if choice == 1:
            injury(2)
        else:
            injury_roll_twice()

    elif roll == 2:
        log_and_print("Arrested. Lose one Benefit from this career and you must take the draft in your next career.")
        config.rogue_terms -= 1
        config.forced_drafted = True

    elif roll == 3:
        life_events(8)

    elif roll == 4:
        log_and_print("A job goes wrong, forcing you to flee off-planet.")
        skill_list = ["Deception", "Pilot", "Zero-G", "Gunner"]
        for skill in skill_list:
            print(f"{skill}: Current Rank{config.skills[skill]}")
        choice = safe_int_input("Gain a skill at Rank 1:\n1. Deception\n2. Pilot\n3. Zero-G\n4. Gunner", (1, 4))
        increase_skill(skill_list[choice - 1], set_rank=1)

    elif roll == 5:
        log_and_print("A police detective or rival criminal forces you to flee and vows to hunt you down.")
        config.enemies += 1
        
    else:
        log_and_print("Injured in a criminal fashion.")
        injury()


def rogue_events():
    roll = roll_2d6()
    if roll == 2:
        config.not_ejected = True     
        log_and_print("Disaster!  You have a mishap, but your career will survive.")
        rogue_mishap()

    elif roll == 3:
        log_and_print("You are arrested and charged.")
        choice = safe_int_input("Do you:\n 1. Defend yourself\n2. Hire a lawyer\n", (1, 2))
        if choice == 1:
            result = skill_check("Advocate")
            if result >= 8:
                log_and_print("After accusing the arresting officer of using an ethnic slur, you are released.")
            else:
                log_and_print("Despite explaining that you were 'travelling,' not 'driving,' you are convicted and fined.")
                log_and_print("You also have an annoyed justice enthusiast after you.")
                config.rogue_terms -= 1
                config.enemies += 1
        else:
            log_and_print("Your lawyer is expensive, but effective.  After getting you acquitted, he gives you a business card.")
            config.contacts += 1    

    elif roll == 4:
        log_and_print("You are involved in the planning of an impressive heist.")
        choice = safe_int_input(f"Gain a skill at Rank 1:\n1. Computers ({config.skills["Computers"]})\n2. Sensors ({config.skills["Sensors"]})\n"
                                f"3. Comms ({config.skills["Comms"]})\n4. Mechanic ({config.skills["Mechanic"]}\n)", (1, 4))
        skill_list = ["Computers", "Sensors", "Comms", "Mechanic"]
        increase_skill(skill_list[choice - 1], set_rank=1)

    elif roll == 5:
        log_and_print("One of your crimes pays off.  Your victim is out to get you.")
        config.benefit_bonus.append(2)
        config.enemies += 1

    elif roll == 6:
        log_and_print("You have the opportunity to backstab a fellow Rogue for personal gain.")
        choice = safe_choice("Do you do it? (y/n)\n", ("y", "n"))
        if choice == "y":
            log_and_print("You get some approval for your mercenary attitude.")
            config.advance_bonus += 4
        else:
            log_and_print("He appreciates your restraint and becomes a good friend.")
            config.allies += 1

    elif roll == 7:
        life_events()

    elif roll == 8:
        log_and_print("You spend months in the dangerous criminal underworld.")
        skill_list = ["Streetwise", "Stealth", "Melee", "Gun Combat"]
        for skill in skill_list:
            print(f"{skill} ({config.skills[skill]})")
        choice = safe_int_input("Gain a skill at Rank 1:\n1. Streetwise\n2. Stealth\n3. Melee\n4. Gun Combat", (1, 4))
        increase_skill(skill_list[choice - 1], set_rank=1)
        

    elif roll == 9:
        log_and_print("You become involved in a feud with a rival criminal organization.")
        choice = safe_int_input("You must roll:\n1. Stealth\n2. Gun Combat", (1, 2))
        skill_list = ["Stealth", "Gun Combat"]
        result = skill_check(skill_list[choice - 1], "Dexterity")
        if result >= 8:
            log_and_print("You come out ahead in the feud.")
            config.rogue_terms += 1
        else:
            log_and_print("You get some scars and humility.")
            injury()

    elif roll == 10:
        log_and_print("You are involved in a gambling ring.")
        increase_skill("Gambler", set_rank=1)
        log_and_print("You get the opportunity to gamble your fortune on a potentially lucrative deal.")
        choice = safe_choice("Will you risk your benefits? (y/n)\n", ("y", "n"))
        if choice == "y":
            benefits = config.rogue_terms
            if config.rogue_rank == 1 or config.rogue_rank == 2:
                benefits += 1
            elif config.rogue_rank == 3 or config.rogue_rank == 4:
                benefits += 2
            elif config.rogue_rank >= 5:
                benefits += 3
            choice = safe_int_input(f"You have {benefits} benefit rolls to gamble.\nChoose how many: ", (1, benefits))
            result = skill_check("Gambler", best_mental())
            if result >= 8:
                config.rogue_terms += math.ceil(choice / 2)
                print(f"You gain {math.ceil(choice / 2)} benefit rolls.")
                config.event_log.append("Your bet pays off.")
            elif result < 8:
                config.rogue_terms -= choice
                print(f"You lose {choice} benefit rolls.")
                config.event_log.append("You lose your shirt.")
        else:
            log_and_print("You play it safe.")
    
    elif roll == 11:
        log_and_print("A crime lord takes you under his wing.")
        config.allies += 1
        choice = safe_int_input("Choose either:\n1. Gain Tactics 1\n2. +4 DM to your next Advancement roll\n", (1, 2))
        if choice == 1:
            increase_skill("Tactics", set_rank=1)
        else:
            config.advance_bonus += 4

    else:
        log_and_print("You commit a legendary crime.  You are automatically promoted.")
        config.auto_advance = True
                
def join_draft():
    config.drafted = True
    config.previously_drafted = True
    config.forced_drafted = False
    event_log.append(f"{config.char_name} signed up for the draft.")
    selection = roll_1d6()
    if selection == 1:
        print("In the Navy, you can live a life of ease...\n")
        car_navy()
    elif selection == 2:
        print("You're in the Army now!")
        car_army()
    elif selection == 3:
        print("Praise the Lord and pass the ammuntion, Marine!")
        car_marines()
    elif selection == 4:
        print("You've joined the Merchant Marine to experience boredom or torpedoes.")
        car_merchants()
    elif selection == 5:
        print("With the Scouts, you will boldly go where others are smart enough not to.")
        car_scout()
    elif selection == 6:
        print("You are...  THE LAW!!!")
        car_agent()

def attempt_career():
    print("You can pursue one of the following careers:")
    for i in range(len(available_careers)):
        print(f"{i + 1}: {available_careers[i]}")
    choice = safe_int_input("Your choice?\n", (1, len(available_careers)))
    career_funcs[available_careers[choice - 1]]()

def check_retirement():
    retirement = safe_choice(f"Do you wish to retire? y/n?\n", ["y", "n"])
    if retirement == "n":
        attempt_career()
    else:
        retire()  

def qualification(career, mod, goal):
    config.qual = True
    score = roll_2d6() + mods[mod] - config.prior_careers
    if config.qual_bonus != 0:
        score += config.qual_bonus
        config.qual_bonus = 0
    if score < goal:
        config.qual = False
        print(f"With a modified roll of {score}, you have failed to qualify for {career}.")
        if not config.previously_drafted:
            choice = safe_int_input("You can now choose to (1.) Join the Draft or (2.) become a lowly Drifter.\n", valid_range=(1, 2))
            if choice == 1:
                join_draft()
            else:
                car_drifter()
        else:
            print("You wander the stars for four years as a lowly Drifter.")
            car_drifter()

def survival(mod, goal):
    roll = roll_2d6()
    surv = roll + config.mods[mod] + config.survive_bonus
    print(f"Your survival roll is {roll} and you add {config.mods[mod]} for a total of {surv}.")
    if surv < goal:
        return False
    else:
        return True
    
def advance(mod, goal, career_terms):
    if config.auto_advance:
        config.auto_advance = False
        return 1
    else:
        roll = roll_2d6()
        if roll == 12:
            config.must_continue = True
        advance = roll + config.mods[mod] + config.advance_bonus
        print(f"You roll for advancement, rolling {roll}, adding {config.mods[mod]} for your abilities and gaining {config.advance_bonus} in miscellaneous bonuses.")
        config.advance_bonus = 0
        if advance <= career_terms:
            return 3
        if advance < goal:
            return 2
        else:
            return 1
        
def cash_roll(career_table, career_rank):
    benefit = roll_1d6()
    if config.skills["Gambler"]:
        if config.skills["Gambler"] >= 1:
            benefit += 1
        if career_rank >= 5:
             benefit += 1
        if config.benefit_bonus:
            benefit += config.benefit_bonus[-1]
            config.benefit_bonus.pop()
        if benefit > 7:
            benefit = 7

    config.starting_cash += career_table[benefit]
    log_and_print(f"You gain {career_table[benefit]} credits.")

def car_drifter():
    global available_careers
    config.terms += 1
    

    DRIFTER_MUSTER_CASH = {
        1: 0,
        2: 0,
        3: 1000,
        4: 2000,
        5: 3000,
        6: 4000,
        7: 8000,
    }

    def drifter_muster():
        muster_rolls = config.drifter_terms
        if config.drifter_rank == 1 or config.drifter_rank == 2:
            muster_rolls += 1
        if config.drifter_rank == 3 or config.drifter_rank == 4:
            muster_rolls += 2
        if config.drifter_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(DRIFTER_MUSTER_CASH, config.drifter_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.drifter_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                    if benefit > 7:
                        benefit = 7

                if benefit == 1:
                    log_and_print(f"You gained a Contact during your time as a {config.spec_name}")
                    config.contacts += 1
                elif benefit == 2 or benefit == 4:
                    weapon_benefit()
                elif benefit == 3:
                    log_and_print("Being at the bottom forges strong friendships. You gain an Ally.")
                    config.allies += 1
                elif benefit == 5:
                    log_and_print("Knowledge is a wealth of its own.  You gain +1 Education.")
                    config.increase_stat("Education")
                    config.update_char()
                elif benefit == 6:
                    log_and_print("You make a few investments and gain a Ship Share")
                    config.ship_shares += 1
                elif benefit == 7:
                    log_and_print("You make a few investments and gain two Ship Shares")
                    config.ship_shares += 2

    def drifter_develop():
        config.careers.append(f"Drifter: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        choice = safe_int_input("1, 2, or 3?\n", (1, 3))
        roll = roll_1d6()
        if choice == 1:
            DRIFTER_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            DRIFTER_SERVICE_SKILLS[roll]()

        else:
            config.spec_table[roll]()

    def drifter_mishap():
        print("You have suffered a dangerous mishap.")
        roll = roll_1d6()
        if roll == 1:
            injury(2)
        if roll == 2:
            injury()
        if roll == 3:
            config.enemies += 1
            print("You run afoul of a criminal gang, corrupt bureaucrat, or other foe.  You have gained an enemy.")
        if roll == 4:
            config.values["Endurance"] -= 1
            print("You have suffered a life-threatening illness.  Endurance - 1")
            update_char()
        if roll == 5:
            life_events(8)
        if roll == 6:
            print("You don't know what happened to you.  There is a gap in your memory.")

    def drifter_events():
        roll = roll_2d6()
        if roll == 2:
            drifter_mishap()
        if roll == 3:
            config.qual_bonus += 4
            print("A patron offers you a chance at a job. You gain +4 DM to your next Qualification roll, but you owe that patron a favor.")
            config.event_log.append("You got a leg up, but now owe a favor to a powerful man/organization.")
        if roll == 4:
            print("You pick up a few useful skills here and there.")
            print("Choose to gain:\n1. Jack of All Trades\n2. Survival\n3. Streetwise\n4. Melee.")
            choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))
            if choice == 1:
                config.increase_skill("Jack of all Trades")
            if choice == 2:
                config.increase_skill("Survival")
            if choice == 3:
                config.increase_skill("Streetwise")
            if choice == 4:
                config.increase_skill("Melee")
        if roll == 5:
            print("You manage to scavenge something of use.  Gain +1 to a Benefit roll.")
            config.benefit_bonus.append(1)
            config.event_log.append("You scavenged something useful.")
        if roll == 6:
            print("You encounter something unusual.")
            config.life_events(12)
        if roll == 7:
            config.life_events()
        if roll == 8:
            if config.enemies < 1:
                config.enemies += 1
            print("You are attacked by enemies!")
            print("To avoid injury you must roll:\n1. Melee\n2. Gun Combat\n3. Stealth")
            choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            if choice == 1:
                result = config.skill_check("Melee", best_of_two("Strength", "Dexterity"))
            elif choice == 2:
                result = config.skill_check("Gun Combat", "Dexterity")
            elif choice == 3:
                result = config.skill_check("Stealth", "Dexterity")
            if result < 8:
                config.injury()
            else:
                print("You narrowly escape injury!")
                config.event_log.append("You were attacked and narrowly escaped injury")
        if roll == 9:
            print("You are offered the chance to take part in a risky, but maybe rewarding, adventure.")
            choice = safe_choice("y/n?\n", ["y", "n"])
            if choice == "y":
                result = roll_1d6()
                if result < 3:
                    print("That didn't go well.")
                    config.injury()
                elif result >2 and result <5:
                    print("Well, that was a waste of time.")
                    config.event_log.append("You engaged in risky venture and gained nothing but stories.")
                else:
                    print("You have great success!  +4 to a benefit roll.")
                    config.benefit_bonus.append(4)
                    config.event_log.append("You engaged in a profitable adventure.  Quark would be proud.")
        if roll == 10:
            print("Life on the edge hones your ablities.")
            increase_existing_skill() 
        if roll == 11:
            print("You are forcibly drafted!")
            config.event_log.append("You were forcibly drafted!")
            config.prior_careers += 1
            join_draft()
            return

        if roll == 12:
            print("You thrive on adversity.  You are automatically promoted.")
            config.auto_advance = True

    DRIFTER_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Strength"),
        2: lambda: increase_stat("Endurance"),
        3: lambda: increase_stat("Dexterity"),
        4: lambda: increase_skill("Jack of all Trades"),
        5: lambda: increase_stat("Endurance"),
        6: lambda: increase_stat("Intelligence")
    }
    
    DRIFTER_SERVICE_SKILLS = {
        1: lambda: increase_skill("Athletics"),
        2: lambda: increase_skill("Melee"),
        3: lambda: increase_skill("Recon"),
        4: lambda: increase_skill("Streetwise"),
        5: lambda: increase_skill("Stealth"),
        6: lambda: increase_skill("Survival"),
    }

    SPEC_BARBARIAN = {
        1: lambda: increase_skill("Animals"),
        2: lambda: increase_skill("Carouse"),
        3: lambda: increase_skill("Melee"),
        4: lambda: increase_skill("Stealth"),
        5: lambda: increase_skill("Seafarer"),
        6: lambda: increase_skill("Survival"),
    }

    SPEC_WANDERER = {
        1: lambda: increase_skill("Athletics"),
        2: lambda: increase_skill("Deception"),
        3: lambda: increase_skill("Recon"),
        4: lambda: increase_skill("Stealth"),
        5: lambda: increase_skill("Streetwise"),
        6: lambda: increase_skill("Survival"),
    }

    SPEC_SCAVENGER = {
        1: lambda: increase_skill("Pilot"),
        2: lambda: increase_skill("Mechanic"),
        3: lambda: increase_skill("Astrogation"),
        4: lambda: increase_skill("Vacc Suit"),
        5: lambda: increase_skill("Zero-G"),
        6: lambda: increase_skill("Gun Combat"),
    }

    if "Drifter" not in config.careers:
        print("As a Drifter, you must choose one of the following paths:")
        print("1. A Barbarian, struggling to survive on a primitive world.")
        print("2. A Wanderer, moving from starport to starport with your hand out.")
        print("3. A Scavenger, mining asteroids or stripping shipwrecks in the cold void.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.drifter_rank = 0

        if spec_choice == 1:
            config.spec_name = "Barbarian"
            config.spec_table = SPEC_BARBARIAN
            config.survival_tuple = ("Endurance", 7) 
            config.advancement_tuple = ("Strength", 7)  
            config.careers.append("Drifter")
            config.event_log.append(f"Term{config.terms}: Drifter: Barbarian")
            if config.prior_careers < 1:
                for effect in SPEC_BARBARIAN.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Wanderer"
            config.spec_table = SPEC_WANDERER
            config.survival_tuple = ("Endurance", 7)
            config.advancement_tuple = ("Intelligence", 7)  
            config.careers.append("Drifter")
            config.event_log.append(f"Term{config.terms}: Drifter: Wanderer")
            if config.prior_careers < 1:
                for effect in SPEC_WANDERER.values():
                    effect()  
                config.basic_training = False  
    
        if spec_choice == 3:
            config.spec_name = "Scavenger"
            config.spec_table = SPEC_SCAVENGER
            config.survival_tuple = ("Dexterity", 7)
            config.advancement_tuple = ("Endurance", 7) 
            config.careers.append("Drifter") 
            config.event_log.append(f"Term{config.terms}: Drifter: Scavenger")
            if config.prior_careers < 1:
                for effect in SPEC_SCAVENGER.values():
                    effect()
                config.basic_training = False

    else:
        print("You continue the life of a Drifter.")
        config.careers.append(f"Term{config.terms}: Drifter: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Drifter: {config.spec_name}")
    
    drifter_develop()
    
    success = survival(*config.survival_tuple)
    
    if not success:
        drifter_mishap()

    if success:
        config.drifter_terms += 1
        drifter_events()
        promotion = advance(*config.advancement_tuple, config.drifter_terms)
 
        if promotion == 1:
            config.drifter_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.drifter_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.drifter_rank} {config.spec_name}.")
            if config.spec_name == "Barbarian":
                if config.drifter_rank == 1:
                    increase_skill("Survival", set_rank=1)
                elif config.drifter_rank == 2:
                    increase_skill("Melee", set_rank=1)
                elif config.drifter_rank == 4:
                    increase_skill("Leadership", set_rank=1)
            elif config.spec_name == "Wanderer":
                if config.drifter_rank == 1:
                    increase_skill("Streetwise", set_rank=1)
                elif config.drifter_rank == 3:
                    increase_skill("Deception", set_rank=1)
            elif config.spec_name == "Scavenger":
                if config.drifter_rank == 1:
                    increase_skill("Vacc Suit", set_rank=1)
                elif config.drifter_rank == 3:
                    choice = safe_int_input("Choose to gain a skill at Rank 1:\n1. Trade\n2. Mechanic\n", (1, 2))
                    if choice == 1:
                        increase_skill("Trade", set_rank=1)
                    elif choice == 2:
                        increase_skill("Mechanic", set_rank=1)

            print("Choose a table to advance your skills:\n")
            print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
            choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                DRIFTER_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                DRIFTER_SERVICE_SKILLS[roll]()

            else:
                config.spec_table[roll]()
    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()
    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_drifter()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_drifter()
    else:
        config.prior_careers += 1
        drifter_muster()
        config.drifter_terms = 0

    check_retirement()

def car_agent():
    global available_careers

    AGENT_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_skill("Gun Combat"),
        2: lambda: increase_stat("Dexterity"),
        3: lambda: increase_stat("Endurance"),
        4: lambda: increase_skill("Melee"),
        5: lambda: increase_stat("Intelligence"),
        6: lambda: increase_skill("Athletics")
    }

    AGENT_SERVICE_SKILLS = {
        1: lambda: increase_skill("Streetwise"),
        2: lambda: increase_skill("Drive"),
        3: lambda: increase_skill("Investigate"),
        4: lambda: increase_skill("Computers"),
        5: lambda: increase_skill("Recon"),
        6: lambda: increase_skill("Gun Combat"),
    }

    AGENT_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Advocate"),
        2: lambda: increase_skill("Comms"),
        3: lambda: increase_skill("Computers"),
        4: lambda: increase_skill("Medic"),
        5: lambda: increase_skill("Stealth"),
        6: lambda: increase_skill("Remote Operations"),
    }   
    
    AGENT_LAW_ENFORCEMENT = {
        1: lambda: increase_skill("Investigate"),
        2: lambda: increase_skill("Recon"),
        3: lambda: increase_skill("Streetwise"),
        4: lambda: increase_skill("Stealth"),
        5: lambda: increase_skill("Melee"),
        6: lambda: increase_skill("Advocate"),
    }

    AGENT_INTELLIGENCE = {
        1: lambda: increase_skill("Investigate"),
        2: lambda: increase_skill("Recon"),
        3: lambda: increase_skill("Comms"),
        4: lambda: increase_skill("Stealth"),
        5: lambda: increase_skill("Persuade"),
        6: lambda: increase_skill("Deception"),
    }

    AGENT_CORPORATE = {
        1: lambda: increase_skill("Investigate"),
        2: lambda: increase_skill("Computers"),
        3: lambda: increase_skill("Stealth"),
        4: lambda: increase_skill("Gun Combat"),
        5: lambda: increase_skill("Deception"),
        6: lambda: increase_skill("Streetwise"),
    }

    AGENT_MUSTER_CASH = {
        1: 1000,
        2: 2000,
        3: 5000,
        4: 7500,
        5: 10000,
        6: 25000,
        7: 50000,
    }    

    def agent_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Agent")
        roll = roll_1d6()
        if roll == 1:
            log_and_print(f"Severely injured in action.")
            choice = safe_int_input("You must choose to:\n1. Accept a roll of '2' on the injury table.\n2. Roll twice and take the lower result.\n", (1, 2))
            if choice == 1:
                injury(2)
            else:
                injury_roll_twice()

        elif roll == 2:
            log_and_print("\nA criminal or other figure under investigation offers you a deal.\n")
            choice = safe_int_input("You must choose:\n1. Accept, and leave this career without further penalty.\n2. Refuse, take the lowest of two rolls on the injury table, gain an Enemy, and advance any one skill of your choice.\n", (1, 2))
            if choice == 1:
                log_and_print("You took the deal, and left your career in disgrace.")
            else:
                injury_roll_twice()
                config.enemies += 1
                increase_any_skill()

        elif roll == 3:
            log_and_print("An investigation goes critically wrong or leads to the top, ruining your career.\n")
            if skill_check("Advocate", best_mental()):
                config.keep_bonus = True
                log_and_print("Fortunately, thanks to a bit of bureaucratic know-how, you keep your benefits for the term.")

        elif roll == 4:
            log_and_print("You learn something you shouldn't know, and people want to kill you for it.")
            config.enemies += 1
            increase_skill("Deception", set_rank=1)

        elif roll == 5:
            if config.contacts == 0 and config.allies == 0:
                log_and_print("Your work follows you home and puts a member of your family in the hospital.")
            elif config.contacts > 0 and config.allies == 0:
                config.contacts -= 1
                log_and_print("Your work follows you home and one of your contacts gets taken out of action.")
            elif config.contacts == 0 and config.allies > 0:
                config.allies -= 1
                log_and_print("One of your closest allies, someone who said they would take a bullet for you, just did.")
            else:
                target = roll_1d6() % 2
                if target == 0:
                    config.contacts -= 1
                    log_and_print("Your work follows you home and one of your contacts gets taken out of action.")  
                else:
                    config.allies -= 1
                    log_and_print("One of your closest allies, someone who said they would take a bullet for you, just did.")

        else:
            injury()

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Agent")
            return
        if not config.keep_bonus:
            config.agent_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        agent_muster()
        check_retirement()
        return

    def agent_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            agent_mishap()
        elif roll == 3:
            log_and_print("An investigation takes on a dangerous turn.")
            choice = safe_int_input("You must roll against one of these skills:\n1. Investigate\n2. Streetwise\n", (1, 2))
            if choice == 1:
                result = skill_check("Investigate", best_mental())
            elif choice == 2:
                result = skill_check("Streetwise", best_mental())
            if result < 8:
                print("That didn't go well.")
                config.not_ejected = True
                agent_mishap()
            else:
                bonus = safe_int_input("You succeeded and learned a few things in the process.  Raise one of the following skills:\n"
                "1. Deception\n2. Jack of all Trades\n3. Persuade\n4. Tactics\n", (1, 4))
                if bonus == 1:
                    increase_skill("Deception")
                elif bonus == 2:
                    increase_skill("Jack of all Trades")
                elif bonus == 3:
                    increase_skill("Persuade")
                else:
                    increase_skill("Tactics")

        elif roll == 4:
            log_and_print("You complete a mission for your superiors, and are suitably rewarded.")
            config.benefit_bonus.append(1)

        elif roll == 5:
            log_and_print("You establish a network of contacts.")
            config.contacts += roll_1d3()

        elif roll == 6:
            log_and_print("You are given advanced training in a specialized field.")
            learning = roll_2d6() + config.mods["Education"]
            if learning < 8:
                log_and_print("The education doesn't really stick, but the teacher was very attractive.")
            else:
                increase_existing_skill()

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("You are sent on an undercover mision.")
            config.agent_undercover = True
            result = skill_check("Deception", best_mental())
            career_choice = safe_int_input("Go undercover in:\n1. Rogue circles\n2. Citizen life\n", (1, 2))
            if result >= 8:
                if career_choice == 1:
                    rogue_events()
                    table_list = [ROGUE_THIEF, ROGUE_ENFORCER, ROGUE_PIRATE]
                    choice = safe_int_input("Select a skill table to roll on:\n1. Thief\n2. Enforcer\n3. Pirate")
                    table = table_list[choice - 1]
                    roll = roll_1d6()
                    table[roll]()
                else:
                    citizen_events()
                    table_list = [CITIZEN_CORPORATE, CITIZEN_WORKER, CITIZEN_COLONIST]
                    choice = safe_int_input("Select a skill table to roll on:\n1. Corporate\n2. Worker\n3. Colonist")
                    table = table_list[choice - 1]
                    roll = roll_1d6()
                    table[roll]()
            else:
                config.not_ejected = True
                if career_choice == 1:
                    rogue_mishap()
                else:
                    citizen_mishap()

        elif roll == 9:
            log_and_print("You go above and beyond the call of duty!")
            config.advance_bonus += 2

        elif roll == 10:
            log_and_print("You are given specialized vehicular training.")
            choice = safe_int_input("Choose to gain a skill at Rank 1:\n"
            "1. Drive\n2. Flyer\n3. Pilot\n4. Gunner\n", (1, 4))
            if choice == 1:
                increase_skill("Drive", set_rank=1)
            elif choice == 2:
                increase_skill("Flyer", set_rank=1)
            elif choice == 3:
                increase_skill("Pilot", set_rank=1)
            else:
                increase_skill("Gunner", set_rank=1)
        
        elif roll == 11:
            log_and_print("You are befriended by a senior agent.")
            choice = safe_int_input("Choose either:\n1. Increase Investigate by one level\n2. +4 DM to your next Advancement roll\n", (1, 2))
            if choice == 1:
                increase_skill("Investigate")
            else:
                config.advance_bonus += 4

        else:
            log_and_print("Your efforts uncover a major conspiracy against your employers.  You are automatically promoted.")
            config.auto_advance = True

    def agent_muster():
        muster_rolls = config.agent_terms
        if config.agent_rank == 1 or config.agent_rank == 2:
            muster_rolls += 1
        if config.agent_rank == 3 or config.agent_rank == 4:
            muster_rolls += 2
        if config.agent_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(AGENT_MUSTER_CASH, config.agent_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.agent_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print(f"You were issued scientific equipment during your time as a {config.spec_name}")
                    config.starting_items.append("Scientific Equipment")
                elif benefit == 2:
                    log_and_print("You got a little smarter in the field when the alternative was getting deader.")
                    increase_stat("Intelligence")
                    update_char()
                elif benefit == 3:
                    log_and_print("You make a few investments and gain a Ship Share.")
                    config.ship_shares += 1
                elif benefit == 4:
                    weapon_benefit()
                elif benefit == 5:
                    log_and_print("Your job required more than a man, so they put some extra hardware in you.")
                    config.starting_items.append("Combat Implant")
                elif benefit == 6:
                    choice = safe_int_input("Choose:\n1. +1 Social\n2. Combat Implant\n", (1, 2))
                    if choice == 1:
                        log_and_print("You made friends in high places.")
                        increase_stat("Social Standing")
                    else:
                        log_and_print("Your job required more than a man, so they put some extra hardware in you.")
                        config.starting_items.append("Combat Implant")
                elif benefit == 7:
                    tas_member()

    def agent_develop():
        config.careers.append(f"Agent: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            AGENT_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            AGENT_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            AGENT_ADVANCED_EDUCATION[roll]()

    if not config.drafted and config.agent_terms < 1:
        qualification("Agent", "Intelligence", 6)

        if not config.qual:
            return
    
    config.terms += 1
    config.agent_terms += 1
    if "Agent" not in config.careers and not config.drafted:
        print("As an Agent, you must choose one of the following paths:")
        print("1. Law Enforcement, a police officer or detective.")
        print("2. Intelligence, spying for a government... maybe even your own.")
        print("3. Corporate, sniffing out the secrets of the competition.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Agent")
        if spec_choice == 1:
            config.spec_name = "Law Enforcement"
            config.spec_table = AGENT_LAW_ENFORCEMENT
            config.survival_tuple = ("Endurance", 6) 
            config.advancement_tuple = ("Intelligence", 6)  
            config.event_log.append(f"Term{config.terms}: Agent: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in AGENT_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Intelligence"
            config.spec_table = AGENT_INTELLIGENCE
            config.survival_tuple = ("Intelligence", 7)
            config.advancement_tuple = ("Intelligence", 5)  
            config.event_log.append(f"Term{config.terms}: Agent: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in AGENT_SERVICE_SKILLS.values():
                    effect() 
                config.basic_training = False   
    
        if spec_choice == 3:
            config.spec_name = "Corporate"
            config.spec_table = AGENT_CORPORATE
            config.survival_tuple = ("Intelligence", 5)
            config.advancement_tuple = ("Intelligence", 7)  
            config.event_log.append(f"Term{config.terms}: Agent: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in AGENT_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    elif config.drafted:
            config.drafted = False
            log_and_print("You are drafted into service as a constable; keeping the peace for the good citizens of the Empire.")
            config.careers.append("Agent")
            config.spec_name = "Law Enforcement"
            config.spec_table = AGENT_LAW_ENFORCEMENT
            config.survival_tuple = ("Endurance", 6) 
            config.advancement_tuple = ("Intelligence", 6)  
            config.event_log.append(f"Term{config.terms}: Agent: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in AGENT_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    else:
        print("You sign up for another term of intrigue.")
        config.careers.append(f"Term{config.terms}: Agent: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Agent: {config.spec_name}")
    
    agent_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        agent_mishap()

    if success:
        agent_events()
        config.agent_undercover = False
        config.not_ejected = False  #Needed to cover situation where Agent rolls on Citizen/Rogue mishap tables.
        promotion = advance(*config.advancement_tuple, config.agent_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            agent_muster()
            config.prior_careers += 1
            available_careers.remove("Agent")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.agent_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.agent_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.agent_rank} {config.spec_name}.")
            if config.spec_name == "Law Enforcement":
                if config.agent_rank == 1:
                    increase_skill("Streetwise", set_rank=1)
                elif config.agent_rank == 4:
                    increase_skill("Investigate", set_rank=1)
                elif config.agent_rank == 5:
                    increase_skill("Admin", set_rank=1)
                elif config.agent_rank == 6:
                    increase_stat("Social Standing")
            else:
                if config.agent_rank == 1:
                    increase_skill("Deception", set_rank=1)
                elif config.agent_rank == 2:
                    increase_skill("Investigate", set_rank=1)
                elif config.agent_rank == 4:
                    increase_skill("Vacc Suit", set_rank=1)

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 8:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                AGENT_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                AGENT_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                AGENT_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_agent()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_agent()
    else:
        config.prior_careers += 1
        agent_muster()

    check_retirement()

def car_army():
    global available_careers

    ARMY_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Strength"),
        2: lambda: increase_stat("Dexterity"),
        3: lambda: increase_stat("Endurance"),
        4: lambda: increase_skill("Gambler"),
        5: lambda: increase_skill("Medic"),
        6: lambda: increase_skill("Melee")
    }

    ARMY_SERVICE_SKILLS = {
        1: lambda: increase_skill("Drive"),
        2: lambda: increase_skill("Athletics"),
        3: lambda: increase_skill("Gun Combat"),
        4: lambda: increase_skill("Recon"),
        5: lambda: increase_skill("Melee"),
        6: lambda: increase_skill("Heavy Weapons"),
    }

    ARMY_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Comms"),
        2: lambda: increase_skill("Sensors"),
        3: lambda: increase_skill("Navigation"),
        4: lambda: increase_skill("Explosives"),
        5: lambda: increase_skill("Engineer"),
        6: lambda: increase_skill("Survival"),
    }   
    
    ARMY_OFFICER = {
        1: lambda: increase_skill("Tactics"),
        2: lambda: increase_skill("Leadership"),
        3: lambda: increase_skill("Advocate"),
        4: lambda: increase_skill("Diplomat"),
        5: lambda: increase_skill("Tactics"),
        6: lambda: increase_skill("Admin"),
    }   

    ARMY_SUPPORT = {
        1: lambda: increase_skill("Mechanic"),
        2: lambda: increase_skill("Drive"),
        3: lambda: increase_skill("Flyer"),
        4: lambda: increase_skill("Explosives"),
        5: lambda: increase_skill("Comms"),
        6: lambda: increase_skill("Medic"),
    }

    ARMY_INFANTRY = {
        1: lambda: increase_skill("Gun Combat"),
        2: lambda: increase_skill("Melee"),
        3: lambda: increase_skill("Heavy Weapons"),
        4: lambda: increase_skill("Stealth"),
        5: lambda: increase_skill("Athletics"),
        6: lambda: increase_skill("Recon"),
    }

    ARMY_CAVALRY = {
        1: lambda: increase_skill("Mechanic"),
        2: lambda: increase_skill("Drive"),
        3: lambda: increase_skill("Flyer"),
        4: lambda: increase_skill("Recon"),
        5: lambda: increase_skill("Gunnery"),
        6: lambda: increase_skill("Sensors"),
    }

    ARMY_MUSTER_CASH = {
        1: 2000,
        2: 5000,
        3: 10000,
        4: 10000,
        5: 10000,
        6: 25000,
        7: 30000,
    }    

    def army_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Army")
        roll = roll_1d6()
        if roll == 1:
            log_and_print(f"Severely injured in action.")
            choice = safe_int_input("You must choose to:\n1. Accept a roll of '2' on the injury table.\n2. Roll twice and take the lower result.\n", (1, 2))
            if choice == 1:
                injury(2)
            else:
                injury_roll_twice()

        elif roll == 2:
            log_and_print("Your unit is slaughtered in a disastrous battle, for which you blame your commander.")
            config.enemies += 1

        elif roll == 3:
            log_and_print("You are dropped into hellish terrain to fight with seasoned guerillas.")
            log_and_print("You are discharged due to stress, injury, or because the government wants to bury the whole incident.")
            log_and_print("The guerilla rebels remember you and consider you an enemy.")
            config.enemies += 1

        elif roll == 4:
            log_and_print("Your commanding officer is engaged in a criminal enterprise.  He invites you to join him.")
            choice = safe_int_input("Do you choose to:\n1. Join him\n2. Notify the military police\n")
            if choice == 1:
                log_and_print("You both get discharged after investigation, but your CO remains a loyal ally.")
                config.allies += 1
            else:
                log_and_print("You are discharged as part of the official coverup, but they don't cut your benefits.")
                config.keep_bonus = True

        elif roll == 5:
            log_and_print("You are tormented by or quarrel with an officer or fellow soldier.  Your rival drives you out of the service.")
            config.rivals += 1

        else:
            injury()

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Army")
            return
        if not config.keep_bonus:
            config.army_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        army_muster()
        check_retirement()   

    def army_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            army_mishap()
        elif roll == 3:
            log_and_print("You are assigned to a planet with a hostile or wild environment.")
            bonus = safe_int_input("Gain one of the following skills:\n"
                "1. Vacc Suit 1\n2. Engineer 1\n3. Animals 1\n4. Recon 1\n", (1, 4))
            if bonus == 1:
                increase_skill("Vacc Suit", set_rank=1)
            elif bonus == 2:
                increase_skill("Engineer", set_rank=1)
            elif bonus == 3:
                increase_skill("Animals", set_rank=1)
            else:
                increase_skill("Recon", set_rank=1)

        elif roll == 4:
            log_and_print("You are assigned to an urbanised planet torn by war.")
            bonus = safe_int_input("Gain one of the following skills:\n"
                "1. Stealth 1\n2. Streetwise 1\n3. Persuade 1\n4. Recon 1\n", (1, 4))
            if bonus == 1:
                increase_skill("Stealth", set_rank=1)
            elif bonus == 2:
                increase_skill("Streetwise", set_rank=1)
            elif bonus == 3:
                increase_skill("Persuade", set_rank=1)
            else:
                increase_skill("Recon", set_rank=1)

        elif roll == 5:
            log_and_print("You are given a special assignment or duty in your unit.")
            config.benefit_bonus.append(1)

        elif roll == 6:
            log_and_print("You are thrown into a brutal ground war.")
            war = config.mods["Endurance"] + roll_2d6()
            if war >= 8:
                    bonus = safe_int_input("Gain one of the following skills:\n"
                "1. Gun Combat\n2. Leadership\n", (1, 2))
                    if bonus == 1:
                        increase_skill("Gun Combat")
                    elif bonus == 2:
                        increase_skill("Leadership")
            else:
                injury()

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("You are given advanced training in a specialized field.")
            learning = roll_2d6() + config.mods["Education"]
            if learning < 8:
                log_and_print("The education doesn't really stick, but the teacher was very attractive.")
            else:
                print("You're an excellent student.")
                increase_existing_skill()

        elif roll == 9:
            log_and_print("Surrounded and outnumbered by the enemy, you hold out until relief arrives!  +2 DM to your next advancement.")
            config.advance_bonus += 2

        elif roll == 10:
            log_and_print("You are assigned to a peacekeeping role.")
            choice = safe_int_input("Choose to gain a skill at Rank 1:\n"
            "1. Admin\n2. Investigate\n3. Deception\n4. Recon\n", (1, 4))
            if choice == 1:
                increase_skill("Admin", set_rank=1)
            elif choice == 2:
                increase_skill("Investigate", set_rank=1)
            elif choice == 3:
                increase_skill("Deception", set_rank=1)
            else:
                increase_skill("Recon", set_rank=1)
        
        elif roll == 11:
            log_and_print("Your commanding officer takes an interest in your career.")
            choice = safe_int_input("Choose either:\n1. Gain Tactics 1\n2. +4 DM to your next Advancement roll\n", (1, 2))
            if choice == 1:
                increase_skill("Tactics", set_rank=1)
            else:
                config.advance_bonus += 4

        else:
            log_and_print("You display heroism in battle.  You are automatically promoted.")
            config.auto_advance = True

    def army_muster():
        muster_rolls = config.army_terms
        if config.army_rank == 1 or config.army_rank == 2:
            muster_rolls += 1
        if config.army_rank == 3 or config.army_rank == 4:
            muster_rolls += 2
        if config.army_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(ARMY_MUSTER_CASH, config.army_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.army_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print("Your job required more than a man, so they put some extra hardware in you.")
                    config.starting_items.append("Combat Implant")
                elif benefit == 2:
                    log_and_print("You got a little smarter in the field when the alternative was getting deader.")
                    increase_stat("Intelligence")
                    update_char()
                elif benefit == 3:
                    log_and_print("You stayed awake during a few of your classes.")
                    increase_stat("Education")
                    update_char()
                elif benefit == 4:
                    weapon_benefit()
                elif benefit == 5:
                    armour_benefit()
                elif benefit == 6:
                    choice = safe_int_input("Choose:\n1. +1 Endurance\n2. Combat Implant\n")
                    if choice == 1:
                        log_and_print("You stayed in shape after basic.")
                        increase_stat("Endurance")
                    else:
                        log_and_print("Your job required more than a man, so they put some extra hardware in you.")
                        config.starting_items.append("Combat Implant")
                elif benefit == 7:
                    log_and_print("Being the star of several medal-pinning ceremonies gave you contacts in high society.")
                    increase_stat("Social Standing")

    def army_develop():
        config.careers.append(f"Army: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            ARMY_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            ARMY_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            ARMY_ADVANCED_EDUCATION[roll]()

    if not config.drafted and config.army_terms < 1:
        if config.age >= 30:
            config.qual_bonus -= 2
        qualification("Army", "Endurance", 5)

        if not config.qual:
            return
    
    config.terms += 1
    config.army_terms += 1
    config.drafted = False

    if "Army" not in config.careers:
        print("As an Army recruit, you must choose one of the following paths:")
        print("1. Support: Doing the less glamorous work in the background.")
        print("2. Infantry: Deployed to areas requiring bullet sponges.")
        print("3. Cavalry: Riding in a tank or other ground vehicle.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Army")
        if spec_choice == 1:
            config.spec_name = "Support"
            config.spec_table = ARMY_SUPPORT
            config.survival_tuple = ("Endurance", 5) 
            config.advancement_tuple = ("Education", 7)  
            if config.prior_careers < 1:
                for effect in ARMY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Infantry"
            config.spec_table = ARMY_INFANTRY
            config.survival_tuple = ("Strength", 6)
            config.advancement_tuple = ("Education", 6)  
            if config.prior_careers < 1:
                for effect in ARMY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Cavalry"
            config.spec_table = ARMY_CAVALRY
            config.survival_tuple = ("Dexterity", 7)
            config.advancement_tuple = ("Intelligence", 5)  
            if config.prior_careers < 1:
                for effect in ARMY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False
        increase_skill("Gun Combat", set_rank=1)

    if config.spec_name != "Officer":
        print("It occurs to you that shining your own boots may be for suckers.")  
        commission = safe_choice("Want to apply for a commission? (y/n)\n", ("y", "n"))
        if commission == "y":
            attempt = config.mods["Social Standing"] + roll_2d6()
            if attempt >= 8:
                config.spec_name = "Officer"
                config.spec_table = ARMY_OFFICER
                log_and_print("You become a commissioned officer.")
            else:
                log_and_print("Your application to officer school is filed very deeply.")

    print("Four years of duty await.")
    config.careers.append(f"Term{config.terms}: Army: {config.spec_name}.")
    config.event_log.append(f"Term{config.terms}: Army: {config.spec_name}")
    
    army_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        army_mishap()

    if success:
        army_events()
        promotion = advance(*config.advancement_tuple, config.army_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            army_muster()
            config.prior_careers += 1
            available_careers.remove("Army")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        if promotion == 1:
            config.army_rank += 1
            if "Officer" in config.spec_name:
                config.army_officer_rank += 1
            else:
                config.army_nco_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.army_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.army_rank} {config.spec_name}.")
            if config.army_nco_rank == 1:
                increase_skill("Recon", set_rank=1)
            elif config.army_nco_rank == 3:
                increase_skill("Leadership", set_rank=1)

            else:
                if config.army_officer_rank == 1:
                    increase_skill("Leadership", set_rank=1)
                elif config.army_officer_rank == 3:
                    increase_skill("Tactics", set_rank=1)
                elif config.army_officer_rank == 6:
                    if config.values["Social Standing"] < 10:
                        config.values["Social Standing"] = 10
                    else:
                        config.values["Social Standing"] += 1

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 8:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                ARMY_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                ARMY_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                ARMY_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        config.event_log.append("You were so successful at your job, you couldn't leave.")
        car_army()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_army()
    else:
        config.prior_careers += 1
        army_muster()

    check_retirement()


def car_citizen():
    global available_careers

    def citizen_muster():
        muster_rolls = config.citizen_terms
        if config.citizen_rank == 1 or config.citizen_rank == 2:
            muster_rolls += 1
        if config.citizen_rank == 3 or config.citizen_rank == 4:
            muster_rolls += 2
        if config.citizen_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1 
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(CITIZEN_MUSTER_CASH, config.citizen_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.citizen_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print("You made a few investments and gained a Ship Share.")
                    config.ship_shares += 1
                elif benefit == 2:
                    log_and_print("You made a lifelong friend and ally.")
                    config.allies += 1
                elif benefit == 3:
                    log_and_print("You earned the sharp eye that comes with experience.")
                    increase_stat("Intelligence")
                elif benefit == 4:
                    weapon_benefit()
                elif benefit == 5:
                    log_and_print("You retained some of that math you learned.")
                    increase_stat("Education")
                elif benefit == 6:
                    log_and_print("You made a few investments and gained two Ship Shares.")
                    config.ship_shares += 2
                elif benefit == 7:
                    tas_member()

    def citizen_develop():
        config.careers.append(f"Citizen: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 10:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            CITIZEN_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            CITIZEN_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            CITIZEN_ADVANCED_EDUCATION[roll]()

    if config.citizen_terms < 1:
        qualification("Citizen", "Education", 5)

        if not config.qual:
            return
    
    config.terms += 1
    config.citizen_terms += 1
    if "Citizen" not in config.careers:
        print("As a Citizen, you must choose one of the following paths:")
        print("1. Corporate, an executive, manager, or bureaucrat.")
        print("2. Worker, somewhere between fixing warp drives and flipping burgers.")
        print("3. Colonist, living that frontier life.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Citizen")
        if spec_choice == 1:
            config.spec_name = "Corporate"
            config.spec_table = CITIZEN_CORPORATE
            config.survival_tuple = ("Social Standing", 6) 
            config.advancement_tuple = ("Intelligence", 6)  
            config.event_log.append(f"Term{config.terms}: Citizen: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in CITIZEN_CORPORATE.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Worker"
            config.spec_table = CITIZEN_WORKER
            config.survival_tuple = ("Endurance", 4)
            config.advancement_tuple = ("Education", 8)  
            config.event_log.append(f"Term{config.terms}: Citizen: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in CITIZEN_WORKER.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Colonist"
            config.spec_table = CITIZEN_COLONIST
            config.survival_tuple = ("Intelligence", 7)
            config.advancement_tuple = ("Endurance", 5)  
            config.event_log.append(f"Term{config.terms}: Citizen: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in CITIZEN_COLONIST.values():
                    effect()
                config.basic_training = False

    else:
        print("You punch the clock for another four years.")
        config.careers.append(f"Term{config.terms}: Citizen: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Citizen: {config.spec_name}")
    
    citizen_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        citizen_mishap()
        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Citizen")
            return
        if not config.keep_bonus:
            config.citizen_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        citizen_muster()
        check_retirement() 

    if success:
        citizen_events()
        promotion = advance(*config.advancement_tuple, config.citizen_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            citizen_muster()
            config.prior_careers += 1
            available_careers.remove("Citizen")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a/an {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.citizen_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.citizen_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.citizen_rank} {config.spec_name}.")
            if config.spec_name == "Corporate":
                if config.citizen_rank == 2:
                    increase_skill("Admin", set_rank=1)
                elif config.citizen_rank == 4:
                    increase_skill("Advocate", set_rank=1)
                elif config.citizen_rank == 6:
                    increase_stat("Social Standing")
            elif config.spec_name == "Worker":
                if config.citizen_rank == 2:
                    increase_skill("Trade", set_rank=1)
                elif config.citizen_rank == 4:
                    increase_skill("Mechanic", set_rank=1)
                elif config.citizen_rank == 6:
                    increase_skill("Engineer", set_rank=1)
            elif config.spec_name == "Colonist":
                if config.citizen_rank == 2:
                    increase_skill("Survival", set_rank=1)
                elif config.citizen_rank == 4:
                    increase_skill("Navigation", set_rank=1)
                elif config.citizen_rank == 6:
                    increase_skill("Gun Combat", set_rank=1)

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 10:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                CITIZEN_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                CITIZEN_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                CITIZEN_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_citizen()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_citizen()
    else:
        config.prior_careers += 1
        citizen_muster()

    check_retirement()

def car_entertainer():
    global available_careers
    ENTERTAINER_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Dexterity"),
        2: lambda: increase_stat("Intelligence"),
        3: lambda: increase_stat("Social Standing"),
        4: lambda: increase_stat("Education"),
        5: lambda: increase_skill("Carouse"),
        6: lambda: increase_skill("Stealth")
    }

    ENTERTAINER_SERVICE_SKILLS = {
        1: lambda: increase_skill("Art"),
        2: lambda: increase_skill("Art"),
        3: lambda: increase_skill("Carouse"),
        4: lambda: increase_skill("Deception"),
        5: lambda: increase_skill("Persuade"),
        6: lambda: increase_skill("Steward"),
    }

    ENTERTAINER_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Advocate"),
        2: lambda: increase_skill("Art"),
        3: lambda: increase_skill("Deception"),
        4: lambda: choose_science_skill(),
        5: lambda: increase_skill("Streetwise"),
        6: lambda: increase_skill("Diplomat"),
    }   
    
    ENTERTAINER_ARTIST = {
        1: lambda: increase_skill("Art"),
        2: lambda: increase_skill("Carouse"),
        3: lambda: increase_skill("Computer"),
        4: lambda: increase_skill("Gambler"),
        5: lambda: increase_skill("Persuade"),
        6: lambda: increase_skill("Trade"),
    }

    ENTERTAINER_JOURNALIST = {
        1: lambda: increase_skill("Art"),
        2: lambda: increase_skill("Comms"),
        3: lambda: increase_skill("Computers"),
        4: lambda: increase_skill("Investigate"),
        5: lambda: increase_skill("Recon"),
        6: lambda: increase_skill("Streetwise"),
    }

    ENTERTAINER_PERFORMER = {
        1: lambda: increase_skill("Art"),
        2: lambda: increase_skill("Athletics"),
        3: lambda: increase_skill("Carouse"),
        4: lambda: increase_skill("Deception"),
        5: lambda: increase_skill("Stealth"),
        6: lambda: increase_skill("Streetwise"),
    }

    ENTERTAINER_MUSTER_CASH = {
        1: 0,
        2: 0,
        3: 10000,
        4: 10000,
        5: 40000,
        6: 40000,
        7: 80000,
    }    

    def entertainer_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Entertainer")
        roll = roll_1d6()
        if roll == 1:
            log_and_print("You took 'break a leg' a bit too literally.")
            injury()

        elif roll == 2:
            log_and_print("You expose or are involved in a scandal of some sort.")

        elif roll == 3:
            log_and_print("Public opinion turns on you.  Lose one Social Standing.")
            config.values["Social Standing"] -= 1

        elif roll == 4:
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

        elif roll == 5:
            log_and_print("An investigation, tour, project, or expedition goes wrong and leaves you stranded far from home.")
            if skill_check("Streetwise", best_mental()):
                print("Hardship is a great teacher.  Gain one of the following skills at Rank 1:")
                print("1. Survival\n2. Pilot\n3. Persuade\n4. Streetwise\n")
                skill_list = ["Survival", "Pilot", "Persuade", "Streetwise"]
                choice = safe_int_input("Choose which skill, by number, to gain:\n", (1, 4))
                increase_skill(skill_list[choice - 1], set_rank=1)

        else:
            log_and_print("You are forced out by controversy or censorship.\nWhat truth did you get too close to?")
            print("You get +2 DM to your next Qualification roll.")
            config.qual_bonus += 2

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Entertainer")
            return
        if not config.keep_bonus:
            config.entertainer_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        entertainer_muster()
        check_retirement()  

    def entertainer_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            entertainer_mishap()
        elif roll == 3:
            log_and_print("You attend a controversial event or exhibition.")
            result = better_skill("Art", best_mental(), "Investigate", best_mental())
            if result >= 8:
                log_and_print("You navigate the weirdness well and gain a Social Standing.")
                config.values["Social Standing"] += 1
                get_mods()
            else:
                log_and_print("You end up in the news with a badger, a cheerleader, and strange amounts of birthday cake.  -1 Soc")
                config.values["Social Standing"] -= 1
                get_mods()
           
        elif roll == 4:
            log_and_print("You are a part of your homeworld's celebrity circles.")
            print("Gain one of the following at Rank 1:\n 1. Carouse\n2. Persuade\n3. Steward\n4. Or gain a Contact\n")
            skill_list = ["Carouse", "Persuade", "Steward"]
            choice = safe_int_input("Choose which skill/contact, by number, to gain:\n", (1, 4))
            if choice < 4:
                increase_skill(skill_list[choice - 1], set_rank=1)
            else:
                config.contacts += 1

        elif roll == 5:
            log_and_print("One of your works is especially well received and popular, making you a minor celebrity.")
            config.benefit_bonus.append(1)

        elif roll == 6:
            log_and_print("You gain a patron in the arts.")
            config.advance_bonus += 2
            config.allies += 1

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("You have the opportunity to criticize, or even bring down, a questionable political leader on your homeworld.")
            choice = safe_int_input("Will you choose to:\n1. Support the politician for no gain\n" \
            "2. Get into politics at risk to yourself", (1, 2))
            if choice == 2:
                config.enemies += 1
                result = better_skill("Art", best_mental(), "Persuade", better_skill())
                if result >= 8:
                    log_and_print("Your propaganda is effective, and you learn a few things.")
                else:
                    log_and_print("Your fumbling attempts at propaganda earn you a powerful enemy, a lot of trouble, and an education")
                increase_any_skill()
                if result < 8:
                    config.not_ejected = True
                    entertainer_mishap()

        elif roll == 9:
            log_and_print("You go on a tour of the sector, visiting several worlds.")
            config.contacts += roll_1d3()

        elif roll == 10:
            log_and_print("One of your pieces of art is stolen, and the investigation brings you into the criminal underworld.")
            skill_list = ["Streetwise", "Investigate", "Recon", "Stealth"]
            choice = safe_int_input("Gain one of the following skills at Rank 1:\n"
            "1. Streetwise\n2. Investigate\n3. Recon\n4. Stealth\n", (1, 4))
            increase_skill(skill_list[choice - 1], set_rank=1)
        
        elif roll == 11:
            log_and_print("As an artist, you lead a charmed, or at least strange, life.  You have an Unusual Event.")
            life_events(forced_roll=12)
        else:
            log_and_print("You win a prestigious award.  You are automatically promoted.")
            config.auto_advance = True

    def entertainer_muster():
        muster_rolls = config.entertainer_terms
        if config.entertainer_rank == 1 or config.entertainer_rank == 2:
            muster_rolls += 1
        if config.entertainer_rank == 3 or config.entertainer_rank == 4:
            muster_rolls += 2
        if config.entertainer_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(ENTERTAINER_MUSTER_CASH, config.entertainer_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.entertainer_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print("You gained a Contact.")
                    config.contacts += 1
                elif benefit == 2:
                    log_and_print("You moved up in society.")
                    increase_stat("Social Standing")
                elif benefit == 3:
                    log_and_print("You gained a Contact.")
                    config.contacts += 1
                elif benefit == 4:
                    log_and_print("You moved up in society.")
                    increase_stat("Social Standing")
                elif benefit == 5:
                    log_and_print("You got a bit sharper between the ears.")
                    increase_stat("Intelligence")
                elif benefit == 6:
                    log_and_print("You made a few investments and gained two Ship Shares.")
                    config.ship_shares += 2
                elif benefit == 7:
                    log_and_print("You spent some time at an elite finishing school.")
                    increase_stat("Social Standing")
                    increase_stat("Education")

    def entertainer_develop():
        config.careers.append(f"Entertainer: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 10:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            ENTERTAINER_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            ENTERTAINER_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            ENTERTAINER_ADVANCED_EDUCATION[roll]()

    if config.entertainer_terms < 1:
        qualification("Entertainer", "Intelligence", 5)

        if not config.qual:
            return
    
    config.terms += 1
    config.entertainer_terms += 1
    if "Entertainer" not in config.careers:
        print("As a Entertainer, you must choose one of the following paths:")
        print("1. Artist: Painting, sculpting, or smearing dung on things.")
        print("2. Journalist: Reporting some possibly true version of events.")
        print("3. Performer: Actor, dancer, pro-athlete, or other public performer.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Entertainer")
        if spec_choice == 1:
            config.spec_name = "Artist"
            config.spec_table = ENTERTAINER_ARTIST
            config.survival_tuple = ("Social Standing", 6) 
            config.advancement_tuple = ("Intelligence", 6)  
            config.event_log.append(f"Term{config.terms}: Entertainer: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in ENTERTAINER_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Journalist"
            config.spec_table = ENTERTAINER_JOURNALIST
            config.survival_tuple = ("Education", 7)
            config.advancement_tuple = ("Intelligence", 5)  
            config.event_log.append(f"Term{config.terms}: Entertainer: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in ENTERTAINER_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Performer"
            config.spec_table = ENTERTAINER_PERFORMER
            config.survival_tuple = ("Intelligence", 5)
            config.advancement_tuple = ("Dexterity", 7)  
            config.event_log.append(f"Term{config.terms}: Entertainer: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in ENTERTAINER_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    else:
        print("You entertain the public for four years.")
        config.careers.append(f"Term{config.terms}: Entertainer: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Entertainer: {config.spec_name}")
    
    entertainer_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        entertainer_mishap()

    if success:
        entertainer_events()
        promotion = advance(*config.advancement_tuple, config.entertainer_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            entertainer_muster()
            config.prior_careers += 1
            available_careers.remove("Entertainer")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a/an {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.entertainer_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.entertainer_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.entertainer_rank} {config.spec_name}.")
            if config.spec_name == "Artist":
                if config.entertainer_rank == 1:
                    increase_skill("Art", set_rank=1)
                elif config.entertainer_rank == 3:
                    increase_skill("Investigate", set_rank=1)
                elif config.entertainer_rank == 5:
                    increase_stat("Social Standing")
            elif config.spec_name == "Journalist":
                if config.entertainer_rank == 1:
                    increase_skill("Comms", set_rank=1)
                elif config.entertainer_rank == 2:
                    increase_skill("Investigate", set_rank=1)
                elif config.entertainer_rank == 4:
                    increase_skill("Persuade", set_rank=1)
                elif config.entertainer_rank == 6:
                    increase_stat("Social Standing")
            elif config.spec_name == "Performer":
                if config.entertainer_rank == 1:
                    increase_stat("Dexterity")
                elif config.entertainer_rank == 3:
                    increase_stat("Strength")
                elif config.entertainer_rank == 5:
                    increase_stat("Social Standing")

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 10:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                ENTERTAINER_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                ENTERTAINER_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                ENTERTAINER_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_entertainer()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_entertainer()
    else:
        config.prior_careers += 1
        entertainer_muster()

    check_retirement()

def car_marines():
    global available_careers
 
    MARINES_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Strength"),
        2: lambda: increase_stat("Dexterity"),
        3: lambda: increase_stat("Endurance"),
        4: lambda: increase_skill("Gambler"),
        5: lambda: increase_skill("Melee"),
        6: lambda: increase_skill("Melee")
    }

    MARINES_SERVICE_SKILLS = {
        1: lambda: increase_skill("Athletics"),
        2: lambda: increase_skill("Battle Dress"),
        3: lambda: increase_skill("Tactics"),
        4: lambda: increase_skill("Heavy Weapons"),
        5: lambda: increase_skill("Gun Combat"),
        6: lambda: increase_skill("Stealth"),
    }

    MARINES_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Medic"),
        2: lambda: increase_skill("Survival"),
        3: lambda: increase_skill("Explosives"),
        4: lambda: increase_skill("Engineer"),
        5: lambda: increase_skill("Pilot"),
        6: lambda: increase_skill("Medic"),
    }   
    
    MARINES_OFFICER = {
        1: lambda: increase_skill("Leadership"),
        2: lambda: increase_skill("Tactics"),
        3: lambda: increase_skill("Admin"),
        4: lambda: increase_skill("Advocate"),
        5: lambda: increase_skill("Battle Dress"),
        6: lambda: increase_skill("Leadership"),
    }   

    MARINES_SUPPORT = {
        1: lambda: increase_skill("Comms"),
        2: lambda: increase_skill("Mechanic"),
        3: lambda: increase_skill("Drive"),
        4: lambda: increase_skill("Medic"),
        5: lambda: increase_skill("Heavy Weapons"),
        6: lambda: increase_skill("Gun Combat"),
    }

    MARINES_STAR_MARINE = {
        1: lambda: increase_skill("Battle Dress"),
        2: lambda: increase_skill("Zero-G"),
        3: lambda: increase_skill("Gunnery"),
        4: lambda: increase_skill("Melee"),
        5: lambda: increase_skill("Sensors"),
        6: lambda: increase_skill("Gun Combat"),
    }

    MARINES_GROUND_ASSAULT = {
        1: lambda: increase_skill("Battle Dress"),
        2: lambda: increase_skill("Heavy Weapons"),
        3: lambda: increase_skill("Recon"),
        4: lambda: increase_skill("Melee"),
        5: lambda: increase_skill("Tactics"),
        6: lambda: increase_skill("Gun Combat"),
    }

    MARINES_MUSTER_CASH = {
        1: 2000,
        2: 5000,
        3: 5000,
        4: 10000,
        5: 20000,
        6: 30000,
        7: 40000,
    }    

    def marines_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Marines")
        roll = roll_1d6()
        if roll == 1:
            log_and_print(f"Severely injured in action.")
            choice = safe_int_input("You must choose to:\n1. Accept a roll of '2' on the injury table.\n2. Roll twice and take the lower result.\n", (1, 2))
            if choice == 1:
                injury(2)
            else:
                injury_roll_twice()

        elif roll == 2:
            log_and_print("A mission goes wrong.  You, and several others, are captured and mistreated by a sadistic jailer.")
            log_and_print("The jailer remains your enemy and your decreased health reminds you why.")
            config.enemies += 1
            config.values["Strength"] -= 1
            config.values["Dexterity"] -= 1
            get_mods()

        elif roll == 3:
            log_and_print("A mission goes wrong and you are trapped behind enemy lines.")
            log_and_print("You learn a few things, but are discharged for your failure.")
            choice = safe_int_input("Choose to improve either:\n1. Stealth\n2. Survival\n", (1, 2))
            if choice == 1:
                increase_skill("Stealth")
            elif choice == 2:
                increase_skill("Survival")

        elif roll == 4:
            log_and_print("You are ordered to take part in a black ops mission that goes against your conscience.")
            choice = safe_int_input("Do you choose to:\n1. Follow orders\n2. Refuse and face repercussions\n")
            if choice == 1:
                log_and_print("For the lone survivor of your raid, it was the most important day of their life.")
                log_and_print("For you, it was Tuesday.")
                config.enemies += 1
                config.not_ejected = True
            else:
                log_and_print("You are labelled a traitor and coward, then ejected from the service.")

        elif roll == 5:
            log_and_print("You are tormented by or quarrel with an officer or fellow marine.  Your rival drives you out of the service.")
            config.rivals += 1

        else:
            injury()

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Marines")
            return
        if not config.keep_bonus:
            config.marines_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        marines_muster()
        check_retirement()   

    def marines_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            marines_mishap()
        elif roll == 3:
            log_and_print("Trapped behind enemy lines, you have to survive on your own.")
            choice = safe_int_input("Gain one of the following skills:\n"
                "1. Survival 1\n2. Stealth 1\n3. Deception 1\n4. Streetwise 1\n", (1, 4))
            skill_list = ["Survival", "Stealth", "Deception", "Streetwise"]
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 4:
            log_and_print("You are assigned to the security staff of a space station..")
            choice = safe_int_input("Increase one of the following skills:\n1. Vacc Suit\n2. Zero-G", (1, 2))
            skill_list = ["Vacc Suit", "Zero-G"]
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 5:
            log_and_print("You are given advanced training in a specialized field.")
            learning = roll_2d6() + config.mods["Education"]
            if learning < 8:
                log_and_print("The education doesn't really stick, but the teacher was very attractive.")
            else:
                print("You're an excellent student.  Gain any skill at Rank 1.")
                increase_any_skill(set_rank=1)

        elif roll == 6:
            log_and_print("You are assigned to assault an enemy fortress.")
            choice = safe_int_input("Will you roll for:\n1. Melee\n2.Gun Combat\n", (1, 2))
            if choice == 1:
                result = skill_check("Melee", best_of_two("Strength", "Dexterity"))
            elif choice == 2:
                result = skill_check("Gun Combat", "Dexterity")
            if result < 8:
                log_and_print("You fail the assault and are injured in the process.")
                choice = safe_int_input("Choose a physical stat to reduce by one:\n1. Strength\n2. Dexterity\n3. Endurance\n")
                config.values[physical_stats[choice - 1]] -= 1
                get_mods()
            else:
                log_and_print("The offensive is a smashing success.")
                choice = safe_int_input("Choose a skill to increase:\n1. Tactics\n2.Leadership\n", (1, 2))
                skill_list = ["Tactics", "Leadership"]
                increase_skill(skill_list[choice - 1])

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("You are on the front lines of a planetary assault and occupation.")
            choice = safe_int_input("Gain one of the following skills at Rank 1:\n"
                "1. Recon 1\n2. Gun Combat 1\n3. Leadership 1\n4. Comms 1\n", (1, 4))
            skill_list = ["Recon", "Gun Combat", "Leadership", "Comms"]
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 9:
            log_and_print("A mission goes disastrously wrong due to your commander's error or incompetence.")
            choice = safe_int_input("Will you:\n1. Turn him in to advance your station\n2. Cover for him to gain his loyalty\n", (1, 2))
            if choice == 1:
                log_and_print("You write a report that gets him in trouble and gets you two points on your performance evaluation.")
                config.advance_bonus += 2
            else:
                log_and_print("Congratulations on your new, corrupt, incompetent ally.")
                config.allies += 1

        elif roll == 10:
            log_and_print("You are assigned to a black ops mission and get +2 to your next Advancement roll.")
            config.advance_bonus += 2
        
        elif roll == 11:
            log_and_print("Your commanding officer takes an interest in your career.")
            choice = safe_int_input("Choose either:\n1. Gain Tactics 1\n2. +4 DM to your next Advancement roll\n", (1, 2))
            if choice == 1:
                increase_skill("Tactics", set_rank=1)
            else:
                config.advance_bonus += 4

        else:
            log_and_print("You display heroism in battle.  You are automatically promoted.")
            config.auto_advance = True

    def marines_muster():
        muster_rolls = config.marines_terms
        if config.marines_rank == 1 or config.marines_rank == 2:
            muster_rolls += 1
        if config.marines_rank == 3 or config.marines_rank == 4:
            muster_rolls += 2
        if config.marines_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(MARINES_MUSTER_CASH, config.marines_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.marines_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    armour_benefit()
                elif benefit == 2:
                    log_and_print("You got a little smarter in the field when the alternative was getting deader.")
                    increase_stat("Intelligence")
                    update_char()
                elif benefit == 3:
                    log_and_print("You stayed awake during a few of your classes.")
                    increase_stat("Education")
                    update_char()
                elif benefit == 4:
                    weapon_benefit()
                elif benefit == 5:
                    armour_benefit()
                elif benefit == 6:
                    choice = safe_int_input("Choose:\n1. +1 Endurance\n2. Armour\n")
                    if choice == 1:
                        log_and_print("You stayed in shape after basic.")
                        increase_stat("Endurance")
                    else:
                        armour_benefit()
                elif benefit == 7:
                    log_and_print("Being the star of several medal-pinning ceremonies gave you contacts in high society.")
                    increase_stat("Social Standing", 2)

    def marines_develop():
        config.careers.append(f"Marines: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            MARINES_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            MARINES_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            MARINES_ADVANCED_EDUCATION[roll]()

    if not config.drafted and config.marines_terms < 1:
        if config.age >= 30:
            config.qual_bonus -= 2
        qualification("Marines", "Endurance", 6)

        if not config.qual:
            return
    
    config.terms += 1
    config.marines_terms += 1
    config.drafted = False

    if "Marines" not in config.careers:
        print("As an Marines recruit, you must choose one of the following paths:")
        print("1. Support: Doing the less glamorous work in the background.")
        print("2. Star Marine: Fighting boarding actions and capturing enemy ships.")
        print("3. Ground Assault: They kicked you out of a spacecraft and said 'capture that planet'.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Marines")
        if spec_choice == 1:
            config.spec_name = "Support"
            config.spec_table = MARINES_SUPPORT
            config.survival_tuple = ("Endurance", 5) 
            config.advancement_tuple = ("Education", 7)  
            if config.prior_careers < 1:
                for effect in MARINES_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Star Marine"
            config.spec_table = MARINES_STAR_MARINE
            config.survival_tuple = ("Endurance", 6)
            config.advancement_tuple = ("Education", 6)  
            if config.prior_careers < 1:
                for effect in MARINES_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Ground Assault"
            config.spec_table = MARINES_GROUND_ASSAULT
            config.survival_tuple = ("Endurance", 7)
            config.advancement_tuple = ("Education", 5)  
            if config.prior_careers < 1:
                for effect in MARINES_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False
        choice = safe_int_input("Gain a skill at Rank 1:\n1. Melee\n2. Gun Combat\n", (1, 2))
        skill_list = ["Melee", "Gun Combat"]
        increase_skill(skill_list[choice - 1], set_rank=1)

    if config.spec_name != "Officer":
        print("It occurs to you that shining your own boots may be for suckers.")  
        commission = safe_choice("Want to apply for a commission? (y/n)\n", ("y", "n"))
        if commission == "y":
            attempt = config.mods["Social Standing"] + roll_2d6()
            if attempt >= 8:
                config.spec_name = "Officer"
                config.spec_table = MARINES_OFFICER
                log_and_print("You become a commissioned officer.")
            else:
                log_and_print("Your application to officer school is filed very deeply.")

    print("Four years of duty await.")
    config.careers.append(f"Term{config.terms}: Marines: {config.spec_name}.")
    config.event_log.append(f"Term{config.terms}: Marines: {config.spec_name}")
    
    marines_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        marines_mishap()

    if success:
        marines_events()
        promotion = advance(*config.advancement_tuple, config.marines_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            marines_muster()
            config.prior_careers += 1
            available_careers.remove("Marines")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        if promotion == 1:
            config.marines_rank += 1
            if "Officer" in config.spec_name:
                config.marines_officer_rank += 1
            else:
                config.marines_nco_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.marines_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.marines_rank} {config.spec_name}.")
            if config.marines_nco_rank == 1:
                increase_skill("Recon", set_rank=1)
            elif config.marines_nco_rank == 3:
                increase_skill("Leadership", set_rank=1)
            elif config.marines_nco_rank == 5:
                increase_stat("Endurance")

            else:
                if config.marines_officer_rank == 1:
                    increase_skill("Leadership", set_rank=1)
                elif config.marines_officer_rank == 3:
                    increase_skill("Tactics", set_rank=1)
                elif config.marines_officer_rank == 5:
                    if config.values["Social Standing"] < 10:
                        config.values["Social Standing"] = 10
                    else:
                        config.values["Social Standing"] += 1

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 8:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                MARINES_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                MARINES_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                MARINES_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        config.event_log.append("You were so successful at your job, you couldn't leave.")
        car_marines()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_marines()
    else:
        config.prior_careers += 1
        marines_muster()

    check_retirement()


def car_merchants():
    global available_careers

    MERCHANTS_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Strength"),
        2: lambda: increase_stat("Dexterity"),
        3: lambda: increase_stat("Endurance"),
        4: lambda: increase_stat("Intelligence"),
        5: lambda: increase_skill("Melee"),
        6: lambda: increase_skill("Streetwise"),
    }

    MERCHANTS_SERVICE_SKILLS = {
        1: lambda: increase_skill("Drive"),
        2: lambda: increase_skill("Vacc Suit"),
        3: lambda: increase_skill("Broker"),
        4: lambda: increase_skill("Steward"),
        5: lambda: increase_skill("Comms"),
        6: lambda: increase_skill("Persuade"),
    }

    MERCHANTS_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Social Sciences"),
        2: lambda: increase_skill("Astrogation"),
        3: lambda: increase_skill("Computers"),
        4: lambda: increase_skill("Pilot"),
        5: lambda: increase_skill("Admin"),
        6: lambda: increase_skill("Advocate"),
    }   
    
    MERCHANTS_MERCHANT_MARINE = {
        1: lambda: increase_skill("Pilot"),
        2: lambda: increase_skill("Vacc Suit"),
        3: lambda: increase_skill("Zero-G"),
        4: lambda: increase_skill("Mechanic"),
        5: lambda: increase_skill("Engineer"),
        6: lambda: increase_skill("Gunner"),
    }

    MERCHANTS_FREE_TRADER = {
        1: lambda: increase_skill("Pilot"),
        2: lambda: increase_skill("Vacc Suit"),
        3: lambda: increase_skill("Zero-G"),
        4: lambda: increase_skill("Mechanic"),
        5: lambda: increase_skill("Engineer"),
        6: lambda: increase_skill("Sensors"),
    }

    MERCHANTS_BROKER = {
        1: lambda: increase_skill("Admin"),
        2: lambda: increase_skill("Advocate"),
        3: lambda: increase_skill("Broker"),
        4: lambda: increase_skill("Streetwise"),
        5: lambda: increase_skill("Deception"),
        6: lambda: increase_skill("Persuade"),
    }

    MERCHANTS_MUSTER_CASH = {
        1: 1000,
        2: 5000,
        3: 10000,
        4: 20000,
        5: 20000,
        6: 40000,
        7: 40000,
    }    

    def merchants_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Merchants")
        roll = roll_1d6()
        if roll == 1:
            log_and_print(f"You are injured.")
            injury()

        elif roll == 2:
            log_and_print("You are bankrupted by a rival.  You lose all benefits from this career.")
            config.rivals += 1
            config.lose_all_benefits = True

        elif roll == 3:
            log_and_print("A sudden war destroys your trade routes and contacts, forcing you to flee that region of space.")
            choice = safe_int_input("Choose to gain:\n1. Gun Combat\n2. Pilot\n", (1, 2))
            skill_list = ["Gun Combat", "Pilot"]
            increase_skill(skill_list[choice - 1])

        elif roll == 4:
            log_and_print("Your ship or starport is destroyed by criminals who are now your enemy.")
            config.enemies += 1

        elif roll == 5:
            log_and_print("Imperial trade restrictions force you out of business.  You may automatically take Rogue for your next career.")
            config.rogue_auto_qualify = True            

        else:
            log_and_print("A series of bad deals and decisions force you into bankruptcy.  You salvage what you can.")
            config.keep_bonus = True

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Merchants")
            return
        if not config.keep_bonus:
            config.merchants_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        merchants_muster()
        check_retirement() 

    def merchants_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            merchants_mishap()
        elif roll == 3:
            log_and_print("You are offered an opportunity to smuggle illegal items onto a planet.")
            choice = safe_choice("Do you accept the offer? (y/n)\n", ("y", "n"))
            if choice == "y":
                skill = safe_int_input("Roll:\n1. Deception\n2. Persuade")
                skill_list = ["Deception", "Persuade"]
                result = skill_check(skill_list[skill - 1], best_mental())
                if result >= 8:
                    log_and_print("Your mission is a success.")
                    config.merchants_terms += 1
                    increase_skill("Streetwise", set_rank=1)
                else:
                    log_and_print("Your contraband gets seized.")
            else:
                log_and_print("You seriously disappoint a criminal who holds a grudge.")
                config.enemies += 1
            
        elif roll == 4:
            log_and_print("You learn a lot from your time with suppliers and spacers.")
            choice = safe_int_input("Gain one of the following at Rank 1:\n1. Trade\n2. Engineer\n3. Animals\n4. Social Sciences", (1, 4))
            skill_list = ["Trade", "Engineer", "Animals", "Social Sciences"]
            increase_skill(skill_list[choice - 1], set_rank=1)            

        elif roll == 5:
            log_and_print("You get the opportunity to gamble your fortune on a potentially lucrative deal.")
            choice = safe_choice("Will you risk your benefits? (y/n)\n", ("y", "n"))
            if choice == "y":
                benefits = config.merchants_terms
                if config.merchants_rank == 1 or config.merchants_rank == 2:
                    benefits += 1
                elif config.merchants_rank == 3 or config.merchants_rank == 4:
                    benefits += 2
                elif config.merchants_rank >= 5:
                    benefits += 3
                choice = safe_int_input(f"You have {benefits} benefit rolls to gamble.\nChoose how many: ", (1, benefits))
                skill_list = ["Gambler", "Broker"]
                skill = safe_int_input("Roll:\n1. Gambler\n2. Broker\n", (1, 2))
                result = skill_check(skill_list[skill - 1], best_mental())
                if result >= 8:
                    config.merchants_terms += math.ceil(choice / 2)
                    print(f"You gain {math.ceil(choice / 2)} benefit rolls.")
                    config.event_log.append("Your bet pays off.")
                elif result < 8:
                    config.merchants_terms -= choice
                    print(f"You lose {choice} benefit rolls.")
                    config.event_log.append("You lose your shirt.")
            else:
                log_and_print("You play it safe.")

        elif roll == 6:
            log_and_print("You make an unexpected connection outside your normal circles.  Gain a Contact.")
            config.contacts += 1

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("You are embroiled in legal trouble and have to learn a few loopholes.")
            skill_list = ["Advocate","Admin", "Diplomat", "Investigate"]
            print(f"You currently have:\nAdvocate: {skills["Advocate"]}, Admin: {skills["Admin"]}\n"
                  f"Diplomat: {skills["Diplomat"]}, Investigate: {skills["Investigate"]}\n")
            choice = safe_int_input("Choose a skill to gain at Rank 1:\n1. Advocate\n2. Admin\n3. Diplomat\n4. Investigate\n", (1, 4))
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 9:
            log_and_print("You are given advanced training in a specialized field.")
            learning = roll_2d6() + config.mods["Education"]
            if learning < 8:
                log_and_print("The education doesn't really stick, but the teacher was very attractive.")
            else:
                increase_existing_skill()

        elif roll == 10:
            log_and_print("A good deal ensures you are living the high life for a few years.  You get +1 DM to a benefit roll.")
            config.benefit_bonus.append(1)
        
        elif roll == 11:
            log_and_print("You befriend a useful ally.")
            config.allies += 1
            choice = safe_int_input("Choose either:\n1. Increase Carouse by one level\n2. +4 DM to your next Advancement roll\n", (1, 2))
            if choice == 1:
                increase_skill("Carouse")
            else:
                config.advance_bonus += 4

        else:
            log_and_print("Your business or ship thrives.  You are automatically promoted.")
            config.auto_advance = True

    def merchants_muster():
        muster_rolls = config.merchants_terms
        if config.lose_all_benefits:
            print("You have lost your benefits.")
            config.lose_all_benefits = False
            return
        elif config.merchants_rank in (1, 2):
            muster_rolls += 1
        elif config.merchants_rank in (3, 4):
            muster_rolls += 2
        elif config.merchants_rank >= 5:
            muster_rolls += 3
        while muster_rolls > 0:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(MERCHANTS_MUSTER_CASH, config.merchants_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.merchants_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    weapon_benefit("Blade")
                elif benefit == 2:
                    log_and_print("You got a little smarter in the field when the alternative was getting deader.")
                    increase_stat("Intelligence")
                    get_mods()
                elif benefit == 3:
                    log_and_print("You learned something useful for a change.")
                    increase_stat("Education")
                    get_mods()
                elif benefit == 4:
                    weapon_benefit("Gun")
                elif benefit == 5:
                    log_and_print("You made some investments and gained a Ship Share.")
                    config.ship_shares += 1
                else:
                    log_and_print("You are offered a significant stake in a Free Trader.")
                    choice = safe_int_input("Will you gain:\n1. 5 Ship Shares in a Free Trader\n2. 2 Ship Shares towards another vessel\n")
                    if choice == 1:
                        config.ship_shares += 5
                        log_and_print("You accept.")
                    else:
                        config.ship_shares += 2
                        log_and_print("You leverage your stake to get two, more flexible, Ship Shares.")

    def merchants_develop():
        config.careers.append(f"Merchants: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            MERCHANTS_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            MERCHANTS_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            MERCHANTS_ADVANCED_EDUCATION[roll]()

    if not config.drafted and "Merchants" not in config.careers:
        qualification("Merchants", "Intelligence", 4)

        if not config.qual:
            return
    
    config.terms += 1
    config.merchants_terms += 1
    if "Merchants" not in config.careers and not config.drafted:
        print("As a Merchant, you must choose one of the following paths:")
        print("1. Merchant Marine, guarding cargo against pirates and boredom.")
        print("2. Free Trader, hauling freight between stars.")
        print("3. Broker, wheeling and dealing.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Merchants")
        if spec_choice == 1:
            config.spec_name = "Merchant Marine"
            config.spec_table = MERCHANTS_MERCHANT_MARINE
            config.survival_tuple = ("Education", 5) 
            config.advancement_tuple = ("Intelligence", 7)  
            config.event_log.append(f"Term{config.terms}: Merchants: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in MERCHANTS_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Free Trader"
            config.spec_table = MERCHANTS_FREE_TRADER
            config.survival_tuple = ("Dexterity", 6)
            config.advancement_tuple = ("Intelligence", 6)  
            config.event_log.append(f"Term{config.terms}: Merchants: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in MERCHANTS_SERVICE_SKILLS.values():
                    effect() 
                config.basic_training = False   
    
        if spec_choice == 3:
            config.spec_name = "Broker"
            config.spec_table = MERCHANTS_BROKER
            config.survival_tuple = ("Education", 5)
            config.advancement_tuple = ("Intelligence", 7)  
            config.event_log.append(f"Term{config.terms}: Merchants: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in MERCHANTS_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    elif config.drafted:
            config.drafted = False
            log_and_print("You are drafted into service in the Merchant Marines.")
            config.careers.append("Merchants")
            config.spec_name = "Merchant Marine"
            config.spec_table = MERCHANTS_MERCHANT_MARINE
            config.survival_tuple = ("Education", 5) 
            config.advancement_tuple = ("Intelligence", 7)    
            config.event_log.append(f"Term{config.terms}: Merchants: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in MERCHANTS_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    else:
        print("You sign up for another term of space capitalism.")
        config.careers.append(f"Term{config.terms}: Merchants: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Merchants: {config.spec_name}")
    
    merchants_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        merchants_mishap()

    if success:
        merchants_events()
        promotion = advance(*config.advancement_tuple, config.merchants_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            merchants_muster()
            config.prior_careers += 1
            available_careers.remove("Merchants")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.merchants_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.merchants_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.merchants_rank} {config.spec_name}.")
            if config.spec_name == "Merchant Marine":
                if config.merchants_rank == 1:
                    increase_skill("Mechanic", set_rank=1)
                elif config.merchants_rank == 4:
                    increase_skill("Pilot", set_rank=1)
                elif config.merchants_rank == 5:
                    increase_stat("Social Standing")

            elif config.spec_name == "Free Trader":
                if config.merchants_rank == 1:
                    increase_skill("Persuade", set_rank=1)
                elif config.merchants_rank == 3:
                    increase_skill("Jack of all Trades", set_rank=1)
                
            else:
                if config.merchants_rank == 1:
                    increase_skill("Broker", set_rank=1)
                elif config.merchants_rank == 3:
                    increase_skill("Streetwise", set_rank=1)

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 8:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                MERCHANTS_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                MERCHANTS_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                MERCHANTS_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_merchants()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_merchants()
    else:
        config.prior_careers += 1
        merchants_muster()

    check_retirement()

def car_navy():
    global available_careers
    
    NAVY_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Strength"),
        2: lambda: increase_stat("Dexterity"),
        3: lambda: increase_stat("Endurance"),
        4: lambda: increase_stat("Intelligence"),
        5: lambda: increase_stat("Education"),
        6: lambda: increase_stat("Social Standing")
    }

    NAVY_SERVICE_SKILLS = {
        1: lambda: increase_skill("Pilot"),
        2: lambda: increase_skill("Vacc Suit"),
        3: lambda: increase_skill("Zero-G"),
        4: lambda: increase_skill("Gunner"),
        5: lambda: increase_skill("Mechanic"),
        6: lambda: increase_skill("Gun Combat"),
    }

    NAVY_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Remote Operations"),
        2: lambda: increase_skill("Astrogation"),
        3: lambda: increase_skill("Engineer"),
        4: lambda: increase_skill("Computers"),
        5: lambda: increase_skill("Navigation"),
        6: lambda: increase_skill("Admin"),
    }   
    
    NAVY_OFFICER = {
        1: lambda: increase_skill("Leadership"),
        2: lambda: increase_skill("Tactics"),
        3: lambda: increase_skill("Pilot"),
        4: lambda: increase_skill("Melee"),
        5: lambda: increase_skill("Admin"),
        6: lambda: increase_skill("Tactics"),
    }   

    NAVY_CREW = {
        1: lambda: increase_skill("Comms"),
        2: lambda: increase_skill("Mechanic"),
        3: lambda: increase_skill("Gun Combat"),
        4: lambda: increase_skill("Sensors"),
        5: lambda: increase_skill("Melee"),
        6: lambda: increase_skill("Vacc Suit"),
    }

    NAVY_ENG_GUN = {
        1: lambda: increase_skill("Engineer"),
        2: lambda: increase_skill("Mechanic"),
        3: lambda: increase_skill("Sensors"),
        4: lambda: increase_skill("Engineer"),
        5: lambda: increase_skill("Gunner"),
        6: lambda: increase_skill("Computers"),
    }

    NAVY_FLIGHT = {
        1: lambda: increase_skill("Pilot"),
        2: lambda: increase_skill("Flyer"),
        3: lambda: increase_skill("Gunner"),
        4: lambda: increase_skill("Pilot"),
        5: lambda: increase_skill("Astrogation"),
        6: lambda: increase_skill("Zero-G"),
    }

    NAVY_MUSTER_CASH = {
        1: 1000,
        2: 5000,
        3: 5000,
        4: 10000,
        5: 20000,
        6: 50000,
        7: 50000,
    }    

    def navy_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Navy")
        roll = roll_1d6()
        if roll == 1:
            log_and_print(f"Severely injured in action.")
            choice = safe_int_input("You must choose to:\n1. Accept a roll of '2' on the injury table.\n2. Roll twice and take the lower result.\n", (1, 2))
            if choice == 1:
                injury(2)
            else:
                injury_roll_twice()

        elif roll == 2:
            log_and_print("Placed in cryogenic storage, you are then revived improperly.  You are discharged due to health issues.")
            config.values["Strength"] -= 1
            config.values["Dexterity"] -= 1
            config.values["Endurance"] -= 1
            get_mods()

        elif roll == 3:
            log_and_print("During a battle, defeat or victory depends on your actions.")
            if config.spec_name == "Engineer/Gunner":
                choice = safe_int_input("Roll:\n1. Sensors\n2. Gunner\n", (1, 2))
                if choice == 1:
                    result = skill_check("Sensors", best_mental())
                else:
                    result = skill_check("Gunner", "Dexterity")
            elif config.spec_name == "Crew":
                choice = safe_int_input("Roll:\n1. Mechanic\n2. Vacc Suit\n", (1, 2))
                if choice == 1:
                    result = skill_check("Mechanic", best_mental())
                else:
                    result = skill_check("Vacc Suit", best_physical())
            elif config.spec_name == "Pilot":
                choice = safe_int_input("Roll:\n1. Pilot\n2. Tactics\n", (1, 2))
                if choice == 1:
                    result = skill_check("Pilot", best_of_two("Dexterity", "Intelligence"))
                else:
                    result = skill_check("Tactics", best_mental())
            if result >= 8:
                log_and_print("After saving the day, you still catch enough blame to be honourably discharged.")
                config.keep_bonus = True
            else:
                log_and_print("After an absolute disaster, you are court-martialed and discharged.")

        elif roll == 4:
            log_and_print("You are blamed for an accident that causes the death of several crew members.")
            choice = safe_choice("Was it your fault? (y/n)", ("y", "n"))
            if choice == "y":
                print("Your guilt drives you to excel.  Take an extra roll on one of the skill tables.")
                if values["Education"] >= 8:
                    print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                    choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

                else:
                    print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                    choice = safe_int_input("1, 2, or 3?\n", (1, 3))
                roll = roll_1d6()
                if choice == 1:
                    NAVY_PERSONAL_DEVELOPMENT[roll]()

                elif choice == 2:
                    NAVY_SERVICE_SKILLS[roll]()

                elif choice == 3:
                    config.spec_table[roll]()

                elif choice == 4:
                    NAVY_ADVANCED_EDUCATION[roll]()

            else:
                log_and_print("The officer who accused you becomes your enemy and you are discharged with pay.")
                config.keep_bonus = True

        elif roll == 5:
            log_and_print("You are tormented by or quarrel with an officer or fellow crewman.  Your rival drives you out of the service.")
            config.rivals += 1

        else:
            injury()

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Navy")
            return
        if not config.keep_bonus:
            config.navy_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        navy_muster()
        check_retirement()   

    def navy_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            navy_mishap()
        elif roll == 3:
            log_and_print("You join a gambling circle on board.")
            choice = safe_int_input("Gain one of the following skills:\n"
                "1. Gambler 1\n2. Deception 1", (1, 2))
            skill_list = ["Gambler", "Deception"]
            increase_skill(skill_list[choice - 1], set_rank=1)
            choice = safe_choice("Would you like to wager one of your benefit rolls? (y/n)\n", ("y", "n"))
            if choice == "y":
                result = skill_check("Gambler", best_mental())
                if result >= 8:
                    log_and_print("You win big.")
                    config.navy_terms += 1
                else:
                    log_and_print("You get taken to the cleaners.")
                    config.navy_terms -= 1

        elif roll == 4:
            log_and_print("You are given a special duty or assignment.  You get +1 DM to a benefit roll.")
            config.benefit_bonus.append(1)
            
        elif roll == 5:
            log_and_print("You are given advanced training in a specialized field.")
            learning = roll_2d6() + config.mods["Education"]
            if learning < 8:
                log_and_print("The education doesn't really stick, but the teacher was very attractive.")
            else:
                print("You're an excellent student.  Improve any skill you already have.")
                increase_existing_skill()

        elif roll == 6:
            log_and_print("Your vessel participates in a notable military engagement.")
            choice = safe_int_input("Choose a skill to gain at Rank 1:\n1. Sensors\n2. Engineer\n3. Gunnery\n4. Pilot\n", (1, 4))
            skill_list = ["Sensors", "Engineer", "Gunnery", "Pilot"]
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("Your vessel participates in a diplomatic mission.")
            choice = safe_int_input("Gain one of the following skills at Rank 1:\n"
                "1. Recon 1\n2. Diplomat 1\n3. Steward 1\n4. Or gain a Contact\n", (1, 4))
            if choice < 4:
                skill_list = ["Recon", "Diplomat", "Steward"]
                increase_skill(skill_list[choice - 1], set_rank=1)
            else:
                log_and_print("You gain a contact.")
                config.contacts += 1

        elif roll == 9:
            log_and_print("You foil an attempted crime on board. You gain the criminal as an enemy, but also get a good evaluation.")
            config.enemies += 1
            config.advance_bonus += 2
            

        elif roll == 10:
            log_and_print("You have the opportunity to abuse your position for profit.")
            choice = safe_choice("Will you:\n1. Do crimes for profit\n2. Refuse and be recognized for your service\n", (1, 2))
            if choice == 1:
                config.navy_terms += 1
                log_and_print("You make an illicit profit.")
            else:
                config.advance_bonus += 2
                log_and_print("You get a good evaluation.")
        
        elif roll == 11:
            log_and_print("Your commanding officer takes an interest in your career.")
            choice = safe_int_input("Choose either:\n1. Gain Tactics 1\n2. +4 DM to your next Advancement roll\n", (1, 2))
            if choice == 1:
                increase_skill("Tactics", set_rank=1)
            else:
                config.advance_bonus += 4

        else:
            log_and_print("You display heroism in battle.  You are automatically promoted.")
            config.auto_advance = True

    def navy_muster():
        muster_rolls = config.navy_terms
        if config.navy_rank == 1 or config.navy_rank == 2:
            muster_rolls += 1
        if config.navy_rank == 3 or config.navy_rank == 4:
            muster_rolls += 2
        if config.navy_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            if config.benefit_bonus:
                print(f"You will receive a +{config.benefit_bonus[-1]} bonus to the roll.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(NAVY_MUSTER_CASH, config.navy_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.navy_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    if "Air/Raft" not in config.starting_items:
                        choice = safe_int_input("Choose to gain:\n1. An air/raft vehicle\n2. One ship share\n", (1, 2))
                        if choice == 1:
                            config.starting_items.append("Air/Raft")
                        else:
                            config.ship_shares += 1
                    else:
                        increase_skill("Flyer")
                elif benefit == 2:
                    log_and_print("You got a little smarter in the field when the alternative was getting deader.")
                    increase_stat("Intelligence")
                    update_char()
                elif benefit == 3:
                    choice = safe_int_input("Choose:\n1. +1 Education\n2. 2 Ship Shares", (1, 2))
                    if choice == 1:
                        log_and_print("You stayed awake during a few of your classes.")
                        increase_stat("Education")
                        get_mods()
                    else:
                        log_and_print("You make a few investments and gain two Ship Shares.")
                        config.ship_shares += 2
                elif benefit == 4:
                    weapon_benefit()
                elif benefit == 5:
                    tas_member()
                elif benefit == 6:
                    choice = safe_int_input("Choose:\n1. Ship's Boat\n2. 2 Ship Shares", (1, 2))
                    if choice == 1:
                        log_and_print("You gain a Ship's Boat.")
                        config.starting_items.append("Ship's Boat")
                    else:
                        log_and_print("You make a few investments and gain two Ship Shares.")
                        config.ship_shares += 2
                elif benefit == 7:
                    log_and_print("Being the star of several medal-pinning ceremonies gave you contacts in high society.")
                    increase_stat("Social Standing", 2)

    def navy_develop():
        config.careers.append(f"Navy: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            NAVY_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            NAVY_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            NAVY_ADVANCED_EDUCATION[roll]()

    if not config.drafted and config.navy_terms < 1:
        if config.age >= 34:
            config.qual_bonus -= 2
        qualification("Navy", "Intelligence", 6)

        if not config.qual:
            return
    
    config.terms += 1
    config.navy_terms += 1
    config.drafted = False

    if "Navy" not in config.careers:
        print("As an Navy recruit, you must choose one of the following paths:")
        print("1. Line/Crew: A typical generalist naval career.")
        print("2. Engineer/Gunnery: Working wrenches and/or turrets.")
        print("3. Flight: You've listened to a lot of Kenny Loggins in the cockpit.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Navy")
        if spec_choice == 1:
            config.spec_name = "Crew"
            config.spec_table = NAVY_CREW
            config.survival_tuple = ("Intelligence", 5) 
            config.advancement_tuple = ("Education", 7)  
            if config.prior_careers < 1:
                for effect in NAVY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Engineer/Gunnery"
            config.spec_table = NAVY_ENG_GUN
            config.survival_tuple = ("Intelligence", 6)
            config.advancement_tuple = ("Education", 6)  
            if config.prior_careers < 1:
                for effect in NAVY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Pilot"
            config.spec_table = NAVY_FLIGHT
            config.survival_tuple = ("Dexterity", 7)
            config.advancement_tuple = ("Education", 5)  
            if config.prior_careers < 1:
                for effect in NAVY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    if config.spec_name != "Officer":
        print("It occurs to you that shining your own boots may be for suckers.")  
        commission = safe_choice("Want to apply for a commission? (y/n)\n", ("y", "n"))
        if commission == "y":
            attempt = config.mods["Social Standing"] + roll_2d6()
            if attempt >= 8:
                config.spec_name = "Officer"
                config.spec_table = NAVY_OFFICER
                log_and_print("You become a commissioned officer.")
            else:
                log_and_print("Your application to officer school is filed very deeply.")

    print("Four years of duty await.")
    config.careers.append(f"Term{config.terms}: Navy: {config.spec_name}.")
    config.event_log.append(f"Term{config.terms}: Navy: {config.spec_name}")
    
    navy_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        navy_mishap()

    if success:
        navy_events()
        promotion = advance(*config.advancement_tuple, config.navy_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            navy_muster()
            config.prior_careers += 1
            available_careers.remove("Navy")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        if promotion == 1:
            config.navy_rank += 1
            if "Officer" in config.spec_name:
                config.navy_officer_rank += 1
            else:
                config.navy_nco_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.navy_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.navy_rank} {config.spec_name}.")
            if config.navy_nco_rank == 1:
                increase_skill("Recon", set_rank=1)
            elif config.navy_nco_rank == 3:
                increase_skill("Leadership", set_rank=1)
            elif config.navy_nco_rank == 5:
                increase_stat("Endurance")

            else:
                if config.navy_officer_rank == 1:
                    increase_skill("Leadership", set_rank=1)
                elif config.navy_officer_rank == 3:
                    increase_skill("Tactics", set_rank=1)
                elif config.navy_officer_rank == 5:
                    if config.values["Social Standing"] < 10:
                        config.values["Social Standing"] = 10
                    else:
                        config.values["Social Standing"] += 1

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 8:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                NAVY_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                NAVY_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                NAVY_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        config.event_log.append("You were so successful at your job, you couldn't leave.")
        car_navy()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_navy()
    else:
        config.prior_careers += 1
        navy_muster()

    check_retirement()


def car_nobility():
    global available_careers

    NOBILITY_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_skill("Carouse"),
        2: lambda: increase_stat("Education"),
        3: lambda: increase_skill("Deception"),
        4: lambda: increase_stat("Dexterity"),
        5: lambda: increase_skill("Melee"),
        6: lambda: increase_stat("Social Standing")
    }

    NOBILITY_SERVICE_SKILLS = {
        1: lambda: increase_skill("Admin"),
        2: lambda: increase_skill("Advocate"),
        3: lambda: increase_skill("Comms"),
        4: lambda: increase_skill("Steward"),
        5: lambda: increase_skill("Diplomat"),
        6: lambda: increase_skill("Persuade"),
    }

    NOBILITY_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Admin"),
        2: lambda: increase_skill("Advocate"),
        3: lambda: increase_skill("Language"),
        4: lambda: increase_skill("Leader"),
        5: lambda: increase_skill("Diplomat"),
        6: lambda: increase_skill("Computers"),
    }   
    
    NOBILITY_ADMINISTRATOR = {
        1: lambda: increase_skill("Admin"),
        2: lambda: increase_skill("Advocate"),
        3: lambda: increase_skill("Broker"),
        4: lambda: increase_skill("Diplomat"),
        5: lambda: increase_skill("Leader"),
        6: lambda: increase_skill("Persuade"),
    }

    NOBILITY_DIPLOMAT = {
        1: lambda: increase_skill("Advocate"),
        2: lambda: increase_skill("Carouse"),
        3: lambda: increase_skill("Comms"),
        4: lambda: increase_skill("Steward"),
        5: lambda: increase_skill("Diplomat"),
        6: lambda: increase_skill("Deception"),
    }

    NOBILITY_DILETTANTE = {
        1: lambda: increase_skill("Carouse"),
        2: lambda: increase_skill("Deception"),
        3: lambda: increase_skill("Flyer"),
        4: lambda: increase_skill("Streetwise"),
        5: lambda: increase_skill("Gambler"),
        6: lambda: increase_skill("Jack of all Trades"),
    }

    NOBILITY_MUSTER_CASH = {
        1: 10000,
        2: 10000,
        3: 50000,
        4: 50000,
        5: 100000,
        6: 100000,
        7: 200000,
    }    

    def nobility_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Nobility")
        roll = roll_1d6()
        if roll == 1:
            log_and_print("Injured in a socially unacceptable fashion.")
            injury()

        elif roll == 2:
            log_and_print("A family scandal forces you out of your position.  Lose one Social Standing.")
            config.values["Social Standing"] -= 1
            get_mods()

        elif roll == 3:
            log_and_print("Disaster or war strikes.")
            choice = safe_int_input("Choose a skill to escape with:\n1. Stealth\n2. Deception\n", (1, 2))
            if choice == 1:
                result = skill_check("Stealth", "Dexterity")
            else:
                result = skill_check("Deception", best_mental())
            if result >= 8:
                log_and_print("You escape unharmed.")
            else:
                injury()

        elif roll == 4:
            log_and_print("Political manoeuverings usurp your position.  Gain a Rival.")
            choice = safe_int_input("Choose to advance:\n1. Diplomat\n2. Advocate\n", (1, 2))
            skill_list = ["Diplomat", "Advocate"]
            increase_skill(skill_list[choice - 1])

        elif roll == 5:
            log_and_print("An assassin tries to end your life.")
            roll = roll_2d6() + config.mods["Endurance"]
            if roll >= 8:
                log_and_print("You escape unharmed.")
            else:
                injury()
            
        else:
            log_and_print("Your fortunes change at court, forcing you to leave.  You gain a Contact and some street savvy.")
            increase_skill("Streetwise")
            config.contacts += 1

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Nobility")
            return
        if not config.keep_bonus:
            config.nobility_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        nobility_muster()
        check_retirement()  

    def nobility_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            nobility_mishap()
        elif roll == 3:
            log_and_print("You are challenged to a duel for your honour and standing.")
            choice = safe_choice("Do you accept? (y/n)\n", ("y", "n"))
            if choice == "n":
                log_and_print("Your cowardice becomes the talk of the town.")
                config.values["Social Standing"] -= 1
            else:
                result = skill_check("Melee", best_of_two("Strength", "Dexterity"))
                if result >= 8:
                    log_and_print("You defend your honor.")
                    increase_stat("Social Standing")
                else:
                    log_and_print("You are stabbed in a few technically unnecessary places and gain a reputation for poor swordsmanship.")
                    config.values["Social Standing"] -= 1
                    injury()
            choice = safe_int_input("Advance one of the following skills:\n1. Melee\n2. Leadership\n3. Tactics\n4. Deception\n")
            skill_list = ["Melee", "Leadership", "Tactics", "Deception"]
            increase_skill(skill_list[choice - 1])            

        elif roll == 4:
            log_and_print("Your time as a ruler or playboy gives you a wide range of experiences.")
            choice = safe_int_input(f"Gain a skill at Rank 1:\n1. Animals ({config.skills["Animals"]})\n2. Art ({config.skills["Art"]})\n"
                                    f"3. Carouse ({config.skills["Carouse"]})\n4. Streetwise ({config.skills["Streetwise"]}\n)", (1, 4))
            skill_list = ["Animals", "Art", "Carouse", "Streetwise"]
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 5:
            log_and_print("You inherit a gift from a rich relative.")
            config.benefit_bonus.append(1)

        elif roll == 6:
            log_and_print("You become a player in the intrigues of your local government.  You gain a Rival, but also knowledge.")
            choice = safe_int_input("Increase one of the following skills:\n1. Advocate\n2. Admin\n3. Diplomat\n4. Persuade\n", (1, 4))
            skill_list = ["Advocate", "Admin", "Diplomat", "Persuade"]
            increase_skill(skill_list[choice - 1])

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("A conspiracy of nobles attempts to recruit you.")
            choice = safe_choice("Do you join in their scheme? (y/n)", ("y", "n"))
            if choice == "n":
                log_and_print("You assert your loyalty and gain an Enemy.")
                config.enemies += 1
            else:
                choice = safe_int_input(f"Roll:\n1. Deception ({config.skills["Deception"]})\n2. Persuade ({config.skills["Persuade"]})\n")
                skill_list = ["Deception", "Persuade"]
                result = skill_check(skill_list[choice - 1], best_mental())
                if result >= 8:
                    log_and_print("You successfully advance the goals of the conspiracy.")
                    choice = safe_int_input("Advance one of the following skills:\n1. Deception\n2. Persuade\n3. Tactics\n4. Carouse\n", (1, 4))
                    skill_list = ["Deception", "Persuade", "Tactics", "Carouse"]
                    increase_skill(skill_list[choice - 1])
                else:
                    config.not_ejected = True
                    nobility_mishap()

        elif roll == 9:
            log_and_print("You gain a reputation as a fair and wise leader, or as a particularly efficient drain on your family.")
            log_and_print("You gain an Enemy from unhappy subjects or jealous relatives.")
            config.enemies += 1
            config.advance_bonus += 2

        elif roll == 10:
            log_and_print("You manipulate and charm your way through high society.  You gain a Rival, an Ally, and some skills.")
            config.rivals += 1
            config.allies += 1
            skill_list = ["Carouse", "Diplomat", "Persuade", "Steward"]
            choice = safe_int_input("Increase one of the following skills:\n"
            "1. Carouse\n2. Diplomat\n3. Persuade\n4. Steward\n", (1, 4))
            increase_skill(skill_list[choice - 1])
        
        elif roll == 11:
            log_and_print("You make an alliance with a powerful and charismatic noble.")
            config.allies += 1
            choice = safe_int_input("Choose either:\n1. Increase Leadership\n2. +4 DM to your next Advancement roll\n", (1, 2))
            if choice == 1:
                increase_skill("Leadership")
            else:
                config.advance_bonus += 4

        else:
            log_and_print("Your efforts are noted by the Imperium.  You are automatically promoted.")
            config.auto_advance = True

    def nobility_muster():
        muster_rolls = config.nobility_terms
        if config.nobility_rank == 1 or config.nobility_rank == 2:
            muster_rolls += 1
        if config.nobility_rank == 3 or config.nobility_rank == 4:
            muster_rolls += 2
        if config.nobility_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            if config.benefit_bonus:
                print(f"You will receive a +{config.benefit_bonus[-1]} bonus to the roll.")
            muster_rolls -= 1 
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(NOBILITY_MUSTER_CASH, config.nobility_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.nobility_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print("You made a few investments and gained a Ship Share.")
                    config.ship_shares += 1
                elif benefit == 2:
                    log_and_print("You made a few investments and gained two Ship Shares.")
                    config.ship_shares += 2
                elif benefit == 3:
                    weapon_benefit("Blade")
                elif benefit == 4:
                    increase_stat("Social Standing")
                elif benefit == 5:
                    tas_member()
                elif benefit == 6:
                    choice = safe_int_input("Choose:\n1. 5 Ship Shares towards a Luxury Yacht\n2. 2 more flexible Ship Shares\n", (1, 2))
                    if choice == 1:
                        config.ship_shares += 5
                        log_and_print("You gain five Ship Shares in a Luxury Yacht.")
                    else:
                        config.ship_shares += 2
                        log_and_print("You made a few investments and gained two Ship Shares")
                elif benefit == 7:
                    log_and_print("You move up in the world.")
                    increase_stat("Social Standing")
                    choice = safe_int_input("Choose:\n1. 5 Ship Shares towards a Luxury Yacht\n2. 2 more flexible Ship Shares\n", (1, 2))
                    if choice == 1:
                        config.ship_shares += 5
                        log_and_print("You gain five Ship Shares in a Luxury Yacht.")
                    else:
                        config.ship_shares += 2
                        log_and_print("You made a few investments and gained two Ship Shares")

    def nobility_develop():
        config.careers.append(f"Nobility: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            NOBILITY_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            NOBILITY_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            NOBILITY_ADVANCED_EDUCATION[roll]()

    config.qual = True
    if config.nobility_terms < 1 and config.values["Social Standing"] < 10:
        qualification("Nobility", "Social Standing", 10)

        if not config.qual:
            return
    
    config.terms += 1
    config.nobility_terms += 1
    if "Nobility" not in config.careers:
        print("As a Noble, you must choose one of the following paths:")
        print("1. Administrator, serving as a functionary or ruler of a small domain.")
        print("2. Diplomat, carrying missives and soothing tempers.")
        print("3. Dilettante, wandering about with a trust fund.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Nobility")
        if spec_choice == 1:
            config.spec_name = "Administrator"
            config.spec_table = NOBILITY_ADMINISTRATOR
            config.survival_tuple = ("Intelligence", 4) 
            config.advancement_tuple = ("Education", 6)  
            config.event_log.append(f"Term{config.terms}: Nobility: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in NOBILITY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Diplomat"
            config.spec_table = NOBILITY_DIPLOMAT
            config.survival_tuple = ("Intelligence", 5)
            config.advancement_tuple = ("Social Standing", 7)  
            config.event_log.append(f"Term{config.terms}: Nobility: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in NOBILITY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Dilettante"
            config.spec_table = NOBILITY_DILETTANTE
            config.survival_tuple = ("Social Standing", 3)
            config.advancement_tuple = ("Intelligence", 8)  
            config.event_log.append(f"Term{config.terms}: Nobility: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in NOBILITY_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    else:
        print("You bask in adulation for another four years.")
        config.careers.append(f"Term{config.terms}: Nobility: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Nobility: {config.spec_name}")
    
    nobility_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        nobility_mishap()

    if success:
        nobility_events()
        promotion = advance(*config.advancement_tuple, config.nobility_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            nobility_muster()
            config.prior_careers += 1
            available_careers.remove("Nobility")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a/an {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.nobility_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.nobility_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.nobility_rank} {config.spec_name}.")
            if config.spec_name == "Administrator":
                if config.nobility_rank == 1:
                    increase_skill("Admin", set_rank=1)
                elif config.nobility_rank == 3:
                    increase_skill("Advocate", set_rank=1)
                elif config.nobility_rank == 5:
                    increase_skill("Leadership", set_rank=1)
            elif config.spec_name == "Diplomat":
                if config.nobility_rank == 1:
                    increase_skill("Admin", set_rank=1)
                elif config.nobility_rank == 3:
                    increase_skill("Advocate", set_rank=1)
                elif config.nobility_rank == 5:
                    increase_skill("Diplomat", set_rank=1)
            elif config.spec_name == "Dilettante":
                if config.nobility_rank == 2:
                    increase_skill("Carouse", set_rank=1)
                elif config.nobility_rank == 4:
                    increase_skill("Persuade", set_rank=1)
                elif config.nobility_rank == 6:
                    increase_skill("Jack of all Trades", set_rank=1)

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 8:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                NOBILITY_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                NOBILITY_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                NOBILITY_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_nobility()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_nobility()
    else:
        config.prior_careers += 1
        nobility_muster()

    check_retirement()

def car_rogue():
    global available_careers

    def rogue_muster():
        muster_rolls = config.rogue_terms
        if config.rogue_rank == 1 or config.rogue_rank == 2:
            muster_rolls += 1
        if config.rogue_rank == 3 or config.rogue_rank == 4:
            muster_rolls += 2
        if config.rogue_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            if config.benefit_bonus:
                print(f"You will receive a +{config.benefit_bonus[-1]} bonus to the roll.")
            muster_rolls -= 1 
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(ROGUE_MUSTER_CASH, config.rogue_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.rogue_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print("You made a few investments and gained a Ship Share.")
                    config.ship_shares += 1
                elif benefit == 2:
                    weapon_benefit()
                elif benefit == 3:
                    log_and_print("You got a bit smarter.")
                    increase_stat("Intelligence")
                elif benefit == 4:
                    log_and_print("You made a few investments and gained two Ship Shares.")
                    config.ship_shares += 2
                elif benefit == 5:
                    armour_benefit()
                elif benefit == 6:
                    log_and_print("You honed your reflexes.")
                    increase_stat("Dexterity")
                elif benefit == 7:
                    choice = safe_int_input("Choose:\n1. Gain 5 Ship Shares towards a Corsair\n2. Take two general Ship Shares")
                    if choice == 1:
                        config.ship_shares += 5
                        log_and_print("You gain a large stake in a pirate ship.")
                    else:
                        config.ship_shares += 2
                        log_and_print("You make a few investments and get two Ship Shares.")

    def rogue_develop():
        config.careers.append(f"Rogue: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            ROGUE_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            ROGUE_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            ROGUE_ADVANCED_EDUCATION[roll]()

    config.qual = True
    if config.rogue_terms < 1:
        qualification("Rogue", "Dexterity", 6)

        if not config.qual:
            return
    
    config.terms += 1
    config.rogue_terms += 1
    if "Rogue" not in config.careers:
        print("As a Rogue, you must choose one of the following paths:")
        print("1. Thief, stealing from the whoever and giving to you.")
        print("2. Enforcer, breaking legs or whatever else needed breaking.")
        print("3. Pirate, plundering space ships and watching illicitly copied movies.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Rogue")
        if spec_choice == 1:
            config.spec_name = "Thief"
            config.spec_table = ROGUE_THIEF
            config.survival_tuple = ("Intelligence", 6) 
            config.advancement_tuple = ("Dexterity", 6)  
            config.event_log.append(f"Term{config.terms}: Rogue: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in ROGUE_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Enforcer"
            config.spec_table = ROGUE_ENFORCER
            config.survival_tuple = ("Endurance", 6)
            config.advancement_tuple = ("Strength", 6)  
            config.event_log.append(f"Term{config.terms}: Rogue: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in ROGUE_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Pirate"
            config.spec_table = ROGUE_PIRATE
            config.survival_tuple = ("Dexterity", 6)
            config.advancement_tuple = ("Intelligence", 6   )  
            config.event_log.append(f"Term{config.terms}: Rogue: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in ROGUE_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    else:
        print("You break the law for another four years.")
        config.careers.append(f"Term{config.terms}: Rogue: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Rogue: {config.spec_name}")
    
    rogue_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        rogue_mishap()
        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Rogue")
            return
        if not config.keep_bonus:
            config.rogue_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        rogue_muster()
        check_retirement()  

    if success:
        rogue_events()
        promotion = advance(*config.advancement_tuple, config.rogue_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            rogue_muster()
            config.prior_careers += 1
            available_careers.remove("Rogue")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a/an {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.rogue_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.rogue_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.rogue_rank} {config.spec_name}.")
            if config.spec_name == "Thief":
                if config.rogue_rank == 1:
                    increase_skill("Stealth", set_rank=1)
                elif config.rogue_rank == 3:
                    increase_skill("Streetwise", set_rank=1)
                elif config.rogue_rank == 5:
                    increase_skill("Recon", set_rank=1)
            elif config.spec_name == "Enforcer":
                if config.rogue_rank == 1:
                    increase_skill("Persuade", set_rank=1)
                elif config.rogue_rank == 3:
                    choice = safe_int_input(f"Gain a skill at Rank 1:\n1. Melee: Current ({config.skills["Melee"]})\n"
                                            f"2. Gun Combat: Current ({config.skills["Gun Combat"]})", (1,2))
                    skill_list = ["Melee", "Gun Combat"]
                    increase_skill(skill_list[choice - 1], set_rank=1)
                elif config.rogue_rank == 5:
                    increase_skill("Streetwise", set_rank=1)
            elif config.spec_name == "Pirate":
                if config.rogue_rank == 1:
                    choice = safe_int_input(f"Gain a skill at Rank 1:\n1. Pilot: Current ({config.skills["Pilot"]})\n"
                                            f"2. Gunner: Current ({config.skills["Gunner"]})", (1,2))
                    skill_list = ["Pilot", "Gunner"]
                    increase_skill(skill_list[choice - 1], set_rank=1)
                elif config.rogue_rank == 3:
                    choice = safe_int_input(f"Gain a skill at Rank 1:\n1. Melee: Current ({config.skills["Melee"]})\n"
                                            f"2. Gun Combat: Current ({config.skills["Gun Combat"]})", (1,2))
                    skill_list = ["Melee", "Gun Combat"]
                    increase_skill(skill_list[choice - 1], set_rank=1)
                elif config.rogue_rank == 5:
                    choice = safe_int_input(f"Gain a skill at Rank 1:\n1. Engineer: Current ({config.skills["Engineer"]})\n"
                                            f"2. Navigation: Current ({config.skills["Navigation"]})", (1,2))
                    skill_list = ["Engineer", "Navigation"]
                    increase_skill(skill_list[choice - 1], set_rank=1)

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 10:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                ROGUE_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                ROGUE_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                ROGUE_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.forced_drafted:
        join_draft()
    
    else:

        if config.must_continue:
            config.must_continue = False
            log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
            car_rogue()
        remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
        if remain == "y":
            car_rogue()
        else:
            config.prior_careers += 1
            rogue_muster()

        check_retirement()

def car_scholar():
    global available_careers
    SCHOLAR_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Intelligence"),
        2: lambda: increase_stat("Education"),
        3: lambda: increase_stat("Social Standing"),
        4: lambda: increase_stat("Dexterity"),
        5: lambda: increase_stat("Endurance"),
        6: lambda: increase_skill("Computers")
    }

    SCHOLAR_SERVICE_SKILLS = {
        1: lambda: increase_skill("Comms"),
        2: lambda: increase_skill("Computers"),
        3: lambda: increase_skill("Diplomat"),
        4: lambda: increase_skill("Medic"),
        5: lambda: increase_skill("Investigate"),
        6: lambda: choose_science_skill(),
    }

    SCHOLAR_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Art"),
        2: lambda: increase_skill("Advocate"),
        3: lambda: increase_skill("Computers"),
        4: lambda: increase_skill("Language"),
        5: lambda: increase_skill("Engineer"),
        6: lambda: choose_science_skill(),
    }   
    
    SCHOLAR_FIELD_RESEARCHER = {
        1: lambda: increase_skill("Sensors"),
        2: lambda: increase_skill("Diplomat"),
        3: lambda: increase_skill("Language"),
        4: lambda: increase_skill("Survival"),
        5: lambda: increase_skill("Investigate"),
        6: lambda: choose_science_skill(),
    }

    SCHOLAR_SCIENTIST = {
        1: lambda: increase_skill("Admin"),
        2: lambda: increase_skill("Engineer"),
        3: lambda: choose_science_skill(),
        4: lambda: increase_skill("Sensors"),
        5: lambda: increase_skill("Computers"),
        6: lambda: choose_science_skill(),
    }

    SCHOLAR_PHYSICIAN = {
        1: lambda: increase_skill("Medic"),
        2: lambda: increase_skill("Comms"),
        3: lambda: increase_skill("Investigate"),
        4: lambda: increase_skill("Medic"),
        5: lambda: increase_skill("Persuade"),
        6: lambda: choose_science_skill(),
    }

    SCHOLAR_MUSTER_CASH = {
        1: 5000,
        2: 10000,
        3: 20000,
        4: 30000,
        5: 40000,
        6: 60000,
        7: 100000,
    }    

    def scholar_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Scholar")
        roll = roll_1d6()
        if roll == 1:
            log_and_print("You learned a painful lesson in biology through injury.")
            injury()

        elif roll == 2:
            log_and_print("A disaster leaves several injured, and others blame you, forcing you to leave your career.")
            log_and_print("You gain a rival.")
            injury_roll_twice(high=True)
            config.rivals += 1

        elif roll == 3:
            log_and_print("The planetary government interferes with your research for political or religious reasons.")
            config.not_ejected = True
            choice = safe_int_input("Choose:\n1. Continue working openly and earn an enemy in the government.\n" \
            "2. Drop out of the public view and lose Social Standing.\n")
            if choice == 1:
                log_and_print("You defy the authorities.  They don't much like that.")
                choose_science_skill()
                config.enemies += 1
            else:
                log_and_print("You hide your research at the cost of standing in the scientific community.")
                choose_science_skill()
                config.values["Social Standing"] -= 2

        elif roll == 4:
            log_and_print("An expedition or voyage goes wrong, leaving you stranded in the wilderness.  Your job doesn't wait for you.")
            skill_list = ["Survival", "Athletics"]
            choice = safe_int_input("Choose to gain at Rank 1:\n1. Survival 1\n2. Athletics\n")
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 5:
            log_and_print("Your work is sabotaged by unknown parties.")
            choice = safe_int_input("Choose:\n1. Salvage what you can and leave the career with full benefits.\n" \
            "2. Start again from scratch, losing your benefits but keeping your job.\n")
            if choice == 1:
                config.keep_bonus = True
                log_and_print("You gather your belongings and head to new pursuits.")
            else:
                config.not_ejected = True
                log_and_print("You start over from scratch.")
                config.scholar_terms = 0
                if config.scholar_rank in (1, 2):
                    config.scholar_terms -= 1
                elif config.scholar_rank in (3, 4):
                    config.scholar_terms -= 2
                elif config.scholar_rank in (5, 6):
                    config.scholar_terms -= 3
            
        else:
            log_and_print("A rival researcher blackens your name or steals your research.  Gain a rival but keep your job.")
            config.rivals += 1
            config.not_ejected = True

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Scholar")
            return
        if not config.keep_bonus:
            config.scholar_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        scholar_muster()
        check_retirement()  

    def scholar_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            scholar_mishap()
        elif roll == 3:
            log_and_print("You are called upon to do research that goes against your conscience.")
            choice = safe_choice("Do you accept the offer? (y/n)\n", ("y", "n"))
            if choice == "y":
                log_and_print("You find your morals flexible and your knife sharp.")
                roll = roll_1d3()
                print(f"Your enemies list increases by {roll}.")
                config.enemies += roll
                print("But, you do learn a few things.")
                skill_list = ["Physical Sciences", "Life Sciences", "Social Sciences", "Space Sciences"]
                for num in range(1, len(skill_list) + 1):
                    print(f"{num}. {skill_list[num - 1]}")
                choice = safe_int_input("Which skill will you advance?\n", (1, 4))
                increase_skill(skill_list(choice - 1))
                skill_list.remove(skill_list[choice - 1])
                for num in range(1, len(skill_list) + 1):
                    print(f"{num}. {skill_list[num - 1]}")
                    choice = safe_int_input("Choose a second skill to advance:\n", (1, 3))
                    increase_skill(skill_list[choice - 1])
            else:
                log_and_print("You take the unprofitable path of virtue.")
            
        elif roll == 4:
            log_and_print("You are assigned to work on a secret project for a patron or organization.")
            skill_list = ["Medic", "Any Science", "Engineer", "Computers", "Investigate"]
            print("Choose a skill to gain at Rank 1")
            for num in range(1, len(skill_list) + 1):
                print(f"{num}. {skill_list[num - 1]}")
            choice = safe_int_input("Which skill?\n", (1, 5))
            if choice == 2:
                choose_science_skill(set_rank=1)
            else:
                increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 5:
            log_and_print("You win a prestigious prize for your work, garnering both the praise and envy of your peers.")
            config.benefit_bonus.append(1)

        elif roll == 6:
            log_and_print("You are given advanced training in a specialized field.")
            roll = roll_2d6() + config.mods["Education"]
            if roll < 8:
                log_and_print("You fall asleep in class, but learn a new card game afterwards.")
            else:
                increase_any_skill(set_rank=1)

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("You have the opportunity to cheat in some fashion, advancing your career and research\n"
            "by stealing another's work.")
            choice = safe_int_input("Will you choose to:\n1. Be honest.\n" \
            "2. Be a greedy research thief.", (1, 2))
            if choice == 2:
                config.enemies += 1
                result = better_skill("Deception", best_mental(), "Admin", best_mental())
                if result >= 8:
                    log_and_print("You've earned an enemy, but a number of benefits.")
                    increase_any_skill()
                    config.benefit_bonus.append(2)
                else:
                    log_and_print("You fail spectacularly, earning an enemy and losing research funding.")
                    config.scholar_terms -= 1

        elif roll == 9:
            log_and_print("You make a breakthrough in your career and get some additional support from the administration.")
            config.advance_bonus += 2

        elif roll == 10:
            log_and_print("You become entangled in a bureaucratic or legal morass that distracts you from your work.")
            skill_list = ["Admin", "Advocate", "Persuade", "Diplomat"]
            choice = safe_int_input("Gain one of the following skills at Rank 1:\n"
            "1. Admin\n2. Advocate\n3. Persuade\n4. Diplomat\n", (1, 4))
            increase_skill(skill_list[choice - 1], set_rank=1)
        
        elif roll == 11:
            log_and_print("You work for an eccentric, but brilliant, mentor who becomes an Ally.")
            choice = safe_int_input("Choose:\n1. Increase any Science skill\n2. Get +4 to your next Advancement roll\n", (1, 2))
            if choice == 1:
                choose_science_skill()
            else:
                config.advance_bonus += 4
            
        else:
            log_and_print("Your work leads to a considerable breakthrough.  You are automatically promoted.")
            config.auto_advance = True

    def scholar_muster():
        muster_rolls = config.scholar_terms
        if config.scholar_rank in (1, 2):
            muster_rolls += 1
        if config.scholar_rank in (3, 4):
            muster_rolls += 2
        if config.scholar_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(SCHOLAR_MUSTER_CASH, config.scholar_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.scholar_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print("You got a bit sharper between the ears.")
                    increase_stat("Intelligence")
                elif benefit == 2:
                    log_and_print("You got some post-graduate education.")
                    increase_stat("Education")
                elif benefit == 3:
                    log_and_print("You made a few investments and gained two Ship Shares.")
                    config.ship_shares += 2
                elif benefit == 4:
                    log_and_print("You moved up in society.")
                    increase_stat("Social Standing")
                elif benefit == 5:
                    log_and_print("You were given some scientific equipment.")
                    config.starting_items.append("Scientific Equipment")
                elif benefit == 6:
                    log_and_print("You were offered a stake in a Lab Ship, or two more flexible Ship Shares.")
                    choice = safe_int_input("Will you take:\n1. 5 Lab Ship Shares\n2. 2 general Ship Shares", (1, 2))
                    if choice == 1:
                        log_and_print("You accept the 5% stake in a Lab Ship")
                        config.ship_shares += 5
                    else:
                        log_and_print("You invest in two general Ship Shares.")
                        config.ship_shares += 2
                elif benefit == 7:
                    log_and_print("You were offered a stake in a Lab Ship, or two more flexible Ship Shares.")
                    choice = safe_int_input("Will you take:\n1. 5 Lab Ship Shares\n2. 2 general Ship Shares", (1, 2))
                    if choice == 1:
                        log_and_print("You accept the 5% stake in a Lab Ship")
                        config.ship_shares += 5
                    else:
                        log_and_print("You invest in two general Ship Shares.")
                        config.ship_shares += 2

    def scholar_develop():
        config.careers.append(f"Scholar: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 10:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            SCHOLAR_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            SCHOLAR_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            SCHOLAR_ADVANCED_EDUCATION[roll]()

    if config.scholar_terms < 1:
        qualification("Scholar", "Intelligence", 6)

        if not config.qual:
            return
    
    config.terms += 1
    config.scholar_terms += 1
    if "Scholar" not in config.careers:
        print("As a Scholar, you must choose one of the following paths:")
        print("1. Field Researcher: Doing hands on research in laboratories and the wilderness.")
        print("2. Scientist: You didn't like leaving your lab.")
        print("3. Physician: Healing everyone, including thyself.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Scholar")
        if spec_choice == 1:
            config.spec_name = "Field Researcher"
            config.spec_table = SCHOLAR_FIELD_RESEARCHER
            config.survival_tuple = ("Endurance", 6) 
            config.advancement_tuple = ("Intelligence", 6)  
            config.event_log.append(f"Term{config.terms}: Scholar: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in SCHOLAR_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Scientist"
            config.spec_table = SCHOLAR_SCIENTIST
            config.survival_tuple = ("Education", 4)
            config.advancement_tuple = ("Intelligence", 8)  
            config.event_log.append(f"Term{config.terms}: Scholar: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in SCHOLAR_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Physician"
            config.spec_table = SCHOLAR_PHYSICIAN
            config.survival_tuple = ("Education", 4)
            config.advancement_tuple = ("Education", 8)  
            config.event_log.append(f"Term{config.terms}: Scholar: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in SCHOLAR_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    else:
        print("You spend four more years with a microscope.")
        config.careers.append(f"Term{config.terms}: Scholar: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Scholar: {config.spec_name}")
    
    scholar_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        scholar_mishap()

    if success:
        scholar_events()
        promotion = advance(*config.advancement_tuple, config.scholar_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            scholar_muster()
            config.prior_careers += 1
            available_careers.remove("Scholar")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a/an {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.scholar_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.scholar_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.scholar_rank} {config.spec_name}.")
            if config.spec_name == "Field Researcher":
                if config.scholar_rank == 1:
                    increase_skill("Social Sciences", set_rank=1)
                elif config.scholar_rank == 3:
                    increase_skill("Investigate", set_rank=1)
                elif config.scholar_rank == 5:
                    increase_skill("Computers")
            elif config.spec_name == "Scientist":
                if config.scholar_rank == 1:
                    increase_skill("Physical Sciences", set_rank=1)
                elif config.scholar_rank == 3:
                    increase_skill("Investigate", set_rank=1)
                elif config.scholar_rank == 5:
                    increase_skill("Computers")
            elif config.spec_name == "Physician":
                if config.scholar_rank == 1:
                    increase_skill("Medic", set_rank=1)
                elif config.scholar_rank == 3:
                    increase_skill("Life Sciences", set_rank=1)
                elif config.scholar_rank == 5:
                    increase_skill("Social Sciences", set_rank=1)

            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 10:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                SCHOLAR_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                SCHOLAR_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                SCHOLAR_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_scholar()
    remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
    if remain == "y":
        car_scholar()
    else:
        config.prior_careers += 1
        scholar_muster()

    check_retirement()

def car_scout():
    global available_careers
    SCOUT_PERSONAL_DEVELOPMENT = {
        1: lambda: increase_stat("Strength"),
        2: lambda: increase_stat("Dexterity"),
        3: lambda: increase_stat("Endurance"),
        4: lambda: increase_stat("Intelligence"),
        5: lambda: increase_stat("Education"),
        6: lambda: increase_skill("Jack of all Trades"),
    }

    SCOUT_SERVICE_SKILLS = {
        1: lambda: increase_skill("Pilot"),
        2: lambda: increase_skill("Survival"),
        3: lambda: increase_skill("Mechanic"),
        4: lambda: increase_skill("Astrogation"),
        5: lambda: increase_skill("Comms"),
        6: lambda: increase_skill("Gun Combat"),
    }

    SCOUT_ADVANCED_EDUCATION = {
        1: lambda: increase_skill("Medic"),
        2: lambda: increase_skill("Navigation"),
        3: lambda: increase_skill("Engineer"),
        4: lambda: increase_skill("Computers"),
        5: lambda: increase_skill("Space Science"),
        6: lambda: increase_skill("Jack of all Trades"),
    }   
    
    SCOUT_COURIER = {
        1: lambda: increase_skill("Comms"),
        2: lambda: increase_skill("Sensors"),
        3: lambda: increase_skill("Pilot"),
        4: lambda: increase_skill("Vacc Suit"),
        5: lambda: increase_skill("Zero-G"),
        6: lambda: increase_skill("Astrogation"),
    }

    SCOUT_SURVEY = {
        1: lambda: increase_skill("Sensors"),
        2: lambda: increase_skill("Persuade"),
        3: lambda: increase_skill("Pilot"),
        4: lambda: increase_skill("Navigation"),
        5: lambda: increase_skill("Diplomat"),
        6: lambda: increase_skill("Streetwise"),
    }

    SCOUT_EXPLORATION = {
        1: lambda: increase_skill("Sensors"),
        2: lambda: increase_skill("Pilot"),
        3: lambda: increase_skill("Pilot"),
        4: lambda: increase_skill("Life Sciences"),
        5: lambda: increase_skill("Stealth"),
        6: lambda: increase_skill("Recon"),
    }

    SCOUT_MUSTER_CASH = {
        1: 20000,
        2: 20000,
        3: 30000,
        4: 30000,
        5: 50000,
        6: 50000,
        7: 50000,
    }    

    def scout_mishap():
        print("You have suffered a severe mishap.")
        available_careers.remove("Scout")
        roll = roll_1d6()
        if roll == 1:
            log_and_print("Severly injured in action.")
            choice = safe_int_input("Choose:\n1. Take a result of '2' on the Injury table\n2. Roll twice and accept the lower result\n", (1, 2))
            if choice == 1:
                injury(2)
            else:
                injury_roll_twice()

        elif roll == 2:
            log_and_print("Psychologically damaged by your time in the scouts.")
            choice = safe_int_input("Choose to reduce:\n1. Intelligence\n2. Social Standing\n", (1, 2))
            if choice == 1:
                config.values["Intelligence"] -= 1
            else:
                config.values["Social Standing"] -= 1
            get_mods()

        elif roll == 3:
            log_and_print("Your ship is damaged and you have to hitch-hike your way back to the nearest scout base.")
            contact_roll = roll_1d6()
            enemies_roll = roll_1d3()
            config.contacts += contact_roll
            config.enemies += enemies_roll
            print(f"Along the way, you gain {contact_roll} Contacts and {enemies_roll} Enemies.")

        elif roll == 4:
            log_and_print("You inadvertently cause a conflict between the Imperium and a minor world or race.")
            config.rivals += 1
            increase_skill("Diplomat", set_rank=1)

        elif roll == 5:
            log_and_print("You have no idea what happened to you -- they found your ship drifting on the fringes of friendly space.")
            
            
        else:
            log_and_print("You boldly go... to the Emergency Room with serious injuries.")
            injury()

        if config.not_ejected:
            config.not_ejected = False
            available_careers.append("Scout")
            return
        if not config.keep_bonus:
            config.scout_terms -= 1
        config.keep_bonus = False
        config.prior_careers += 1
        config.age += 4
        check_aging()
        update_char()
        scout_muster()
        check_retirement()  

    def scout_events():
        roll = roll_2d6()
        if roll == 2:
            config.not_ejected = True     
            log_and_print("Disaster!  You have a mishap, but your career will survive.")
            scout_mishap()
        elif roll == 3:
            log_and_print("Your ship is ambushed by enemy vessels.")
            config.enemies += 1
            choice = safe_int_input("Choose:\n1. A piloting check to escape\n2. A difficult attempt to persuade the attackers", (1, 2))
            if choice == "1":
                roll = skill_check("Pilot", "Dexterity")
                if roll >= 8:
                    log_and_print("You successfully escaped, but gained an Enemy.")
                    increase_skill("Sensors", set_rank=1)  
                else:
                    config.must_leave = True
                    log_and_print("Your ship is destroyed and you are rejected for future terms in the Scouts.")
            else:
                roll = skill_check("Persuade", best_mental())
                if roll >= 10:
                    log_and_print("You make some promises you can't keep, but they don't realize it until you're gone.")
                    increase_skill("Sensors", set_rank=1) 
                else:
                    config.must_leave = True
                    log_and_print("Your ship is destroyed and you are rejected for future terms in the Scouts.")
            
        elif roll == 4:
            log_and_print("You survey an alien world.")
            skill_list = ["Animals", "Survival", "Recon", "Life Sciences"]
            print("Choose a skill to gain at Rank 1")
            for num in range(1, len(skill_list) + 1):
                print(f"{num}. {skill_list[num - 1]}: Currently {config.skills[skill_list[num - 1]]}")
            choice = safe_int_input("Which skill?\n", (1, 4))
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 5:
            log_and_print("You perform an exemplary service for the Scouts.")
            config.benefit_bonus.append(1)

        elif roll == 6:
            log_and_print("You spend several years jumping from world to world in your scout ship.")
            skill_list = ["Animals", "Survival", "Recon", "Life Sciences"]
            print("Choose a skill to gain at Rank 1")
            for num in range(1, len(skill_list) + 1):
                print(f"{num}. {skill_list[num - 1]}: Currently {config.skills[skill_list[num - 1]]}")
            choice = safe_int_input("Which skill?\n", (1, 4))
            increase_skill(skill_list[choice - 1], set_rank=1)

        elif roll == 7:
            life_events()

        elif roll == 8:
            log_and_print("When dealing with an alien race, you have an opportunity to gather extra intelligence about them.")
            result = better_skill("Sensors", best_mental(), "Deception", best_mental())
            if result >= 8:
                log_and_print("You get the intel, gain a loyal Ally in the Imperium, and get a bonus to advancement.")
                config.allies += 1
                config.advance_bonus += 2
            else:
                log_and_print("You fail spectacularly.")
                config.not_ejected = True
                scout_mishap()

        elif roll == 9:
            log_and_print("Your scout ship is one of the first on the scene to rescue disaster survivors.")
            result = better_skill("Medic", best_mental(), "Engineer", best_mental())
            if result >= 8:
                log_and_print("You are an excellent first responder, gaining a useful Contact and a commendation.")
                config.advance_bonus += 2
                config.contacts += 1
            else:
                log_and_print("One of the few survivors blames your incompetence for high body count.  Gain an Enemy.")
                config.enemies += 1

        elif roll == 10:
            log_and_print("You spend a great deal of time on the fringes of known space.")
            result = better_skill("Survival", best_mental(), "Pilot", "Dexterity")
            if result >= 8:
                log_and_print("You gain an alien Contact and learn a few things.")
                increase_any_skill()
                config.contacts += 1
            else:
                log_and_print("Bad things happen out there.")
                config.not_ejected = True
                scout_mishap()
        
        elif roll == 11:
            log_and_print("You deliver an important message for the Imperium.")
            choice = safe_int_input("Choose:\n1. Gain a level of Diplomat\n2. Get +4 to your next Advancement roll\n", (1, 2))
            if choice == 1:
                increase_skill("Diplomat")
            else:
                config.advance_bonus += 4

        else:
            log_and_print("You discover something of great value to the Imperium.  You are automatically promoted.")
            config.auto_advance = True

    def scout_muster():
        muster_rolls = config.scout_terms
        if config.scout_rank in (1, 2):
            muster_rolls += 1
        if config.scout_rank in (3, 4):
            muster_rolls += 2
        if config.scout_rank >= 5:
            muster_rolls += 3
        while muster_rolls:
            print(f"You have {muster_rolls} benefit rolls remaining.")
            muster_rolls -= 1
            cashben = safe_int_input("Will you choose:\n1. Cash\n2. Benefits?\n", valid_range=(1, 2))
            if cashben == 1:
                cash_roll(SCOUT_MUSTER_CASH, config.scout_rank)

            if cashben == 2:
                benefit = roll_1d6()
                if config.scout_rank >= 5:
                    benefit += 1
                if config.benefit_bonus:
                    benefit += config.benefit_bonus[-1]
                    config.benefit_bonus.pop()
                if benefit > 7:
                    benefit = 7
                
                if benefit == 1:
                    log_and_print("You make a few investments and get a Ship Share.")
                    config.ship_shares += 1
                elif benefit == 2:
                    log_and_print("You got a bit sharper between the ears.")
                    increase_stat("Intelligence")
                elif benefit == 3:
                    log_and_print("You got some education.")
                    increase_stat("Education")
                elif benefit == 4:
                    weapon_benefit()
                elif benefit == 5:
                    weapon_benefit()
                else:
                    if "Scout Ship" not in config.starting_items():
                        log_and_print("You receive a Scout Ship on loan from Scouts.")
                        config.starting_items.append("Scout Ship")
                    else:
                        shares = roll_1d6()
                        log_and_print("You gain some Ship Shares.")
                        config.ship_shares += shares

    def scout_develop():
        config.careers.append(f"Scout: {config.spec_name}")
        print("Choose a table to advance your skills:\n")
        print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
        if config.values["Education"] >= 8:
            print("4. Advanced Education\n")
        choice = safe_int_input("Your choice?\n", (1, 4))
        roll = roll_1d6()
        if choice == 1:
            SCOUT_PERSONAL_DEVELOPMENT[roll]()

        elif choice == 2:
            SCOUT_SERVICE_SKILLS[roll]()

        elif choice == 3:
            config.spec_table[roll]()

        else:
            SCOUT_ADVANCED_EDUCATION[roll]()

    if not config.drafted and config.scout_terms < 1:
        qualification("Scout", "Intelligence", 5)

        if not config.qual:
            return
    config.drafted = False
    config.terms += 1
    config.scout_terms += 1
    if "Scout" not in config.careers:
        print("As a Scout, you must choose one of the following paths:")
        print("1. Courier: Serving lonely duty on the X-boat network, carrying messages for the Imperium.")
        print("2. Survey: You visited border worlds and assessed their worth.")
        print("3. Explorer: Boldly going where no man has come back from.")
        spec_choice = safe_int_input("Choose: 1/2/3?\n", (1, 3))
        config.careers.append("Scout")
        if spec_choice == 1:
            config.spec_name = "Courier"
            config.spec_table = SCOUT_COURIER
            config.survival_tuple = ("Endurance", 5) 
            config.advancement_tuple = ("Education", 9)  
            config.event_log.append(f"Term{config.terms}: Scout: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in SCOUT_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

        if spec_choice == 2:
            config.spec_name = "Survey"
            config.spec_table = SCOUT_SURVEY
            config.survival_tuple = ("Endurance", 6)
            config.advancement_tuple = ("Intelligence", 8)  
            config.event_log.append(f"Term{config.terms}: Scout: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in SCOUT_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False    
    
        if spec_choice == 3:
            config.spec_name = "Exploration"
            config.spec_table = SCOUT_EXPLORATION
            config.survival_tuple = ("Endurance", 7)
            config.advancement_tuple = ("Education", 7)  
            config.event_log.append(f"Term{config.terms}: Scout: {config.spec_name}")
            if config.prior_careers < 1:
                for effect in SCOUT_SERVICE_SKILLS.values():
                    effect()
                config.basic_training = False

    else:
        print("You sign up for four more years among the stars.")
        config.careers.append(f"Term{config.terms}: Scout: {config.spec_name}.")
        config.event_log.append(f"Term{config.terms}: Scout: {config.spec_name}")
    
    scout_develop()

    success = survival(*config.survival_tuple)
    
    if not success:
        scout_mishap()

    if success:
        scout_events()
        promotion = advance(*config.advancement_tuple, config.scout_terms)

        if promotion == 3:
            log_and_print("You get bored and frustrated with your inability to advance.")
            scout_muster()
            config.prior_careers += 1
            available_careers.remove("Scout")
            config.age += 4
            check_aging()
            print(f"\n\nAfter four years as a/an {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
            update_char()
            check_retirement()
            
        
        elif promotion == 1:
            config.scout_rank += 1
            print(f"\033[34m{config.char_name} advanced to Rank {config.scout_rank} {config.spec_name}.\033[0m")
            config.event_log.append(f"{config.char_name} advanced to Rank {config.scout_rank} {config.spec_name}.")
            
            if config.scout_rank == 1:
                increase_skill("Vacc Suit", set_rank=1)
            elif config.scout_rank == 3:
                increase_skill("Pilot", set_rank=1)
                
            print("Choose a table to advance your skills:\n")
            if values["Education"] >= 8:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}\n4. Advanced Education\n")
                choice = safe_int_input("1, 2, 3, or 4?\n", (1, 4))

            else:
                print(f"1. Personal Development\n2. Service Skills\n3. Specialist: {config.spec_name}")
                choice = safe_int_input("1, 2, or 3?\n", (1, 3))
            roll = roll_1d6()
            if choice == 1:
                SCOUT_PERSONAL_DEVELOPMENT[roll]()

            elif choice == 2:
                SCOUT_SERVICE_SKILLS[roll]()

            elif choice == 3:
                config.spec_table[roll]()

            elif choice == 4:
                SCOUT_ADVANCED_EDUCATION[roll]()

    config.age += 4
    check_aging()
    print(f"\n\nAfter four years as a {config.spec_name}, you are {config.age} years old and your stats are as follows:\n")
    update_char()

    if config.must_continue:
        config.must_continue = False
        log_and_print(f"You were so good at being a {config.spec_name} that you aren't allowed to stop.  You automatically continue.")
        car_scout()
    if config.must_leave:
        config.prior_careers += 1
        scout_muster()
    else:
        remain = safe_choice(f"Do you wish to continue the life of a {config.spec_name}? y/n?\n", ["y", "n"])
        if remain == "y":
            car_scout()
        else:
            config.prior_careers += 1
            scout_muster()

    check_retirement()
