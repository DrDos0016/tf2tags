#!/usr/bin/python
from __future__ import unicode_literals
import json, os, sys
sys.path.append("/var/projects/tf2tags.com")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
from schema.models import *
from datetime import datetime
from wikitools import wiki, page

SKIP_STARTS = ["etf2l", "esl", "strange_filter", "strange_part", "map_stamp", "your_account", "class_token", "chemistry_set", "congratulations!", "owl_10", "highlander", "noise_maker", "what's",
                "halloween", "mann_co._supply", "slot_token", "taunt:", "pile_o", "naughty_winter", "nice_winter", "dr._grord", "esh"]
SKIP_HAS    = ["bundle", "promo"]

def main():
    site = wiki.Wiki("http://wiki.teamfortress.com/w/api.php")
    items = Item.objects.filter(defindex__gte=35)
    
    changes = []
    
    for item in items:
        wiki_name = item.item_name.replace(" ", "_").lower()
        enabled = []
        
        # Check skips
        
        # Check botkillers
        if "botkiller" in wiki_name and not item.rarity.strange:
            item.rarity.strange = True
            item.rarity.save()
            changes.append("Enabled strange rarity for " + item.item_name)
        
        try:
            data = page.Page(site, "Template:Dictionary/quad/"+wiki_name)
            text = data.getWikiText()
            #print len(text), datetime.now(), item.item_name
            
            # Unique is special since it's enabled by default
            if "unique" not in text and item.rarity.unique:
                item.rarity.unique = False
                enabled.append("unique")
            
            wiki_rarities = ["unique", "vintage", "genuine", "strange", "unusual", "haunted", "collectors"]
            for rarity in wiki_rarities:
                if rarity in text and getattr(item.rarity, rarity) == False:
                    setattr(item.rarity, rarity, True)
                    enabled.append(rarity)
                    
            # Community
            # Self-Made
            
            # Apply changes
            if len(enabled) != 0:
                item.rarity.save()
                changed = "Enabled " + ", ".join(enabled) + " rarity for " + item.item_name
                changes.append(changed)
                print changed
            
            
        except:
            try:
                print "NO PAGE FOR", wiki_name
            except:
                print "NO PAGE FOR", item.defindex
            
    #print changes
    return
if __name__ == "__main__":main()

