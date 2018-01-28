# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import django
import glob
import os
import sys
import shutil

try:
    from PIL import Image, ImageFont, ImageDraw
except:
    print "PIL NOT FOUND"

sys.path.append("/var/projects/tf2tags")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
django.setup()
from schema.models import *


def main():
    files = glob.glob("/var/projects/tf2tags/tools/skins/*.png")

    weapons = [
        "Scattergun", "Pistol",
        "Rocket_Launcher", "Shotgun",
        "Flame_Thrower",
        "Grenade_Launcher", "Stickybomb_Launcher",
        "Minigun",
        "Wrench",
        "Medi_Gun",
        "Sniper_Rifle", "SMG",
        "Revolver", "Knife",
    ]
    defindexes = {"Scattergun":200, "Pistol":209,
        "Rocket Launcher":205, "Shotgun":199,
        "Flame Thrower":208,
        "Grenade Launcher":206, "Stickybomb Launcher":207,
        "Minigun":202,
        "Wrench":197,
        "Medi Gun":211,
        "Sniper Rifle":201, "SMG":203,
        "Revolver":210, "Knife":194
    }

    for file in files:
        base = os.path.basename(file).replace("200px-Backpack_", "")

        # Detect Wear
        if "Factory_New" in base:
            wear = "Factory New"
        elif "Minimal_Wear" in base:
            wear = "Minimal Wear"
        elif "Field-Tested" in base:
            wear = "Field-Tested"
        elif "Well-Worn" in base:
            wear = "Well-Worn"
        elif "Battle_Scarred" in base:
            wear = "Battle Scarred"


        style = base.replace("_" + wear + ".png", "")
        item = ""

        for weapon in weapons:
            idx = style.rfind(weapon)
            if idx != -1:
                item = weapon
                style = style[:idx-1]
                break

        style_name = style.replace("_", " ")
        item = item.replace("_", " ")
        print "File:", file
        print "Style:", style_name
        print "Wear:", wear
        print "Item:", item

        # Create the style if it doesn't exist
        styles = Style.objects.filter(defindex_id=defindexes[item]).order_by("-style_num")
        exists = False
        style_num = 0

        if styles:
            style_num = styles[0].style_num + 1
        else:
            # For items which don't have styles at all yet
            new_style = Style(defindex_id=defindexes[item], style_num=0, name="Default")
            new_style.save()
            style_num += 1


        for style in styles:
            if style.name == style:
                exists = True
                print "Style", style, "already exists. Skipping"
                break

        if not exists:
            new_style = Style(defindex_id=defindexes[item], style_num=style_num, name=style_name)
            new_style.save()
            print "Saved style", style_name
        else:
            print "Already saved style, just moving the image"

        # Move it to the proper directory
        new_file = "/var/projects/tf2tags/assets/items/"+str(defindexes[item])+"-"+str(style_num)+".png"
        #print file
        #print new_file
        shutil.copy(file, new_file)

        print "-"*30
    return True

if __name__ == "__main__":
    main()
