# I used this code to convert the files in /json into NeoFoodClub-compatible json files, located in /fixed

# NOTES:
#  - Must use Python3.8+
#  - 618 files were invalid, 1515 files were valid.
#  - you'll probably need to change the Paths below.

import json
import os
from pathlib import Path
from typing import List

folder = Path("/Users/steve/Downloads/foodclubdata-master/json")
fixedfolder = Path("/Users/steve/Downloads/foodclubdata-master/fixed")

FOODS = {
    "Hotfish": 1,
    "Broccoli": 2,
    "Wriggling Grub": 3,
    "Joint Of Ham": 4,
    "Rainbow Negg": 5,
    "Streaky Bacon": 6,
    "Ultimate Burger": 7,
    "Bacon Muffin": 8,
    "Hot Cakes": 9,
    "Spicy Wings": 10,
    "Apple Onion Rings": 11,
    "Sushi": 12,
    "Negg Stew": 13,
    "Ice Chocolate Cake": 14,
    "Strochal": 15,
    "Mallowicious Bar": 16,
    "Fungi Pizza": 17,
    "Broccoli and Cheese Pizza": 18,
    "Bubbling Blueberry Pizza": 19,
    "Grapity Slush": 20,
    "Rainborific Slush": 21,
    "Tangy Tropic Slush": 22,
    "Blueberry Tomato Blend": 23,
    "Lemon Blitz": 24,
    "Fresh Seaweed Pie": 25,
    "Flaming Burnumup": 26,
    "Hot Tyrannian Pepper": 27,
    "Eye Candy": 28,
    "Cheese and Tomato Sub": 29,
    "Asparagus Pie": 30,
    "Wild Chocomato": 31,
    "Cinnamon Swirl": 32,
    "Anchovies": 33,
    "Flaming Fire Faerie Pizza": 34,
    "Orange Negg": 35,
    "Fish Negg": 36,
    "Super Lemon Grape Slush": 37,
    "Rasmelon": 38,
    "Mustard Ice Cream": 39,
    "Worm and Leech Pizza": 40,
}

ARENA_NAMES = ["Shipwreck", "Lagoon", "Treasure", "Hidden", "Harpoon"]

PIRATE_NAMES = {
    "Scurvy Dan the Blade": 1,
    "Young Sproggie": 2,
    "Orvinn the First Mate": 3,
    "Lucky McKyriggan": 4,
    "Sir Edmund Ogletree": 5,
    "Peg Leg Percival": 6,
    "Bonnie Pip Culliford": 7,
    "Puffo the Waister": 8,
    "Stuff-A-Roo": 9,
    "Squire Venable": 10,
    "Captain Crossblades": 11,
    "Ol' Stripey": 12,
    "Ned the Skipper": 13,
    "Fairfax the Deckhand": 14,
    "Gooblah the Grarrl": 15,
    "Franchisco Corvallio": 16,
    "Federismo Corvallio": 17,
    "Admiral Blackbeard": 18,
    "Buck Cutlass": 19,
    "The Tailhook Kid": 20,
}


if __name__ == "__main__":
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in sorted(files):
            foods: List[List[int]] = []
            pirates: List[List[int]] = []
            current_odds: List[List[int]] = []
            opening_odds: List[List[int]] = []
            winners: List[int] = [0, 0, 0, 0, 0]
            round: int = 0
            errors: List[str] = []

            with open(folder / name, "r") as f:
                js = json.loads(f.read())
                round = int(js["round"])

                if len(js['arenas']) == 0:
                    errors.append("MISSING_ARENAS")
                else:
                    for arena_index in range(5):
                        arena = js["arenas"][arena_index]

                        these_pirates: List[int] = []
                        these_foods: List[int] = [FOODS[f] for f in arena["foods"]]
                        these_opening: List[int] = []
                        these_current: List[int] = []
                        for pirate_index in range(4):
                            these_pirates.append(
                                PIRATE_NAMES[arena["pirates"][pirate_index]]
                            )
                            this_pirate = js["pirates"][arena_index * 4 + pirate_index]
                            if current := this_pirate["current"]:
                                these_current.append(int(current.split(":")[0]))
                            if opening := this_pirate["opening"]:
                                these_opening.append(int(opening.split(":")[0]))
                            if this_pirate["won"]:
                                winners[arena_index] = pirate_index + 1

                        pirates.append(these_pirates)
                        foods.append(these_foods)
                        current_odds.append([1] + these_current)
                        opening_odds.append([1] + these_opening)

                if len(current_odds) != 5:
                    errors.append('MISSING_CURRENT_ODDS')
                if len(opening_odds) != 5:
                    errors.append('MISSING_OPENING_ODDS')
                if sum(winners) == 0:
                    errors.append('MISSING_WINNERS')

                if len(errors) == 0:
                    with open(fixedfolder / name, "w") as f:
                        data = dict(
                            pirates=pirates,
                            currentOdds=current_odds,
                            openingOdds=opening_odds,
                            winners=winners,
                            foods=foods,
                            round=round,
                        )
                        f.write(json.dumps(data, separators=(",", ":")))
                    print(f'[PASSED] - {name}')
                else:
                    print(f'[FAILED] - {name} - ERRORS: {", ".join(errors)}')
