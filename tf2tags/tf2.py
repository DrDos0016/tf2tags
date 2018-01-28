"""TF2 Specific Classes and Functions"""
import json
import glob
import os
from schema.models import *

try:
    from tf2tags.models import *
except:
    print("tf2tags.models not found!")

APRIL       = False # April Fool's Week

class TF(object):
    def __init__(self):
        self.classes = ["Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy", "All"]
        self.classdict = {"All":"0", "Scout":"1", "Soldier":"2", "Pyro":"3", "Demoman":"4", "Heavy":"5", "Engineer":"6", "Medic":"7", "Sniper":"8", "Spy":"9", "April":"A"}
        self.botclasses = ["Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy"]
        self.slots = ["primary", "secondary", "melee", "pda", "pda2", "misc", "action"]
        self.is_april = APRIL

        # slot4 is building in the case of the sapper, and pda in the case of the construction PDA and non-nameable disguise kit. Schema edits will make sappers PDAs.

        self.rarities = ["Normal", "Unique", "Vintage", "Genuine", "Strange", "Unusual", "Haunted", "Collector's", "Community", "Self-Made", "Valve"]
        self.colors = {"Normal":"#B2B2B2",
            "Unique":"#FFD700",
            "Vintage":"#476291",
            "Genuine":"#4D7455",
            "Strange":"#CF6A32",
            "Unusual":"#8650AC",
            "Haunted":"#38F3AB",
            "Collector's":"#AA0000",
            "Community":"#70B04A",
            "Self-Made":"#70B04A",
            "Valve":"#A50F79",
            "":"#FFD700"}

        self.all_colors_list = ["cf6a32", "b2b2b2", "ffd700", "476291", "4d7455", "8650ac", "38f3ab", "aa0000", "70b04a", "a50f79"]
        """
        For strange ranks do not include strange! It's covered by it being marked as possibly strange.
        """
        self.rarities_strange = ["Unremarkable", "Scarcely Lethal", "Mildly Menacing", "Somewhat Threatening", "Uncharitable", "Notably Dangerous",
        "Sufficiently Lethal", "Truly Feared", "Spectacularly Lethal", "Gore-Spattered", "Wicked Nasty", "Positively Inhumane",
        "Totally Ordinary", "Face-Melting", "Rage-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Hale's Own"]

        self.rarities_holiday_punch = ["Unremarkable", "Almost Amusing", "Mildly Mirthful", "Somewhat Droll", "Thigh-Slapping",
        "Notably Cheery", "Sufficiently Wry", "Truly Feared", "Spectacularly Jocular", "Riotous", "Wicked Funny", "Totally Unamusing",
        "Positively Persiflagious", "Frown-Annihilating", "Grin-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Mann Co. Select"]

        self.rarities_mantreads = ["Broken-In", "Scarcely Worn", "Mildly Minatory", "Crushingly Crushing", "Inauspicious", "Profoundly Penumbric",
        "Sufficiently Eclipsing", "Truly Tenebrific", "Spectacularly Fell", "Fashion-Splattered", "Wicked Stinky", "Positively Planar",
        "Totally Comfortable", "Face-Flattening", "Rage-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Hale's Custom"]

        # Sapper / Invis Watch
        self.rarities_sapper = ["Unremarkable", "Scarcely Shocking", "Mildly Magnetizing", "Somewhat Inducting", "Unfortunate", "Notably Deleterious",
        "Sufficiently Ruinous", "Truly Conducting", "Spectacularly Pseudoful", "Ion-Spattered", "Wickedly Dynamizing", "Positively Plasmatic",
        "Totally Ordinary", "Circuit-Melting", "Nullity-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Mann Co. Select"]

        self.rarities_spirit_of_giving = ["The", "The Baseline Benefactor's", "The Competent Contributor's", "The Adequate Altruist's", "The Satisfactory Santa's",
        "The Sufficient Samaritan's", "The Distinguished Donator's", "The Dynamic Do-Gooder's", "The Consumate Contributor's", "The Baron of Bequeathment's",
        "The Lord of Largesse's", "The Chieftain of Charity's", "The Generalissimo of Generosity's", "The Bigshot Benefactor's", "The Caesar of Pleasers'",
        "The First-Class Philanthropist's", "The Humanitarian Hotshot's", "The Selfless Samaritan's", "The Uber-Altruist's", "Saxton's Own"]

        # Hats/Miscs
        self.rarities_cosmetic = ["Ragged", "Tacky", "Secondhand", "Odious", "Garish", "Comfortable", "Dapper", "Sharp", "Fancy", "Fancy Schmancy", "Fashionable",
        "Glamorous", "Posh", "Fabulous", "Stunning", "Epic", "Legendary", "Australian", "Mann Co. Select", "Mannceaux Signature Collection"]

        # These are for validation, edit advOptions.html to actually change what shows up
        self.filters = ["Canadian", "Chaotic", "Covert", "Dazzling", "Efficient", "Egyptian", "Fresh", "Frosty", "Hydraulic", "Locomotive", "Mennko", "Outlaw",
        "Psychadelic", "Rigid", "Rugged", "Sophisticated", "Spooky", "Sun-Kissed", "Technical", "Vigilant", "Venomous", "Wild"]

        # Particles
        self.particles = ["Abduction", "Aces High", "Amaranthine", "Ancient Codex", "Ancient Eldritch", "Anti-Freeze", "Arcana", "Atomic", "Blizzardy Storm", "Bonzo The All-Gnawing", "Bubbling", "Burning Flames", "Cauldron Bubbles",
            "Chiroptera Venenata", "Circling Heart", "Circling Peace Sign", "Circling TF Logo","Cloud 9", "Cloudy Moon", "Darkblaze", "Dead Presidents", "Death at Dusk", "Death by Disco",
            "Demonflame", "Disco Beat Down", "Eerie Orbiting Fire", "Eldritch Flame", "Electric Hat Protector", "Electrostatic", "Ether Trail", "Flaming Lantern", "Frostbite", "Galactic Codex", "Ghastly Ghosts Jr.", "Green Black Hole", "Green Confetti",
            "Green Energy", "Harvest Moon", "Haunted Ghosts", "Haunted Phantasm Jr.", "Hellfire", "It's a mystery to everyone", "It's a puzzle to me", "It's A Secret To Everybody", "Kill-a-Watt", "Knifestorm", "Magnetic Hat Protector", "Massed Flies",
            "Memory Leak", "Miami Nights", "Misty Skull", "Molten Mallard", "Morning Glory", "Nebula", "Nether Trail", "Nuts and Bolts", "The Ooze", "Orbiting Fire", "Orbiting Planets", "Overclocked",
            "Phosphorous", "Poisoned Shadows", "Power Surge", "Purple Confetti", "Purple Energy", "Roboactive", "Scorching Flames", "Searing Plasma", "Smoking",
            "Something Burning This Way Comes", "Spellbound", "Stare From Beyond", "Steaming", "Stormy 13th Hour", "Stormy Storm", "Subatomic", "Sunbeams", "Sulphurous", "Terror-Watt",
            "Time Warp", "Vivid Plasma", "Voltaic Hat Protector"]

        self.particles_special = ["Flying Bits", "Nemesis Burst", "Community Sparkle", "Holy Glow", "Map Stamps", "Genteel Smoke"]

        # HSV Sorted
        self.paints = ["A Distinctive Lack of Hue", "Aged Moustache Grey", "An Extraordinary Abundance of Tinge", "Operator's Overalls (RED)", "The Value of Teamwork (RED)",
            "An Air of Debonair (RED)", "Dark Salmon Injustice", "Radigan Conagher Brown", "Mann Co. Orange", "Cream Spirit (RED)", "Waterlogged Lab Coat (RED)", "Muskelmannbraun",
            "Peculiarly Drab Tincture", "Ye Olde Rustic Colour", "Cream Spirit (BLU)", "Australium Gold", "The Color of a Gentlemann's Business Pants", "After Eight", "Drably Olive",
            "Indubitably Green", "Zepheniah's Greed", "A Mann's Mint", "The Bitter Taste of Defeat and Lime", "A Color Similar to Slate", "Waterlogged Lab Coat (BLU)",
            "The Value of Teamwork (BLU)", "Operator's Overalls (BLU)", "Team Spirit (BLU)", "An Air of Debonair (BLU)", "Balaclavas are Forever (BLU)", "Color No. 216-190-216",
            "A Deep Commitment to Purple", "Noble Hatter's Violet", "Pink as Hell", "Balaclavas are Forever (RED)", "Team Spirit (RED)"]

        self.hex = ["141414", "7E7E7E", "E6E6E6", "483838", "803020", "654740", "E9967A", "694D3A", "CF7336", "C36C2D", "A89A8C", "A57545", "C5AF91", "7C6C57", "B88035", "E7B53B",
            "F0E68C", "2D2D24", "808000", "729E42", "424F3B", "BCDDB3", "32CD32", "2F4F4F", "839FA3", "256D8D", "384248", "5885A2", "28394D", "18233D", "D8BED8", "7D4071", "51384A",
            "FF69B4", "3B1F23", "B8383B"]

        if APRIL:
            self.april()

    def validate(self, item):
        if APRIL:
            return "SUCCESS"

        errors = []

        # Verify item exists
        rules = Item.objects.filter(pk=int(item.defindex))
        if not rules:
            return "Item with defindex #"+str(item.defindex)+" does not exist."
        else:
            rules = rules[0]

        # Role
        if self.classdict[item.role] not in rules.used_by_classes:
            errors.append(item.role + " is not a valid class for the item #" + str(item.defindex))
        # Verify slot
        if item.slot not in rules.item_slot:
            if item.defindex == 199 and item.slot not in ["primary", "secondary"]:
                errors.append(item.slot + " is not the correct slot for the item #" + str(item.defindex))

        # Verify base
        if item.base[:4] == "The ": # Remove leading The if it exists
            adj_base = item.base[4:]
        else:
            adj_base = item.base
        if adj_base not in rules.item_name:
            errors.append(item.base + " does not match the defindex given ("+str(item.defindex)+")")

        # Verify prefix (if any)
        strange = False
        if (item.prefix == "Strange"):
            strange = True
        if (item.prefix != "") and (item.prefix not in rules.rarity.all()):
            # Check for strange variant
            if (item.prefix in self.rarities_strange) or (item.prefix in self.rarities_mantreads) or (item.prefix in self.rarities_holiday_punch) or (item.prefix in self.rarities_sapper) or (item.prefix in self.rarities_spirit_of_giving) or (item.prefix in self.rarities_cosmetic):
                strange = True
            else:
                errors.append(item.prefix + " is not a valid rarity for the item." + str(item.defindex))

        # Verify color
        if item.prefix == "":
            item.prefix = "Unique"
        rarity_name = item.prefix.title()

        if (rarity_name == "Collector'S"): # Collector's hotfix
            rarity_name = "Collector's"

        if ("#"+item.color.upper()) != self.colors.get(rarity_name):
            if not (strange and (item.color.lower() in self.all_colors_list)):
                errors.append(item.color + " is not a valid color for an item of rarity " + item.prefix + " " + str(item.defindex))
        if item.prefix == "Unique":
            item.prefix = ""

        # Verify filter (if any)
        if item.filter != "" and not strange:
            errors.append("Filters cannot be added a non-strange item.")
        elif item.filter != "" and item.filter not in self.filters:
            errors.append(item.filter + " is not a valid filter for the item."  + str(item.defindex))

        # Verify paint (if any)
        if item.paint != "" and rules.paintable:
            if item.paint not in self.hex:
                errors.append(item.paint + " is not a valid color paint."  + str(item.defindex))

        # Verify particles (if any)
        if item.particles != "" and item.prefix in ["Self-Made", "Community"]:
            if item.particles != "Community Sparkle":
                errors.append(item.particles + " is not a valid particle effect " + str(item.defindex))
        elif item.particles != "" and item.prefix == "Valve":
            if item.particles != "Flying Bits":
                errors.append(item.particles + " is not a valid particle effect "  + str(item.defindex))
        elif item.particles != "" and item.prefix == "Unusual":
            if item.particles not in self.particles:
                errors.append(item.particles + " is not a valid particle effect "  + str(item.defindex))
        elif item.particles != "":
            errors.append(item.particles + " is not a valid particle effect for " + item.prefix + " items"  + str(item.defindex))

        # Verify style (if any)
        #if int(item.style) >= len(data.get("styles", "1")):
        #    errors.append(item.style + " is not a valid style number for the item."  + str(item.defindex))

        # DEBUG
        """
        if (item.particles != ""):
            errors.append("Test error")
        else:
            print "PARTICLES--"+item.particles+"--"
        """

        if errors == []:
            return "SUCCESS"

        return "\n".join(errors)

    def getRank(self, points):
        if points is None:
            rank = 0
        elif points >= 8500:
            rank = 20
        elif points >= 7616:
            rank = 19
        elif points >= 7500:
            rank = 18
        elif points >= 5000:
            rank = 17
        elif points >= 2500:
            rank = 16
        elif points >= 1500:
            rank = 15
        elif points >= 1000:
            rank = 14
        elif points == 999:
            rank = 13
        elif points >= 750:
            rank = 12
        elif points >= 500:
            rank = 11
        elif points >= 350:
            rank = 10
        elif points >= 275:
            rank = 9
        elif points >= 225:
            rank = 8
        elif points >= 175:
            rank = 7
        elif points >= 135:
            rank = 6
        elif points >= 100:
            rank = 5
        elif points >= 70:
            rank = 4
        elif points >= 45:
            rank = 3
        elif points >= 25:
            rank = 2
        elif points >= 10:
            rank = 1
        else:
            rank = 0
        if rank == 0:
            return "Strange"
        else:
            return self.rarities_strange[rank-1]


    def april(self):
        self.classes.append("April")
        self.slots = self.slots + ["a_doom", "a_mlp", "a_poke", "a_portal", "a_regular", "a_tf2", "a_valve", "a_who", "a_april", "a_ut", "a_su"]
        self.particles = self.particles + self.particles_special + []
        self.rarities += self.rarities_strange
        self.rarities += self.rarities_holiday_punch
        self.rarities += self.rarities_mantreads
        self.rarities += self.rarities_sapper
        self.rarities += self.rarities_cosmetic
        self.rarities += self.rarities_spirit_of_giving
        self.rarities += ["Buff the", "Nerf the", "Kurt Cobain's", "Ayn Rand's", "Well-Intentioned", "Rapping", "Dr. Dos'", "Dark",
            "Team Rocket's", "Questionable", "Ugly", "A Distinctive Lack Of", "An extraordinary Abundance Of", "Facebook's Own", "An extraordinary Lack Of",
            "A Distinctive Abundance Of", "Underpowered", "Overpowered", "Fairly Balanced", "Fused"]
        self.april_filters = ["Magical", "Under-Rated", "Over-Rated", "Sensual", "Mysterious", "Home-Made", "Artificial", "Glistening", "Wet", "Dry", "Spicy",
            "Vegetarian", "Raggedy", "Gross", "Equestrian", "Infernal", "Mann Co.", "Aperture", "Dalek", "Misconfigured", "Malfunctioning", "Polite",
            "A Distinctive Lack Of", "An extraordinary Abundance Of", "An extraordinary Lack Of", "A Distinctive Abundance Of"
            ]
        self.april_filters = sorted(self.april_filters)

def deleteItem(id):
    Submissions.objects.filter(pk=id).delete()
    Votes.objects.filter(itemID=id).delete()
    Comments.objects.filter(itemID=id).delete()

def deleteVotes(id):
    Votes.objects.filter(itemID=id).delete()
