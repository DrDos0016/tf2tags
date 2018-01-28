from .common import *
from .other import *
from datetime import datetime, timedelta
from schema.models import *
from tf2tags.tf2 import APRIL

#AJAX Related
def getAttributes(request, defindex=None):
    #return HttpResponse('getAttributes ' + str(tf2.SCHEMA["items"]));
    #data = {"attributes":tf2.SCHEMA["attributes"].sort(key=tf2.SCHEMA["attributes"]["name"])}
    ordered = sorted(tf2.SCHEMA["attributes"], key=lambda attrib: attrib["name"].lower())
    data = {"attributes":ordered}
    return render(request, "ajax/attributes.html", data)
    #return HttpResponse(item, content_type="application/json")

def getItems(request):
    role = tf.classdict.get(request.GET.get("role"), "All")
    slot = request.GET.get("slot", "misc")

    # Check for baked data ?
    results = []

    qs = Item.objects.filter(item_slot=slot, used_by_classes__contains=role, nameable=True).order_by("item_name")

    # APRIL FOOL'S DAY
    if APRIL:
        if slot == "a_tf2":
            qs = Item.objects.filter(Q(item_slot=None) | Q(item_slot=slot, used_by_classes__contains=role)).order_by("item_name")
        else:
            qs = Item.objects.filter(item_slot=slot, used_by_classes__contains=role).order_by("item_name")
    # END APRIL

    last_item_name = ""
    for item in qs:
        data = {}
        data["defindex"]    = item.defindex
        data["item_name"]   = ("The " * item.proper_name)+ item.item_name
        data["image"]       = item.image_url

        # Remove primary shotgun for non-engineer
        if item.item_name in ["Shotgun", "Panic Attack", "Festive Shotgun"] and item.item_slot == "primary" and role != "6":
            continue

        # Erase duplicates
        if item.item_name == last_item_name:
            continue

        results.append(data)
        last_item_name = item.item_name

    # Add secondary shotgun for soldier/pyro/heavy
    if len(qs) and item.item_slot == "secondary" and role in ["2","3","5"]:
        # I am not sure why the Shotgun is no longer needed on dev, but here we are.
        results.append({"defindex":199, "item_name":"Shotgun", "image":"http://media.steampowered.com/apps/440/icons/w_shotgun.1d9c8ea9d8b2b14b331ae22427c5e624f6d5d60c.png"})
        results.append({"defindex":1141, "item_name":"Festive Shotgun", "image":"http://media.steampowered.com/apps/440/icons/c_shotgun_xmas.17d9e510d01f54fac9c0c86407426ece748045a6.png"})
        results.append({"defindex":1153, "item_name":"The Panic Attack", "image":"http://media.steampowered.com/apps/440/icons/c_trenchgun.e5628dd3a7d93a8a9ce6bda057a1e68b79d139c5.png"})

    results = sorted(results, key=lambda itemsort: itemsort["item_name"] if not itemsort["item_name"].startswith("The ") else itemsort["item_name"][4:])
    results = json.dumps(results)
    return HttpResponse(results, content_type="application/json")

def getItem(request, defindex=None):
    # APRIL FOOL'S DAY
    if APRIL:
        item = Item.objects.get(pk=int(defindex))
        data = {}
        data["defindex"]    = item.defindex
        data["rarities"] = sorted(set(tf.rarities))
        if int(defindex) < 0:
            data["paintable"]   = False
        else:
            data["paintable"]   = item.paintable
        data["style"]       = []
        styles = Style.objects.filter(defindex_id=item.defindex)
        if styles:
            for style in styles:
                data["style"].append(style.name)
        results = json.dumps(data)
        return HttpResponse(results, content_type="application/json")
    # END APRIL

    item = Item.objects.get(pk=int(defindex), nameable=True)
    data = {}
    data["defindex"]    = item.defindex
    data["rarities"]    = item.rarity.all()
    data["paintable"]   = item.paintable
    data["style"]       = []
    styles = Style.objects.filter(defindex_id=item.defindex)
    if styles:
        for style in styles:
            data["style"].append(style.name)
    results = json.dumps(data)

    return HttpResponse(results, content_type="application/json")

def verify(request):
    #try:
    data = urllib.parse.unquote(request.POST.get("json"))
    data = json.loads(data)
    style = data["style"]
    if style == "":
        style = 0
    item = Submissions(defindex=data["defindex"], role=data["role"], slot=data["slot"], base=data["base"], name=data["name"], desc=data["desc"], prefix=data["prefix"], filter=data["filter"], color=data["color"], paint=data["paint"], particles=data["particles"], style=style, user_id=0)

    result = tf.validate(item)
    #except:
    #    return HttpResponse("General Verification Failure! This item will likely not submit correctly.")
    return HttpResponse(str(result))

def vote(request, item=None, vote=None):
    ip = request.META["REMOTE_ADDR"]

    if not request.is_ajax():
        return HttpResponse("Vote Error");

    i = Submissions.objects.filter(pk=item)[0]

    #Force vote to be 1/-1
    vote = int(vote)
    if (vote >= 0):
        vote = 1
    else:
        vote = -1

    # Force vote to be an upvote. Thanks tf2tags community.
    #vote = 1

    # Ignore votes for years prior to the item's creation
    year_created = i.timestamp.year
    vote_start = {2011:1, 2012:34720, 2013:169141, 2014:463673, 2015:764897, 2016:1162720}.get(year_created, 1162720)
    v = Votes.objects.filter(id__gte=vote_start, itemID=item, ip=ip)

    user = getUser(request.COOKIES.get("session", None))
    if user.get("steamID", "0") == "0":
        today = str(datetime.now())[:10] + " 00:00:00"
        count = len(Votes.objects.filter(ip=ip, timestamp__gte=today))

        if count > 5:
            return HttpResponse("Sign-in to vote!")

    if banned(user["steamID"], request):
        return HttpResponse("Not while banned!")

    # Spy checking mode
    """
    if user == None:
        return HttpResponse("Sign-in to vote!") # DEBUG
    elif str(user["steamID"]) == "0":
        return HttpResponse("Sign-in to vote!") # DEBUG
    """

    try:
        with open("/var/projects/tf2tags/votes.log", "a") as votelog:
            if user == None:
                votelog.write("Vote by non logged in user Item #"+str(item)+" IP: "+str(ip)+" Vote " + str(vote) + " TIME: " + str(datetime.now()) + "\n")
            else:
                votelog.write("Vote by STEAMID: "+str(user["steamID"])+" Item #"+str(item)+" IP: "+str(ip)+" Vote " + str(vote) + " TIME: " + str(datetime.now()) + "\n")
    except:
        None

    if len(v) == 0: #New Vote
        #Add the vote
        if user:
            v = Votes(itemID=item, ip=ip, vote=vote, user_id=user["id"])
        else:
            v = Votes(itemID=item, ip=ip, vote=vote, user_id=0)
        v.save()

        #Update the score
        if vote == 1:
            i.upVotes += 1
        else:
            i.downVotes += 1
        i.score += vote
        i.save()

    else: #Old Vote
        old_vote = v[0]

        # Check if the vote changed
        if old_vote.vote != vote:
            old_vote.vote = vote

            # Update the vote counts
            if vote == 1:
                i.upVotes += 1
                i.downVotes -= 1
            else:
                i.upVotes -= 1
                i.downVotes += 1

            old_vote.timestamp = datetime.now()
            old_vote.save()

            # Update the score
            i.score += (vote * 2) # Because you're undoing the old vote, then performing the opposite of the old vote it's like voting a certain way twice
            i.save()
            return HttpResponse("Item Rated!");
        else:
            return HttpResponse("Already Rated!")
    return HttpResponse("Item Rated!");
