from django.db import models
from datetime import datetime
import random

class Users(models.Model):
    steamID     = models.CharField(max_length=20)
    name        = models.CharField(max_length=32)
    profile     = models.CharField(max_length=200)
    avatar      = models.CharField(max_length=200)
    submitted   = models.IntegerField(default=0)
    maxSubmitted= models.IntegerField(default=5)
    posted_comments = models.IntegerField(default=0)
    max_posted_comments = models.IntegerField(default=10)
    timestamp   = models.DateTimeField(auto_now_add=True)
    session     = models.CharField(max_length=100)

    def __unicode__(self):
        return "USER: " + self.steamID + " " + self.name

class Submissions(models.Model):
    set         = models.CharField(max_length=50, default=0)
    defindex    = models.CharField(max_length=5, db_index=True)
    role        = models.CharField(max_length=8, db_index=True)
    slot        = models.CharField(max_length=9, db_index=True)
    base        = models.CharField(max_length=200, db_index=True)
    name        = models.CharField(max_length=200, db_index=True)
    desc        = models.CharField("description", max_length=200, default="", db_index=True)
    prefix      = models.CharField(max_length=50, default="")
    filter      = models.CharField(max_length=50, default="")
    color       = models.CharField(max_length=6, default="FFD700")
    paint       = models.CharField(max_length=6, default="")
    particles   = models.CharField(max_length=50, default="")
    style       = models.IntegerField(default=0)
    keywords    = models.CharField(max_length=500, default="", db_index=True)
    user        = models.ForeignKey(Users, on_delete=models.SET_DEFAULT, default=1) #Requires a user row with steamID 0 to function
    ip          = models.GenericIPAddressField(default="")
    upVotes     = models.IntegerField(default=0) #These should both be positive
    downVotes   = models.IntegerField(default=0)
    score       = models.IntegerField(default=0, db_index=True)
    comments    = models.IntegerField(default=0)
    timestamp   = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        x = "===== SUBMISSION =====" + "\n"
        x += "Set         = " + self.set + "\n"
        x += "Defindex    = " + str(self.defindex) + "\n"
        x += "Role        = " + self.role + "\n"
        x += "Slot        = " + self.slot + "\n"
        x += "Base        = " + self.base + "\n"
        x += "Name        = " + self.name + "\n"
        x += "Desc        = " + self.desc + "\n"
        x += "Prefix      = " + self.prefix + "\n"
        x += "Filter      = " + self.filter + "\n"
        x += "Color       = " + self.color + "\n"
        x += "Paint       = " + self.paint + "\n"
        x += "Particles   = " + self.particles + "\n"
        x += "Style       = " + str(self.style) + "\n"
        x += "Keywords    = " + self.keywords + "\n"
        x += "User        = " + "NOT CODED" + "\n"
        x += "IP          = " + self.ip + "\n"
        x += "upVotes     = " + str(self.upVotes) + "\n"
        x += "downVotes   = " + str(self.downVotes) + "\n"
        x += "score       = " + str(self.score) + "\n"
        x += "comments    = " + str(self.comments) + "\n"
        x += "timestamp   = " + "- TBD -\n"
        x += "======================\n"
        return x


    def display_name(self):
        if self.name == self.base:
            # Quality/Filter
            if self.prefix or self.filter:
                return (self.prefix + " " + self.filter).strip() + " " + self.base
            else:
                return self.base
        else:
            return '"' + self.name + '"'

    def display_desc(self):
        if self.desc:
            return '"' + self.desc + '"'
        else:
            return ""

    def display_particles(self):
        if self.particles and self.particles != "None":
            return "Effect: " + self.particles
        else:
            return ""

    def prepare(self, prevDate="1970-01-01"):
        self.getKtD()
        self.getFakeAuthor()
        self.getIdentifier()
        self.getImage()
        #self.dateCheck(prevDate)
        self.paint_name = ""
        #return self.timestamp[:10]
        return True

    def getKtD(self):
        ktd = 1.0 * self.upVotes / max(self.downVotes, 1)

        if (ktd >= 1) or (self.downVotes == 0):
            color = "00FF00"
        else:
            color = "FF0000"

        ktd = '{0:.2f}'.format(ktd)
        while ktd[-1] == "0":
            ktd = ktd[:-1]
        if ktd[-1] == ".":
            ktd = ktd[:-1]

        self.ktd = ktd
        self.ktdColor = color
        return True

    def getFakeAuthor(self):
        self.fakeAuthor = ['Saxton Hale', 'Redmond Mann', 'Blutarch Mann', 'Silas Mann', 'The Administrator', 'Miss Pauling', 'Mrs. DeGroot', 'Radigan Conagher', 'Archimedes', 'Charles Darling', 'Balloonicorn', 'Robro 3000', 'Koala Compact', 'Pocket Purrer', 'Teddy Roosebelt', 'Alien Swarm Parasite', 'Triboniophorus Tyrannus', 'Grey Mann', 'Scout\'s Mom', 'Bird-Man of Aberdeen'][self.id % 20]
        return True

    def getIdentifier(self):
        if self.set == "0":
            self.identifier = "Item #" + str(self.id)
        else:
            self.identifier = self.name

    def getImage(self):
        self.image = self.defindex
        if self.paint != "":
            self.image += "/" + self.paint
        if self.style > 0:
            self.image += "-" + str(self.style)
        return True

    """
    def dateCheck(self, prevDate):
        # Checks if this item was posted on the same day as the last one
        self.showDate = (str(self.timestamp)[:10] != prevDate)

        if len(str(self.timestamp)) < 19:
            if len(str(self.timestamp)) == 10:
                self.timestamp = str(self.timestamp) + " 12:00:00"
            else:
                self.timestamp = "2011-04-01 12:00:00"
        else:
            self.timestamp = str(self.timestamp)

        self.timestamp = str(self.timestamp[:19])
        self.datetime = datetime.strptime(str(self.timestamp), "%Y-%m-%d %H:%M:%S")
        return True
    """

    def save(self, *args, **kwargs):
        # Pre save
        self.upVotes = abs(self.upVotes)
        self.downVotes = abs(self.downVotes)
        self.score = self.upVotes - self.downVotes

        # Actual save call
        super(Submissions, self).save(*args, **kwargs)

class Bans(models.Model):
    ip      = models.GenericIPAddressField()
    steamID = models.CharField(max_length=20)
    notes   = models.CharField(max_length=150)
    begins  = models.DateTimeField("Ban Start", auto_now_add=True)
    ends    = models.DateTimeField("Ban End")

    def __unicode__(self):
        return "BAN INFO:\n", "IP:", self.ip, "steamID:", self.steamID, "notes:", self.notes, "begins:", self.begins, "ends", self.ends

class Comments(models.Model):
    itemID      = models.IntegerField(db_index=True)
    #steamID     = models.CharField(max_length=20)
    user        = models.ForeignKey(Users, on_delete=models.CASCADE)
    ip          = models.GenericIPAddressField()
    comment     = models.CharField(max_length=500)
    timestamp   = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return "COMMENT INFO:\n", "itemID:", self.itemID, "steamID:", self.steamID, "ip:", self.ip, "comment", self.comment, "time:", self.time

class Flagged(models.Model):
    itemID      = models.IntegerField()
    type        = models.CharField(max_length=20) #This is the type as in "junk", "duplicate", etc. NOT item/set
    explanation = models.CharField(max_length=500)
    handled     = models.CharField(max_length=100)
    ip          = models.GenericIPAddressField()
    steamID     = models.CharField(max_length=20)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "FLAGGED: \n"


class News(models.Model):
    title       = models.CharField(max_length=50)
    author      = models.CharField(max_length=50, default="TODO")
    profile     = models.CharField(max_length=50, default="id/TODO")
    image       = models.CharField(max_length=50)
    text        = models.CharField(max_length=8000)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "NEWS: " + str(self.title)

class Votes(models.Model):
    itemID      = models.IntegerField()
    ip          = models.GenericIPAddressField()
    vote        = models.IntegerField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey(Users, null=True, blank=True, default=0, on_delete=models.SET_NULL) # Requires a user row with steamID 0 to function

    def __unicode__(self):
        return "VOTE: "

    def public(self):
        random.seed(self.ip + "X3BH42WURND4SLXDGT40WLHE8T76995WVM78XCO8XR1O24WLPFXOY3PJVTC2RBDJIH4P1Y46126H4N9JCYP0Z0YAJMQVOOC3MDNK")
        key = ""
        for x in range(0,12):
            key += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
        key = key[:4] + "-" + key[4:8] + "-" + key[8:]
        return key

class Contest(models.Model):
    theme       = models.CharField(max_length=50)
    startDate   = models.DateField()
    endDate     = models.DateField()
    winner      = models.IntegerField(default=0)
