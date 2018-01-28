# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys, os, glob, shutil

sys.path.append("/var/projects/tf2tags/")

try:
    import django
    None
except:
    sys.path.append("/var/projects/tf2tags/virt/lib/python2.7/site-packages")
    import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
django.setup()

from schema.models import *

from PIL import Image

def main():
    print "April Fool's Week Item Parser"
    ROOT = "/var/projects/tf2tags/tools/april/"
    ITEM_ROOT = "/var/projects/tf2tags/assets/items/"

    defindex = None

    for root, dirs, files in os.walk(ROOT):
        #print root, dirs, files

        for file in files:
            file_path = os.path.join(root, file)
            item_name = file[:-4]
            item_slot = root[len(ROOT):]

            # Check if the item exists already
            exists = len(Item.objects.filter(item_slot=item_slot, item_name=item_name, defindex__lt=0))
            if exists:
                print item_slot + "\t\t" + item_name + "\t\t" + "ALREADY IN DATABASE"
            else:
                print item_slot + "\t\t" + item_name + "\t\t" + "PARSING..."

                # Load the image
                wip = Image.open(file_path)

                # Make sure it's square
                src_width, src_height = wip.size
                print "  Width/Height", src_width, src_height

                if src_width != src_height:
                    print "  Resizing canvas"
                    anchor = "C"
                    w = max(src_width, src_height)
                    h = max(src_width, src_height)

                    anchors = {"NW":(0,0), "N":((w - src_width) / 2,0), "NE":((w - src_width),0),
                        "W":(0,(h - src_height) / 2), "C":((w - src_width) / 2,(h - src_height) / 2), "E":(w - src_width, (h - src_height) / 2),
                        "SW":(0,(h - src_height)), "S":((w - src_width) / 2,(h - src_height)), "SE":((w - src_width),(h - src_height))}

                    out = Image.new("RGBA", (w, h), (0,0,0,0))
                    x, y = anchors[anchor]
                    out.paste(wip, (x,y))
                    wip = out

                    print "  Image is now square"

                # Resize to 128x128
                if src_width != 128 or src_height != 128:
                    if item_slot in ["a_doom"]: # Nearest Neighbor
                        wip = wip.resize((128,128), Image.NEAREST)
                    else:
                        wip = wip.resize((128,128), Image.BICUBIC)

                    print  "  Image is now 128x128"

                    # Save
                    wip.save(file_path)
                    print "  Image saved."

                print "  Adding database entry"

                if defindex == None:
                    # Get the defindex to use for a new entry (minimum currently used - 1)
                    item = Item.objects.all().order_by("defindex")[0]
                    defindex = item.defindex

                defindex = defindex - 1
                item = Item(defindex=defindex)
                item.defindex = defindex
                item.image_url = "/assets/items/"+str(defindex)+".png"
                item.image_url_large = item.image_url
                item.item_name = item_name
                item.item_slot = item_slot
                item.used_by_classes = "A"
                item.nameable = True
                item.paintable = False
                item.save()

                rarity = Rarity()
                rarity.defindex    = item
                rarity.collectors  = True
                rarity.community   = True
                rarity.completed   = True
                rarity.customized  = True
                rarity.genuine     = True
                rarity.haunted     = True
                rarity.normal      = True
                rarity.rarity2     = True
                rarity.rarity3     = True
                rarity.self_made   = True
                rarity.strange     = True
                rarity.unique      = True
                rarity.unusual     = True
                rarity.valve       = True
                rarity.vintage     = True
                rarity.save()

                print "  Item saved as defindex " + str(item.defindex)
                output_path = os.path.join(ITEM_ROOT, str(item.defindex)+".png")
                shutil.copy2(file_path, output_path)
                print "  Image moved."


    return True

if __name__ == "__main__":main()
