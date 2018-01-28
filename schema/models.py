from django.db import models
#import jsonfield

"""
class Capability(models.Model):
    defindex                = models.IntegerField(primary_key=True, db_column="defindex_id")
    can_be_restored         = models.BooleanField(default=False)
    can_card_upgrade        = models.BooleanField(default=False)
    can_collect             = models.BooleanField(default=False)
    can_consume             = models.BooleanField(default=False)
    can_craft_count         = models.BooleanField(default=False)
    can_craft_if_purchased  = models.BooleanField(default=False)
    can_craft_mark          = models.BooleanField(default=False)
    can_customize_texture   = models.BooleanField(default=False)
    can_gift_wrap           = models.BooleanField(default=False)
    can_killstreakify       = models.BooleanField(default=False)
    can_spell_page          = models.BooleanField(default=False)
    can_strangify           = models.BooleanField(default=False)
    decodable               = models.BooleanField(default=False)
    nameable                = models.BooleanField(default=False)
    paintable               = models.BooleanField(default=False)
    strange_parts           = models.BooleanField(default=False)
    usable                  = models.BooleanField(default=False)
    usable_gc               = models.BooleanField(default=False)
    usable_out_of_game      = models.BooleanField(default=False)

    def __unicode__(self):
        out = ""
        if self.can_be_restored:
            out += "\tRestorable\n"
        if self.can_card_upgrade:
            out += "\tCard Upgradable\n"
        if self.can_collect:
            out += "\tCollectible\n"
        if self.can_consume:
            out += "\tConsumeable\n"
        if self.can_craft_count:
            out += "\tCraft Countable\n"
        if self.can_craft_if_purchased:
            out += "\tCraftable if Purchased\n"
        if self.can_craft_mark:
            out += "\tCraft Markable\n"
        if self.can_customize_texture:
            out += "\tCustomizable Texture\n"
        if self.can_gift_wrap:
            out += "\tGiftable\n"
        if self.can_killstreakify:
            out += "\tKillstreakable\n"
        if self.can_spell_page:
            out += "\tSpell Pageable\n"
        if self.can_strangify:
            out += "\tStrangifiable\n"
        if self.decodable:
            out += "\tDecodable\n"
        if self.nameable:
            out += "\tNameable\n"
        if self.paintable:
            out += "\tPaintable\n"
        if self.strange_parts:
            out += "\tStrange Partsable\n"
        if self.usable:
            out += "\tUsable\n"
        if self.usable_gc:
            out += "\tUsable GC\n"
        if self.usable_out_of_game:
            out += "\tUsable out of game\n"
        return out

"""

class Item(models.Model):
    defindex                = models.IntegerField(primary_key=True)
    image_url               = models.CharField(max_length=150, null=True)
    image_url_large         = models.CharField(max_length=150, null=True)
    item_class              = models.CharField(max_length=50, null=True)
    item_name               = models.CharField(max_length=200, null=True)
    item_quality            = models.IntegerField(default=6)
    item_slot               = models.CharField(max_length=10, null=True, db_index=True)
    per_class_loadout_slots = models.CharField(null=True, max_length=10)
    proper_name             = models.BooleanField(default=False)
    used_by_classes         = models.CharField(max_length=10, db_index=True)
    nameable                = models.BooleanField(default=False, db_index=True)
    paintable               = models.BooleanField(default=False, db_index=True)
    #style                   = models.ForeignKey("Style", null=True)

    def __unicode__(self):
        out = ""
        out += "DEFINDEX      : " + str(self.defindex) + "\n"
        out += "ITEM_NAME     : " + str(self.item_name) + "\n"
        out += "NAMEABLE      : " + str(self.nameable) + "\n"
        out += "PAINTABLE     : " + str(self.paintable) + "\n"
        out += "USED BY       : " + str(self.decode_classes()) + "\n"
        out += "RARITIES      : " + str(self.rarity.all()) + "\n"
        return out

    def decode_classes(self):
        out = []
        classes = {"0":"All", "1":"Scout", "2":"Soldier", "3":"Pyro", "4":"Demoman", "5":"Heavy", "6":"Engineer", "7":"Medic", "8":"Sniper", "9":"Spy"}
        for num in str(self.used_by_classes):
            out.append(classes.get("num"))
        return out

class Rarity(models.Model):
    defindex    = models.OneToOneField("Item", primary_key=True, on_delete=models.CASCADE)
    collectors  = models.BooleanField(default=False)
    community   = models.BooleanField(default=False)
    completed   = models.BooleanField(default=False)
    customized  = models.BooleanField(default=False)
    genuine     = models.BooleanField(default=False)
    haunted     = models.BooleanField(default=False)
    normal      = models.BooleanField(default=False)
    rarity2     = models.BooleanField(default=False)
    rarity3     = models.BooleanField(default=False)
    self_made   = models.BooleanField(default=False)
    strange     = models.BooleanField(default=False)
    unique      = models.BooleanField(default=True)
    unusual     = models.BooleanField(default=False)
    valve       = models.BooleanField(default=True)
    vintage     = models.BooleanField(default=False)

    # Decorated
    """
    civilian    = models.BooleanField(default=False)
    freelance   = models.BooleanField(default=False)
    mercenary   = models.BooleanField(default=False)
    commando    = models.BooleanField(default=False)
    assassin    = models.BooleanField(default=False)
    elite       = models.BooleanField(default=False)
    """

    # This may or may not need decorated rarities added?
    def all(self):
        output = []
        attrs = ["normal", "unique", "vintage", "genuine", "strange", "unusual", "haunted", "collectors", "community",
                "self_made", "valve", "completed", "customized", "rarity2", "rarity3"]
        attr_names = {"normal":"Normal", "unique":"Unique", "vintage":"Vintage", "genuine":"Genuine", "strange":"Strange",
                "unusual":"Unusual", "haunted":"Haunted", "collectors":"Collector's", "community":"Community", "self_made":"Self-Made",
                "valve":"Valve", "completed":"Completed", "customized":"Customized", "rarity2":"Rarity2", "rarity3":"Rarity3"}
        for attr in attrs:
            if getattr(self, attr) == True:
                output.append(attr_names[attr])
        return output

class Style(models.Model):
    defindex    = models.ForeignKey("Item", on_delete=models.CASCADE)
    style_num   = models.IntegerField(default=0)
    name        = models.CharField(max_length=40)
