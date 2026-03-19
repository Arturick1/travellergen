import config
from config import *


def generate_planet():
    
    SIZES_GRAVITY = {
        0: ("800 km", "Negligible"),
        1: ("1,600 km", "0.05"),
        2: ("3,200 km", "0.15"),
        3: ("4,800 km", "0.25"),
        4: ("6,400 km", "0.35"),
        5: ("8,000 km", "0.45"),
        6: ("9,600 km", "0.7"),
        7: ("11,200 km", "0.9"),
        8: ("12,800 km", "1.0"),
        9: ("14,400 km", "1.25"),
        10: ("16,000 km", "1.4"),
    }

    ATMOSPHERE = {
        0: "None",
        1: "Trace",
        2: "Very Thin, Tainted",
        3: "Very Thin",
        4: "Thin, Tainted",
        5: "Thin",
        6: "Standard",
        7: "Standard, Tainted",
        8: "Dense",
        9: "Dense, Tainted",
        10: "Exotic",
        11: "Corrosive",
        12: "Insidious",
        13: "Dense, High",
        14: "Thin, Low",
        15: "Unusual",
    }

    HYDROGRAPHICS = {
        0: "0%-5%",
        1: "6%-15%",
        2: "16%-25%",
        3: "26%-35%",
        4: "36%-45%",
        5: "46%-55%",
        6: "56%-65%",
        7: "66%-75%",
        8: "76%-85%",
        9: "86%-95%",
        10: "96%-100%",
    }

    POPULATION = {
        0: "None",
        1: "Few",
        2: "Hundreds",
        3: "Thousands",
        4: "Tens of thousands",
        5: "Hundreds of thousands",
        6: "Millions",
        7: "Tens of millions",
        8: "Hundreds of millions",
        9: "Billions",
        10: "Tens of billions",
        11: "Hundreds of billions",
        12: "Trillions",
    }

    GOVERNMENT = {
        0: "None",
        1: "Company/Corporation",
        2: "Participating democracy",
        3: "Self-perpetuating oligarchy",
        4: "Representative democracy",
        5: "Feudal technocracy",
        6: "Captive government",
        7: "Balkanisation",
        8: "Civil service bureaucracy",
        9: "Impersonal bureaucracy",
        10: "Charismatic dictator",
        11: "Non-charismatic leader",
        12: "Charismatic oligarchy",
        13: "Religious dictatorship",
    }

    CULTURAL_QUIRKS = {
        11: "Sexist",
        12: "Religious",
        13: "Artistic",
        14: "Ritualised",
        15: "Conservative",
        16: "Xenophobic",
        21: "Taboo",
        22: "Deceptive",
        23: "Liberal",
        24: "Honourable",
        25: "Influenced",
        26: "Fusion",
        31: "Barbaric",
        32: "Remnant",
        33: "Degenerate",
        34: "Progressive",
        35: "Recovering",
        36: "Nexus",
        41: "Tourist Attraction",
        42: "Violent",
        43: "Peaceful",
        44: "Obsessed",
        45: "Fashion",
        46: "At war",
        51: "Unusual Custom: Offworlders",
        52: "Unusual Custom: Starport",
        53: "Unusual Custom: Media",
        54: "Unusual Customs: Technology",
        55: "Unusual Customs: Lifecycle",
        56: "Unusual Customs: Social Standings",
        61: "Unusual Customs: Trade",
        62: "Unusual Customs: Nobility",
        63: "Unusual Customs: Sex",
        64: "Unusual Customs: Eating",
        65: "Unusual Customs: Travel",
        66: "Unusual Customs: Conspiracy",
    }
    print(SIZES_GRAVITY[roll_2d6() - 2][0])
    print(CULTURAL_QUIRKS[roll_dd()])

generate_planet()