#!/usr/bin/python
import json, os, sys
sys.path.append("/var/projects/tf2tags")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
from schema.models import *
from datetime import datetime

ALL_CLASS_VALUE = "0"
SLOT_OVERRIDE = {"building":"pda", "taunt":"action"}

def main():
    start = str(datetime.now())

    """
    while True:
        temp = Item.objects.get(pk=int(raw_input("defindex:")))
        print temp

    print "DONE."
    sys.exit()
    """

    class_values = {"Scout":"1", "Soldier":"2", "Pyro":"3", "Demoman":"4", "Heavy":"5", "Engineer":"6", "Medic":"7", "Sniper":"8", "Spy":"9"}
    # Open schema
    with open(os.path.join("/var/projects/tf2tags/assets/data/unusualSchema.json")) as f:
        schema = f.read()

    # Everything we care about is within the items section
    #schema = json.loads(schema)["result"]["items"]
    schema = json.loads(schema)["items"]
    print "Read schema."

    for entry in schema:
        # Produce Item
        item = Item()

        # Standard values
        keys = ["defindex", "craft_class", "craft_material_type", "drop_type", "holiday_restriction", "image_inventory", "image_url",
            "image_url_large", "item_class", "item_description", "item_name", "item_quality", "item_set", "item_type_name",
            "max_ilevel", "min_ilevel", "model_player", "name", "proper_name"]
        for key in keys:
            setattr(item, key, entry.get(key))

        if entry.get("item_slot"):
            if entry["item_slot"] in SLOT_OVERRIDE.keys():
                item.item_slot = SLOT_OVERRIDE[entry["item_slot"]]
            else:
                item.item_slot = entry["item_slot"]


        if item.defindex % 100 == 0:
            print item.defindex

        if entry.get("attributes"):
            item.attributes = json.dumps(entry["attributes"])

        if entry.get("per_class_loadout_slots"):
            item.per_class_loadout_slots = json.dumps(entry["per_class_loadout_slots"])

        if entry.get("tool"):
            item.tool = json.dumps(entry["tool"])

        if entry.get("used_by_classes"):
            item.used_by_classes = ""
            for role in entry["used_by_classes"]:
                item.used_by_classes += class_values[role]
        else:
            item.used_by_classes = ALL_CLASS_VALUE

        item.save()

        # Rarities
        rarity = Rarity(defindex=item)
        if entry.get("rarities"):
            if "Collector's" in entry["rarities"]:
                rarity.collectors = True
            if "Community" in entry["rarities"]:
                rarity.community = True
            if "Customized" in entry["rarities"]:
                rarity.customized = True
            if "Genuine" in entry["rarities"]:
                rarity.genuine = True
            if "Haunted" in entry["rarities"]:
                rarity.haunted = True
            if "Self-Made" in entry["rarities"]:
                rarity.self_made = True
            if "Strange" in entry["rarities"]:
                rarity.strange = True
            if "Unique" not in entry["rarities"]:
                rarity.unique = False
            if "Unusual" in entry["rarities"]:
                rarity.unusual = True
            if "Vintage" in entry["rarities"]:
                rarity.vintage = True
        elif item.defindex < 35:
                rarity.normal = True
                rarity.unique = False
        rarity.save()

        # Capabilities
        if entry.get("capabilities"):
            capability = Capability(defindex=item)
            keys = ["can_be_restored", "can_card_upgrade", "can_collect", "can_consume", "can_craft_count", "can_craft_if_purchased",
                    "can_craft_mark", "can_customize_texture", "can_gift_wrap", "can_killstreakify", "can_spell_page", "can_strangify",
                    "decodable", "nameable", "paintable", "strange_parts", "usable", "usable_gc", "usable_out_of_game"]
            for key in keys:
                setattr(capability, key, entry["capabilities"].get(key, False))

            if item.defindex < 35:
                capability.nameable = False
            capability.save()

        # Styles
        if entry.get("styles"):
            num = 0
            for style_name in entry["styles"]:
                style, created = Style.objects.get_or_create(defindex=item, style_num=num)
                style.name = style_name.get("name", "Unknown Style").strip()
                num += 1
                style.save()


    print start
    print datetime.now()
    return

if __name__ == "__main__": main()
