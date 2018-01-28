// tf2.js - Lots of arrays - 2015-08-17

var classes = ["Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy", "All", "April"];
var slots = ["primary", "secondary", "melee", "pda", "pda2", "misc", "action"];

var rarity_classes = {"Normal":"Normal", "Unique":"Unique", "Vintage":"Vintage", "Genuine":"Genuine", 
    "Strange":"Strange", "Unusual":"Unusual", "Haunted":"Haunted", "Collector's":"Collector", 
    "Community":"Community", "Self-Made":"Self-Made", "Valve":"Valve"};
        
var rarities_strange = ["Unremarkable", "Scarcely Lethal", "Mildly Menacing", "Somewhat Threatening", "Uncharitable", "Notably Dangerous", 
    "Sufficiently Lethal", "Truly Feared", "Spectacularly Lethal", "Gore-Spattered", "Wicked Nasty", "Positively Inhumane", 
    "Totally Ordinary", "Face-Melting", "Rage-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Hale's Own"];
        
var rarities_holiday_punch = ["Unremarkable", "Almost Amusing", "Mildly Mirthful", "Somewhat Droll", "Thigh-Slapping", 
    "Notably Cheery", "Sufficiently Wry", "Truly Feared", "Spectacularly Jocular", "Riotous", "Wicked Funny", "Totally Unamusing", 
    "Positively Persiflagious", "Frown-Annihilating", "Grin-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Mann Co. Select"];
    
var rarities_mantreads = ["Broken-In", "Scarcely Worn", "Mildly Minatory", "Crushingly Crushing", "Inauspicious", "Profoundly Penumbric", 
    "Sufficiently Eclipsing", "Truly Tenebrific", "Spectacularly Fell", "Fashion-Splattered", "Wicked Stinky", "Positively Planar", 
    "Totally Comfortable", "Face-Flattening", "Rage-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Hale's Custom"];
        
var rarities_sapper = ["Unremarkable", "Scarcely Shocking", "Mildly Magnetizing", "Somewhat Inducting", "Unfortunate", "Notably Deleterious",
    "Sufficiently Ruinous", "Truly Conducting", "Spectacularly Pseudoful", "Ion-Spattered", "Wickedly Dynamizing", "Positively Plasmatic", 
    "Totally Ordinary", "Circuit-Melting", "Nullity-Inducing", "Server-Clearing", "Epic", "Legendary", "Australian", "Mann Co. Select"];
        
var rarities_spirit_of_giving = ["The", "The Baseline Benefactor's", "The Competent Contributor's", "The Adequate Altruist's", "The Satisfactory Santa's", 
    "The Sufficient Samaritan's", "The Distinguished Donator's", "The Dynamic Do-Gooder's", "The Consumate Contributor's", "The Baron of Bequeathment's", 
    "The Lord of Largesse's", "The Chieftain of Charity's", "The Generalissimo of Generosity's", "The Bigshot Benefactor's", "The Caesar of Pleasers'", 
    "The First-Class Philanthropist's", "The Humanitarian Hotshot's", "The Selfless Samaritan's", "The Uber-Altruist's", "Saxton's Own"];
        
var rarities_cosmetic = ["Ragged", "Tacky", "Secondhand", "Odious", "Garish", "Comfortable", "Dapper", "Sharp", "Fancy", "Fancy Schmancy", "Fashionable",
    "Glamorous", "Posh", "Fabulous", "Stunning", "Epic", "Legendary", "Australian", "Mann Co. Select", "Mannceaux Signature Collection"];
        
var particles = ["Abduction", "Aces High", "Amaranthine", "Ancient Codex", "Ancient Eldritch", "Anti-Freeze", "Arcana", "Atomic", "Blizzardy Storm", "Bonzo The All-Gnawing", "Bubbling", "Burning Flames", "Cauldron Bubbles", 
    "Chiroptera Venenata", "Circling Heart", "Circling Peace Sign", "Circling TF Logo","Cloud 9", "Cloudy Moon", "Darkblaze", "Dead Presidents", "Death at Dusk", "Death by Disco",
    "Demonflame", "Disco Beat Down", "Eerie Orbiting Fire", "Eldritch Flame", "Electric Hat Protector", "Electrostatic", "Ether Trail", "Flaming Lantern", "Frostbite", "Galactic Codex", "Ghastly Ghosts Jr.", "Green Black Hole", "Green Confetti", 
    "Green Energy", "Harvest Moon", "Haunted Ghosts", "Haunted Phantasm Jr.", "Hellfire", "It's a mystery to everyone", "It's a puzzle to me", "It's A Secret To Everybody", "Kill-a-Watt", "Knifestorm", "Magnetic Hat Protector", "Massed Flies", 
    "Memory Leak", "Miami Nights", "Misty Skull", "Molten Mallard", "Morning Glory", "Nebula", "Nether Trail", "Nuts and Bolts", "The Ooze", "Orbiting Fire", "Orbiting Planets", "Overclocked",
    "Phosphorous", "Poisoned Shadows", "Power Surge", "Purple Confetti", "Purple Energy", "Roboactive", "Scorching Flames", "Searing Plasma", "Smoking", 
    "Something Burning This Way Comes", "Spellbound", "Stare From Beyond", "Steaming", "Stormy 13th Hour", "Stormy Storm", "Subatomic", "Sunbeams", "Sulphurous", "Terror-Watt", 
    "Time Warp", "Vivid Plasma", "Voltaic Hat Protector"];