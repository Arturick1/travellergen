from config import roll_2d6, roll_1d6

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

def increase_skill(skill):
    if skills[skill] == None:
        skills[skill] = 0

    else:
        skills[skill] += 1

    return skills

def skill_check(skill, mod, mods):
    skill_bonus = 0
    skill_result = 0
    rolled = roll_2d6()
    stat_bonus = mods[mod]
    if skills[skill] == None:
        skill_bonus -= 3
        print(f"Adding {skill} skill bonus of {skill_bonus}, {mod} bonus of {stat_bonus}, and dice roll of {rolled}")
        skill_result += skill_bonus + stat_bonus + rolled
        return skill_result
    skill_bonus += skills[skill]
    print(f"Adding {skill} skill bonus of {skill_bonus}, {mod} bonus of {stat_bonus}, and dice roll of {rolled}")
    skill_result += skill_bonus + stat_bonus + rolled
    return skill_result    