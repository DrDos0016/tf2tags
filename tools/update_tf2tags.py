# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

"""
This script is to execute automatically and nightly to update the items on tf2tags
NO OTHER FILES SHOULD BE NECESSARY INCLUDING THE SCHEMA APP OR UNUSUALSCHEMA SCRIPTS
"""
import json, urllib, codecs, os
import urllib.request
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import sys, smtplib
from sys import exit
#from wikitools import wiki, api, page

import django, codecs
sys.path.append("/var/projects/tf2tags")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
django.setup()
from schema.models import *
from django.template import Template, Context
from django.template.loader import get_template

KEY             = "TODO"
SCHEMA_URL      = "http://api.steampowered.com/IEconItems_440/GetSchema/v0001?key="+KEY+"&language=en"
TF2WIKI_API     = "https://wiki.teamfortress.com/w/api.php"
RARITIES_URL    = "https://wiki.teamfortress.com/w/index.php?title=Template:Dictionary/quad&action=raw"
SELF_MADE_URL   = "https://wiki.teamfortress.com/w/index.php?title=List_of_Self-Made_item_owners&action=raw"
IMAGE_ROOT      = "/var/projects/tf2tags/assets/items/"

KNOWN_RARITIES  = ["Normal", "Unique", "Haunted", "Vintage", "Genuine", "Strange", "Collector's", "Unusual", "Self-Made", "Community", "Valve", "Completed", "Customized", "rarity2", "rarity3"]
ALL_CLASS_VALUE = "0"
SLOT_OVERRIDE   = {"building":"pda", "taunt":"action"}
CLASS_VALUES = {"Scout":"1", "Soldier":"2", "Pyro":"3", "Demoman":"4", "Heavy":"5", "Engineer":"6", "Medic":"7", "Sniper":"8", "Spy":"9"}
PAINTS = ["141414", "18233D", "256D8D", "28394D", "2F4F4F", "32CD32", "384248", "3B1F23", "424F3B", "483838", "51384A", "5885A2", "654740", "694D3A", "729E42", "7C6C57", "7D4071", "7E7E7E", "803020", "808000", "839FA3", "A57545", "A89A8C", "B8383B", "B88035", "C36C2D", "C5AF91", "CF7336", "D8BED8", "E6E6E6", "E7B53B", "E9967A", "F0E68C", "FF69B4", "2D2D24", "BCDDB3"]

def main():
    output = ""
    start_time = datetime.now()
    errors = 0
    warnings = 0

    output += "============================================================\n"
    output += "UPDATE TF2TAGS\n"
    output += "SCRIPT START: " + str(start_time)[:19] + "\n"
    output += "SCRIPT END  : {{end}}\n"
    output += "============================================================\n"
    output += "ORDER OF OPERATIONS\n"
    output += "   I. Download item schema from Valve\n"
    output += "  II. Check for New Rarities\n"
    output += " III. Download rarities from tf2wiki\n"
    output += "  IV. Download images from Valve\n"
    output += "   V. Handle Edge Cases\n"
    output += "  VI. Download Painted Images from tf2wiki\n"
    output += " VII. Compress PNGs\n"
    output += "VIII. Update site database\n"
    output += "  IX. Generate raw data HTML page\n"
    output += "   X. Email script report\n"

    ################################################################################
    output += "============================================================\n"
    output += "I.   Download item schema from Valve\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " I.   Download item schema from Valve")

    try:
        schema_fh = urllib.request.urlopen(SCHEMA_URL)
        schema_txt = schema_fh.read().decode("utf-8")
        schema = json.loads(schema_txt)["result"]
        output += "SCHEMA SIZE: " + str(round(len(schema_txt) / 1024.0, 2)) + " KB\n"
        success = True
    except:
        errors += 1
        output += "ERROR: FAILED TO READ SCHEMA. ABORTING\n"
        success = False

    if not success:
        finish(output, errors, warnings)

    ################################################################################
    output += "============================================================\n"
    output += "II.   Check for New Rarities\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " II.   Check for New Rarities")
    found_unknown = False
    for k in schema["qualityNames"]:
        v = schema["qualityNames"][k]
        if v not in KNOWN_RARITIES:
            # Decorated Hotfix - TODO: Properly handle this
            if v == "Decorated Weapon":
                continue

            output += "WARNING: Found unknown rarity: " + v + "\n"
            found_unknown = True
            warnings += 1
    if not found_unknown:
        output += "No new rarities detected.\n"

    ################################################################################
    """
    output += "============================================================\n"
    output += "III.  Download rarities from tf2wiki\n".upper()
    output += "--------------------\n"
    print str(datetime.now())[:19] + " III.  Download rarities from tf2wiki"

    try:
        rarities_fh = urllib.urlopen(RARITIES_URL)
        rarities_txt = rarities_fh.readlines()

        output += "Parsing tf2wiki rarities page\n"
        rarities = {}

        mode = "search"
        for line in rarities_txt:
            line = unicode(line.decode("utf-8")).strip().replace("collectors:", "collector's:")
            #print "LINE:" , line, "--END"
            if line == "":
                mode = "search"
                continue

            if mode == "search" and line[-1] == ":":

                # HOTFIX - SMG
                if line == "submachine gun | smg:":
                    line = "smg:"

                # HOTFIX - Construction PDA
                if line == "construction pda | pda:":
                    line = "construction pda:"

                # HOTFIX - ubersaw
                if line == "übersaw | ubersaw:":
                    line = "ubersaw:"

                # HOTFIX - high five
                if line == "high five | high five!:":
                    line = "the high five!:"

                # HOTFIX - athletic supporter
                if line == "athletic supporter:":
                    line = "the athletic supporter:"

                # HOTFIX - superfan
                if line == "superfan:":
                    line = "the superfan:"

                # HOTFIX - essential accessories
                if line == "essential accessories:":
                    line = "the essential accessories:"

                # HOTFIX - high five
                if line == "high five | high five!:":
                    line = "high five!:"

                # HOTFIX - meet the medic
                if line == "meet the medic (taunt):":
                    line = "meet the medic:"

                # HOTFIX - Quackenbirdt
                if line == "quäckenbirdt | quackenbirdt:":
                    line = "quäckenbirdt:"

                # HOTFIX - Festive Ubersaw
                if line == "festive übersaw:":
                    line = "festive ubersaw:"

                mode = "acquire"
                item = line[:-1]
                rarities[item] = {}
                #print item, " IS AN ITEM"
                continue

            if mode == "acquire":
                rarity = line.split(":")[0]
                rarities[item][rarity] = True
                continue

    except:
        errors += 1
        output += "ERROR: FAILED TO READ TF2WIKI RARITIES TEMPLATE. ABORTING\n"
        finish(output, errors, warnings)

    del rarities_fh
    del rarities_txt
    output += "Rarities page parsed. Assigning rarities to items.\n"

    rarity_count = {}
    for rarity in KNOWN_RARITIES:
        rarity_count[rarity] = 0

    for item in schema["items"]:
        item["rarities"] = {}
        name = item["item_name"]
        key = name.lower()
        defindex = item["defindex"]

        # HOTFIX - Various taunts
        if name[:11] == "Taunt: The ":
            key = name[11:].lower()
        elif name[:7] == "Taunt: ":
            key = name[7:].lower()

        if defindex < 35:
            item["rarities"]["Normal"] = True
            rarity_count["Normal"] = rarity_count.get("Normal", 0) + 1

        #KNOWN_RARITIES = ["Haunted", "Vintage", "Genuine", "Strange", "Collector's", "Unusual", "Self-Made", "Community", "Completed", "Customized", "rarity2", "rarity3"]
        item["rarities"]["Unique"]      = True
        item["rarities"]["Community"]   = True
        item["rarities"]["Valve"]       = True
        rarity_count["Unique"] = rarity_count.get("Unique", 0) + 1
        rarity_count["Community"] = rarity_count.get("Community", 0) + 1
        rarity_count["Valve"] = rarity_count.get("Valve", 0) + 1

        # HOTFIX - Items to ignore
        if (defindex in [28, 122, 123, 124, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 850, 30572, 30609, 30614, 30391, 5084, 5043]) or defindex in range(15000,16000):
            # Duplicate PDA, Idler Violation, Idler Violation 2, Non-Idler, 1057-1065 TF_GateBot_Light, Deflector MvM minigun,
            # Boston Breakdance, Killer Solo, Most Wanted, Sengoku Scorcher, Giftapult, Gift
            # Range is Contract Decorated Weapons
            continue

        try:
            print "TRY", defindex
            if not item.get("capabilities") or not item["capabilities"].get("nameable"):
                continue

            # HOTFIX Botkillers
            if "botkiller" in key:
                #print "Manually setting rarities for ", name
                item["rarities"]["Unique"] = False
                item["rarities"]["Strange"] = True
                rarity_count["Unique"] = rarity_count.get("Normal", 0) - 1
                rarity_count["Strange"] = rarity_count.get("Normal", 0) - 1
                continue

            # HOTFIX Fortified Compound
            if defindex == 1092:
                item["rarities"]["Genuine"] = True
                rarity_count["Genuine"] = rarity_count.get("Genuine", 0) + 1
                continue

            # HOTFIX Rome MvM
            if defindex in [30143, 30144, 30145, 30146, 30147, 30148, 30149, 30150, 30151, 30152, 30153, 30154, 30155, 30156, 30157, 30158, 30159, 30160, 30161]:
                continue

            # HOTFIX Taunts
            if defindex == 167:
                key = "the high five!"
            elif defindex == 438:
                key = "director's vision"
            elif defindex == 463:
                key = "schadenfreude"
            elif defindex == 477:
                key = "meet the medic"
            elif defindex in [578, 579, 580]:
                key = "spine-chilling skull"

            print name, defindex, rarities[key].keys()
            for rarity in rarities[key].keys():
                item["rarities"][rarity.title().replace("Collector'S", "Collector's")] = True
                rarity_count[rarity.title()] = rarity_count.get(rarity.title(), 0) + 1
        except:
            warnings += 1
            output += "WARNING: Failed to set additional rarities for defindex/name/key: " + str(defindex) + " - " + name + " - " + key + "\n"

    output += "Non Self-Made rarities set\n"

    # Get Self-Made items
    try:
        selfmade_fh = urllib.urlopen(SELF_MADE_URL)
        selfmade_txt = selfmade_fh.readlines()
        selfmade_list = []
        for line in selfmade_txt:
            if line[:7] == " | item":
                line = unicode(line.decode("utf-8")).split("=")[1][1:].strip()
                selfmade_list.append(line)
        for item in schema["items"]:
            name = item["item_name"]
            defindex = item["defindex"]
            if name in selfmade_list:
                item["rarities"]["Self-Made"] = True
    except:
        errors += 1
        output += "ERROR: FAILED TO READ TF2WIKI SELF MADE ITEM OWNERS LIST. ABORTING\n"
        finish(output, errors, warnings)

    del selfmade_fh
    del selfmade_txt
    del selfmade_list

    output += "Final rarity counts:\n"
    for key in rarity_count.keys():
        output += (key + "               ")[:15] + str(rarity_count[key]) + "\n"
    """
    output += "============================================================\n"
    output += "III.  Download rarities from tf2wiki\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " III.  Assign Rarities based on slot")

    for item in schema["items"]:
        item["rarities"] = {}
        name = item["item_name"]
        key = name.lower()
        defindex = item["defindex"]
        slot = item.get("item_slot", "")

        if slot in ["melee", "pda", "pda2", "primary", "secondary"]:
            item["rarities"] = {"Unique":True, "Haunted":True, "Vintage":True, "Genuine":True, "Strange":True, "Collector's":True, "Self-Made":True, "Community":True, "Valve":True}
        elif slot == "misc":
            item["rarities"] = {"Unique":True, "Haunted":True, "Vintage":True, "Genuine":True, "Strange":True, "Collector's":True, "Self-Made":True, "Community":True, "Valve":True, "Unusual":True}
        if defindex == 266: # Headtaker
            item["rarities"]["Unusual"] = True

    ################################################################################
    output += "============================================================\n"
    output += "IV. Download images from Valve".upper() + "\n"
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " IV. Download images from Valve")

    dl_count = 0
    for item in schema["items"]:
        break  # DEBUG
        defindex = item["defindex"]

        # HOTFIX - MvM and Promos that will never have images
        if defindex in [1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1154, 1159, 1160, 1161, 2128, 2132, 2133, 2134, 2136, 2137, 2141, 2142]:
            continue
        name = item["item_name"]
        fname = str(defindex) + ".png"
        url = item["image_url"]
        if not os.path.isfile(IMAGE_ROOT + fname):
            try:
                ret = urllib.request.urlretrieve(url, os.path.join(IMAGE_ROOT, fname))
                dl_count += 1
            except:
                output += "WARNING: Could not retrieve image: " + str(fname) + " from " + str(url) + "\n"
                warnings += 1
    output += "Downloaded " + str(dl_count) + " images.\n"

    ################################################################################
    output += "============================================================\n"
    output += "V. Handle Edge Cases\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " V. Handle Edge Cases")

    try:
        cases = open("/var/projects/tf2tags/tools/edge_cases.dat").readlines()
    except:
        output += "ERROR: Could not read edge_cases.dat\n"
        finish(output, errors, warnings)

    for case in cases:
        #Comments
        if case[0] == "#":
            continue

        case = case.split(";")[0]
        data = case.split(" ")

        if data[0] == "DELETE":
            matched = False
            input = int(data[2])
            for count in range(0,len(schema["items"])):
                if schema["items"][count]["defindex"] == input:
                    del schema["items"][count]
                    output += "Removed item " + str(input) + "\n"
                    matched = True
                    break
            if not matched:
                output += "WARNING: Item not found for deletion: " + input + "\n"
                warnings += 1

        elif data[0] == "SET" and data[1] == "SLOT":
            defindex = int(data[2])
            input = data[3]
            matched = False
            for count in range(0,len(schema["items"])):
                if schema["items"][count]["defindex"] == defindex:
                    schema["items"][count]["item_slot"] = input
                    output += "Set slot for " + str(defindex) + " to " + input + "\n"
                    matched = True
                    break
            if not matched:
                output += "WARNING: Item not found for slot adjustment: " + input + "\n"
                warnings += 1

        elif data[0] == "TOGGLE" and data[1] == "PAINT":
            matched = False
            defindex = int(data[2])
            for count in range(0,len(schema["items"])):
                if schema["items"][count]["defindex"] == defindex:
                    if (schema["items"][count]["capabilities"].get("paintable", False)):
                        del schema["items"][count]["capabilities"]["paintable"]
                        output += "Removed paint for item " + str(defindex) + "\n"
                    else:
                        schema["items"][count]["capabilities"]["paintable"] = True
                        output += "Added paint for item " + str(defindex) + "\n"
                    matched = True
                    break
            if not matched:
                output += "WARNING: Item not found for paint adjustment: " + data + " " + str(defindex) + "\n"
                warnings += 1

        elif data[0] == "TOGGLE" and data[1] == "NAMING":
            matched = False
            defindex = int(data[2])
            for count in range(0,len(schema["items"])):
                if schema["items"][count]["defindex"] == defindex:
                    if (schema["items"][count]["capabilities"].get("nameable", False)):
                        del schema["items"][count]["capabilities"]["nameable"]
                        output += "Removed naming for item " + str(defindex) + "\n"
                    else:
                        schema["items"][count]["capabilities"]["nameable"] = True
                        output += "Added naming for item " + str(defindex) + "\n"
                    matched = True
                    break
            if not matched:
                output += "WARNING: Item not found for naming adjustment: " + data + " " + str(defindex) + "\n"
                warnings += 1

        elif data[0] == "REMOVE" and data[1] == "STYLES":
            matched = False
            defindex = int(data[2])
            for count in range(0,len(schema["items"])):
                if schema["items"][count]["defindex"] == defindex:
                    if schema["items"][count].get("styles", False):
                        del schema["items"][count]["styles"]
                    matched = True
                    output += "Removed styles for item " + str(defindex) + "\n"
                    break
            if not matched:
                output += "WARNING: Item not found for style removal: " + data + " " + str(defindex) + "\n"
                warnings += 1

        elif data[0] == "RENAME" and data[1] == "STYLE":
            matched = False
            defindex = int(data[2])
            style = int(data[3])
            name = data[4]
            for count in range(0,len(schema["items"])):
                if schema["items"][count]["defindex"] == defindex:
                    if schema["items"][count].get("styles", False):
                        schema["items"][count]["styles"][style]["name"] = name
                    matched = True
                    output += "Renamed style " + str(style) + " for item " + str(defindex) + "\n"
                    break
            if not matched:
                output += "WARNING: Item not found for style renaming: " + data + " " + str(defindex) + "\n"
                warnings += 1

        elif case.strip() != "":
                output += "WARNING: Unknown command given in edge_cases.dat: " + case + "\n"
                warnings += 1

    ################################################################################
    output += "============================================================\n"
    output += "VI. Download Painted Images from tf2wiki\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " VI. Download Painted Images from tf2wiki")

    saved_count = 0
    missing_count = 0

    # Initialize the font for placeholder images
    font = ImageFont.truetype("victor-pixel.ttf", 10)

    for item in schema["items"]:
        break # DEBUG
        paintable = item["capabilities"].get("paintable", False)
        no_styles = len(item.get("styles", [])) == 0
        if not paintable and no_styles:
            continue
        missing  = []
        for style in range(0,len(item.get("styles", "1"))):
            dlQueue = []
            styleNum = style

            if style == 0:
                style = ""
                styleName = ""
            else:
                style = "-" + str(style)
                styleName = item["styles"][styleNum]["name"].replace(" ", "_")

            # Check that the folder for paints exists, if not, make it
            defindex = str(item["defindex"])
            imagePath = os.path.join("/var/projects/tf2tags/assets/items", defindex)
            if not os.path.exists(imagePath):
                os.mkdir(imagePath)

            # See what paint images don't exist
            for paint in PAINTS:
                if paintable and not os.path.isfile(os.path.join(imagePath, paint + style + ".png")):
                    dlQueue.append(paint)

            if os.path.isfile(os.path.join(imagePath, "missing.txt")):
                missing_data = open(os.path.join(imagePath, "missing.txt")).readlines()
                for data in missing_data:
                    data = data.strip()
                    if data and data != "UNPAINTED":
                        dlQueue.append(data)
                # Delete the file containing list of missing painted images
                os.remove(os.path.join(imagePath, "missing.txt"))

            # Add non-painted style variants to queue
            if not no_styles: #Mind the grammar
                dlQueue.append("UNPAINTED")

            # Download them if possible
            for paint in dlQueue:
                # Find the url from the painted page
                print(item["item_name"]) # .encode('utf-8').replace(" ", "_")
                if paint == "UNPAINTED":
                    url = "http://wiki.teamfortress.com/wiki/File:RED_" + item["item_name"].replace(" ", "_") + "_" + styleName + ".png"
                else:
                    url = "http://wiki.teamfortress.com/wiki/File:Painted_" + item["item_name"].replace(" ", "_") + "_" + paint + ("_"*(styleName != "")) + styleName + ".png"
                url = url.replace("?", "_") # Dangersque, Too? Fix

                try:
                    page = urllib.request.urlopen(url).read().decode("utf-8")
                except:
                    print("Could not read", url)
                    continue

                start = page.find('fullImageLink" id="file"><a href="')+34
                page = page[start:]
                end = page.find('.png')
                page = page[:end]
                #print start, end, page

                # Download the image
                url = "http://wiki.teamfortress.com" + page
                try:
                    urllib.request.urlretrieve(url, os.path.join(imagePath, paint + style + ".png"))
                    image = Image.open(os.path.join(imagePath, paint + style + ".png"))
                    placeholder = False
                except:
                    #print "File Not Found. Using a placeholder instead:" + paint + style + ".png"
                    image = Image.open(os.path.join(imagePath + ".png"))
                    placeholder = True

                # Resize the image (only for good images, not placeholders)
                if not placeholder:
                    image.thumbnail((85, 85), Image.ANTIALIAS)
                    width = image.size[0]
                    height = image.size[1]

                    painted = Image.new("RGBA", (128,128))
                    painted.paste(image, ((128-width) // 2, (128-height) // 2))
                else: # Mark placeholders
                    painted = Image.new("RGBA", (128,128))
                    painted.paste(image, (0,0))
                    textimg = ImageDraw.Draw(painted)
                    textimg.text((2, 118), "#"+paint, font=font, fill=(255,215,0))
                    missing.append(paint)
                    missing_count += 1

                try:
                    if not placeholder or (placeholder and not os.path.isfile(os.path.join(imagePath, paint + style + ".png"))):
                        painted.save(os.path.join(imagePath, paint + style + ".png"))
                        saved_count += 1
                        #print "Downloaded " + os.path.join(imagePath, paint + style + ".png")
                except:
                    output += "WARNING: Couldn't save image " + os.path.join(imagePath, paint + style + ".png" + "\n")
                    warnings += 1

            # Try to download a non-painted style??

            # Write any missing paints
            if missing:
                later = open(os.path.join(imagePath, "missing.txt"), "w")
                for m in missing:
                    later.write(m + "\n")
                later.close()

    output += "Downloaded "+ str(saved_count) + " painted images.\n"
    output += "Missing " + str(missing_count) + " painted images.\n"

    ################################################################################
    output += "============================================================\n"
    output += "VII. Compress PNGs\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " VII. Compress PNGs")
    image_count = 0
    for dir, subdirs, files in os.walk(IMAGE_ROOT):
        break  # DEBUG
        for file in files:
            if file.lower()[-4:] == ".png":
                path = os.path.join(dir,file)
                modified = datetime.fromtimestamp(os.path.getmtime(path))

                if (modified >= start_time):
                    os.system("pngcrush -brute \""+path+"\" "+IMAGE_ROOT+"temp.png > /dev/null")
                    os.system("mv -f "+IMAGE_ROOT+"temp.png " + path)
                    image_count += 1
    output += "Crushed " + str(image_count) + " files.\n"
    ################################################################################
    output += "============================================================\n"
    output += "VIII. Update site database\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " VIII. Update site database")

    contract_dupes = range(15000,16000)
    for entry in schema["items"]:
        # Produce Item
        item = Item()

        # Standard values
        keys = ["defindex", "image_url", "image_url_large", "item_class", "item_name", "item_quality", "proper_name"]
        for key in keys:
            setattr(item, key, entry.get(key))

        # Name/Paint
        item.nameable = True if entry.get("capabilities", {}).get("nameable") else False
        item.paintable = True if entry.get("capabilities", {}).get("paintable") else False


        if (item.defindex < 35) or (item.defindex in contract_dupes):
            item.nameable = False

        if entry.get("item_slot"):
            if entry["item_slot"] in SLOT_OVERRIDE.keys():
                item.item_slot = SLOT_OVERRIDE[entry["item_slot"]]
            else:
                item.item_slot = entry["item_slot"]

        if entry.get("used_by_classes"):
            item.used_by_classes = ""
            for role in entry["used_by_classes"]:
                item.used_by_classes += CLASS_VALUES[role]
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

        # Styles
        if entry.get("styles"):
            num = 0
            for style_name in entry["styles"]:
                style, created = Style.objects.get_or_create(defindex=item, style_num=num)
                style.name = style_name.get("name", "Unknown Style").strip()
                num += 1
                style.save()


    ################################################################################

    output += "============================================================\n"
    output += "IX. Generate raw data HTML page\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " IX. Generate raw data HTML page")

    template = get_template("/var/projects/tf2tags/templates/raw.html")
    data = {}
    data["items"] = Item.objects.filter(defindex__gte=1, nameable=True).order_by("defindex")
    c = Context(data)
    raw_data_page = template.render(c)
    template = codecs.open("/var/projects/tf2tags/templates/data.html", "w", "utf-8")
    template.write(raw_data_page)
    template.close()
    output += "Wrote templates/data.html\n"

    finish(output, errors, warnings)
    return True

def finish(output, errors, warnings):
    output += "============================================================\n"
    output += "X. E-Mail Script Report\n".upper()
    output += "--------------------\n"
    print(str(datetime.now())[:19] + " X. E-Mail Script Report")

    print("ERRORS", errors)
    print("WARNINGS", warnings)
    end_time = str(datetime.now())[:19]

    try:
        SERVER  = "localhost"
        FROM    = "TODO@tf2tags.com"
        TO      = ["TODO"]
        SUBJ    = "tf2tags update - Warnings "+str(warnings)+", Errors " + str(errors)
        TEXT    = output.replace("{{end}}", end_time)

        message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM, ", ".join(TO), SUBJ, TEXT)

        #print message
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, TO, message)
        server.quit()
        print("tf2tags has been updated. Mail has been sent")
    except:
        print("tf2tags has been updated. Mail has NOT been sent. Output is being dumped to update_tf2tags_nomail.log")


    file = codecs.open("/var/projects/tf2tags/tools/update_tf2tags_nomail.log", "w", "utf-8")
    file.write(SUBJ + "\n" + TEXT)
    file.close()
    exit()

if __name__ == "__main__":main()
