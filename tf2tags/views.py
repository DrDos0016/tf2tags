# View Modules
from .common import *
from .ajax import *
from .admin import *
from .other import *

import smtplib

def awards(request):
    data = {}
    today = date.fromtimestamp(time.time())
    data["running_contest"] = False
    data["contest"] = Contest.objects.filter(startDate__lte=today, endDate__gte=today).order_by('-id')
    if data["contest"]:
        data["running_contest"] = True
        data["contest"] = data["contest"][0]
        data["time"] = str(data["contest"].endDate - today)
        if data["time"][0] == "-":
            data["time"] = "no time remaining"
        else:
            data["time"] = data["time"].split(",")[0]
    return render(request, "awards.html", data)

def browse(request, page=1):
    page = int(page)
    data = {"title":" - Browse Items"}
    data["cookie"] = request.COOKIES

    # Get news
    data["news"] = News.objects.all().order_by("-id")
    data["show_news"] = False

    # Fetch the latest news post and see if it needs to be displayed
    if data["news"]:
        data["news"] = data["news"][0]
        if str(data["news"].timestamp)[:10] > request.COOKIES.get("latest_news", "1970-01-01"):
            data["show_news"] = True


    #Get items
    data["type"] = "browse"
    data["items"] = loadItems(page, data["type"])
    data["itemCount"] = Submissions.objects.filter(Q(set="0") | Q(slot="set")).count()
    data["maxPage"] = int(math.ceil(data["itemCount"] / 10.0))

    #Navigation
    data["pageCurrent"] = page
    data["pageList"] = range(max(1, page-3), min(page+4, data["maxPage"]+1))
    return render(request, "browse.html", data)

def browseUser(request, steamID="0", page=1):
    page = int(page)
    data = {"title":" - User Items"}

    #Get items
    data["type"] = "browse-"+steamID
    data["items"] = loadItems(page, data["type"])

    data["itemCount"] = Submissions.objects.filter(Q(set="0") | Q(slot="set"), user__steamID=steamID).count()
    data["maxPage"] = int(math.ceil(data["itemCount"] / 10.0))

    #Navigation
    data["pageCurrent"] = page
    data["pageList"] = range(max(1, page-3), min(page+4, data["maxPage"]+1))

    return render(request, "browse.html", data)

def contest(request, theme, page=1):
    page = int(page)
    data = {"title":" - Contest Entries"}

    #Get items
    data["type"] = "contest/" + theme
    data["items"] = loadItems(page, data["type"])

    contest = Contest.objects.filter(theme=theme).order_by("-id")[0]
    data["itemCount"] = Submissions.objects.filter(Q(set="0") | Q(slot="set"), keywords__contains=theme, timestamp__gte=contest.startDate, timestamp__lte=contest.endDate).count()
    data["maxPage"] = int(math.ceil(data["itemCount"] / 10.0))

    #Navigation
    data["pageCurrent"] = page
    data["pageList"] = range(max(1, page-3), min(page+4, data["maxPage"]+1))

    return render(request, "browse.html", data)

def create(request):
    data = {'tf':tf}
    data["user"] = getUser(request.COOKIES.get("session", None))

    if data["user"]["steamID"] == "0":
        return redirect("/openid/login")

    if request.GET.get("debug"):
        data["debug"] = True

    # Check the user isn't banned
    if banned(data["user"]["steamID"], request):
        return redirect("/error/banned")

    # Check for Spycheck mode
    #if SPYCHECK and data["user"]["steamID"] == "0":
    #    return redirect("/error/spycheck")

    # Check the user can still submit items today
    if data["user"]["submitted"] == data["user"]["max_submitted"]:
        return redirect("/error/max_submissions")

    return render(request, "create.html", data)

def delete_comment(request):
    return HttpResponse("Delete", context_instance=RequestContext(request))

def error(request, type="unknown"):
    data = {"error":type}

    data["user"] = getUser(request.COOKIES.get("session", None))
    if type == "banned":
        data["ban"] = Bans.objects.filter(Q(ip=request.META["REMOTE_ADDR"]) | Q(steamID=data["user"]["steamID"])).order_by('-id')[0]

    return render(request, "error.html", data)

def generic(request, template, title=""):
    return render(request, template, {"title": title})

def images(request, item):
    data = {"title": " - Image Audit"}

    #data["item"] = tf.itemInfo(int(item))["item_name"]
    data["item"] = Item.objects.get(defindex=int(item)).item_name
    data["images"] = []
    images = glob.glob(ROOT + "assets/items/"+str(item)+"/*.png")
    for image in images:
        data["images"].append(image[25:])
    data["images"].sort()
    data["count"] = len(data["images"])

    #data["next"] =
    return render(request, "images.html", data)

def login(request):
    choices = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    shuffle(choices)
    nonce = (datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") + "".join(choices[:6]))
    post_params = "openid.return_to="+URL+"openid/complete/?janrain_nonce="+nonce
    post_params += "&openid.realm="+URL+"&openid.ns=http://specs.openid.net/auth/2.0&openid.sreg.optional=email,fullname,nickname"
    post_params += "&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.ns.sreg=http://openid.net/extensions/sreg/1.1"
    post_params += "&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.mode=checkid_setup"

    if not request.GET.get("janrain_nonce"):
        # Send request
        url = "https://steamcommunity.com/openid/login?"+(post_params)
        return redirect(url)
    else:
        # Check the response is valid
        new_params = request.GET.copy()
        new_params["openid.mode"] = "check_authentication"
        resp = urllib.request.urlopen("https://steamcommunity.com/openid/login"+"?"+new_params.urlencode())
        body = resp.read().decode("utf-8")
        if "is_valid:true" not in body:
            return redirect("/error/login")

    # Valid login
    data = {}
    data["response"] = request.GET["openid.claimed_id"]
    data["id"] = request.GET["openid.claimed_id"][36:]
    # Set your Steam API key here
    data["url"] = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=TODO&steamids="+data["id"]

    #Get public info
    try:
        data["info"] = json.loads(urllib.request.urlopen(data["url"]).read().decode("utf-8"))["response"]["players"][0]
    except:
        error_log = "==========\n"
        error_log += str(datetime.now()) + "\n"
        error_log += "ID: " + data["id"] + "\n"
        try:
            error_log += urllib.urlopen(data["url"]).read() + "\n"
        except:
            error_log + "Can't parse url " + data["url"] + "\n"

        output = open("/var/projects/tf2tags.com/assets/data/login_errors.log", "w")
        output.write(error_log)
        output.close()
        return redirect("/error/login")

    if not data["info"].get("profilestate"):
        return redirect("/error/login")

    #Get/Set User data
    user = Users.objects.filter(steamID=data["info"]["steamid"])

    #Prepare response page
    response = redirect("/")

    if len(user) == 0: #New User
        s = SessionStore()
        s.save()
        data["key"] = s.session_key
        user = Users(steamID=data["info"]["steamid"], name=data["info"]["personaname"], profile=data["info"]["profileurl"], avatar=data["info"]["avatar"], session=data["key"])
    else:
        s = SessionStore()
        s.save()
        user = user[0]
        data["key"] = user.session
        if data["key"] == "":
            data["key"] = s.session_key
            #Update user session in DB
            user = Users.objects.filter(steamID=data["info"]["steamid"])[0]
            user.session = data["key"]
            user.profile = data["info"]["profileurl"]
            user.avatar = data["info"]["avatar"]

    try:
        response.set_cookie('session', data["key"], max_age=(3600*24*30))
        user.save()
    except:
        return redirect("/error/login")


    return response

def logout(request):
    response = redirect("/")

    #Clear DB session
    user = Users.objects.filter(session=request.COOKIES.get("session", None))
    if user:
        user[0].session = ""
        user[0].save()

    #Clear cookie
    response.delete_cookie('session')
    response.delete_cookie('sessionid')
    return response

def newsArchive(request, id=None):
    data = {}
    if id == None:
        data["news"] = News.objects.all().order_by('-timestamp')
        return render(request, "newsArchive.html", data)
    elif id == "latest":
        data["news"] = News.objects.filter().order_by('-timestamp')[0]
        data["set_cookie"] = True
        return render(request, "newsPost.html", data)
    else:
        data["news"] = News.objects.get(pk=id)
        return render(request, "newsPost.html", data)

def modifyItem(request, item):
    data = {}
    data["user"] = getUser(request.COOKIES.get("session", None))
    # First confirm the item is the user's or the user is an admin

    itemID = item
    items = Submissions.objects.filter(pk=item)

    if items[0].set != "0":
        items = Submissions.objects.filter(set=items[0].set)

    if ((data["user"]["steamID"] != items[0].user.steamID) or (items[0].user.steamID == "0")):
        if not data["user"]["admin"]:
            return redirect("/")

    if request.POST.get("action"):
        if request.POST["action"] == "Confirm Deletion":
            set = request.POST["set_id"]

            if set == "0":
                tf2.deleteItem(request.POST["id"])
            else: # Delete the set
                items = Submissions.objects.filter(set=set)
                for item in items:
                    tf2.deleteItem(item.id)
            return redirect("/")
        else:
            item_ids = request.POST.getlist("item_id")
            items = Submissions.objects.filter(pk__in=item_ids)

            count = 0
            names = request.POST.getlist("name")
            descs = request.POST.getlist("desc")
            keywords = request.POST.get("keywords")

            for item in items:
                # See if the name has been changed
                if (item.name != names[count] or item.desc != descs[count]):
                    posted = datetime.strptime(str(item.timestamp)[:19], "%Y-%m-%d %H:%M:%S")
                    now = datetime.now()
                    days = (now - posted)

                    # Change fields
                    item.name = names[count]
                    item.desc = descs[count]

                    # If the item is a day old, delete votes/comments
                    if days.days >= 1:
                        item.upVotes = 0
                        item.downVotes = 0
                        item.score = 0
                        tf2.deleteVotes(itemID)

                item.keywords = keywords
                item.save()
                count += 1
            return redirect(viewItem, item=itemID)

    posted = datetime.strptime(str(items[0].timestamp)[:19], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    days = (now - posted)
    data["reset"] = (days.days >= 1)

    itemslist = []
    for item in items:
        item.prepare()
        itemslist.append(item)

    # Remove set head from
    if len(itemslist) > 1:
        itemslist = itemslist[:-1]

    data['items'] = itemslist
    data["count"] = len(data["items"])


    return render(request, "modifyItem.html", data)

def profile(request, steamID="0"):
    data = {}
    data["user"] = getUser(request.COOKIES.get("session", None))
    page = 1
    comment_list = 10 # Comments to show per page
    comment_page = int(request.GET.get("cpage", 1))
    data["next"] = comment_page + 1
    data["prev"] = max(comment_page - 1, 1)

    if request.POST.get("name") and steamID != "0":
        if len(request.POST["name"].strip()) > 0:
            you = Users.objects.get(steamID=steamID)
            you.name = request.POST["name"]
            you.save()

    data["stats"] = getProfile(steamID)
    data["you"] = False
    if (data["user"]["steamID"] == data["stats"]["steamID"]) and data["user"]["steamID"] != "0":
        data["you"] = True

    # Latest Comments
    if data["you"]:
        comment_ids = {}
        commented_on = Submissions.objects.filter(Q(set="0") | Q(slot="set"), user__steamID=data["stats"]["steamID"], comments__gte=1).order_by("-id")
        for submission in commented_on:
            if not comment_ids.get(submission.id):
                comment_ids[submission.id] = submission.name

        comments = Comments.objects.filter(itemID__in=comment_ids).order_by("-timestamp")[(comment_list*(comment_page-1)):(comment_list*(comment_page-1))+comment_list]
        parsed_comments = []
        parsed_ids = []
        for comment in comments:
            if True or comment.itemID not in parsed_ids:
                comment.name = comment_ids[comment.itemID]
                parsed_comments.append(comment)
                parsed_ids.append(comment.itemID)

        data["comments"] = parsed_comments

    # Submissions - Only the latest 10
    #data["submissions"] = Submissions.objects.filter(Q(set="0") | Q(slot="set"), user__steamID=data["stats"]["steamID"]).order_by("-id")[(10*(page-1)):(10*(page-1))+10]
    return render(request, "profile.html", data)

def random(request):
    data = {"title":" - Random Items"}

    #Get items
    data["type"] = "random"
    data["items"] = loadItems(1, data["type"])

    return render(request, "browse.html", data)

def results(request, page=1):
    data = {}

    page = int(page)
    results = Submissions.objects.all()
    if request.GET.get("class") and not request.GET.get("base"):
        results = results.filter(role=request.GET["class"])
    if request.GET.get("slot") and not request.GET.get("base"):
        results = results.filter(slot=request.GET["slot"])
    if request.GET.get("base"):
        results = results.filter(base=request.GET["base"])
    if request.GET.get("name"):
        results = results.filter(name__icontains=request.GET["name"])
    if request.GET.get("desc"):
        results = results.filter(desc__icontains=request.GET["desc"])
    if request.GET.get("start"):
        results = results.filter(timestamp__gte=request.GET["start"])
    if request.GET.get("end"):
        results = results.filter(timestamp__lte=request.GET["end"])
    if request.GET.get("keywords"):
        keywords = request.GET.get("keywords").lower().replace(", ", ",")
        results = results.filter(keywords__contains=keywords)

    if request.GET.get("rating"):
        results = results.filter(score__gte=request.GET["rating"])

    # Order
    if request.GET.get("order"):
        if request.GET["order"] in ("timestamp", "score"):
            descend = "-"
        else:
            descend = ""
        results = results.order_by(descend + request.GET["order"], "-id")

    # Page
    data["itemCount"] = results.count()
    results = results[(page-1)*10:(page-1)*10+10]
    for item in results:
        item.prepare()

    #Get items
    data["type"] = "results"
    data["items"] = results

    data["maxPage"] = int(math.ceil(data["itemCount"] / 10.0))

    #Navigation
    data["page"] = page
    data["pageCurrent"] = page
    data["pageList"] = range(max(1, page-2), min(page+7, data["maxPage"]+1))
    data["qs"] = "?" + request.META["QUERY_STRING"]

    return render(request, "browse.html", data)

def streak_search(request):
    """ This feature has been removed """
    return redirect("/")

    """
    start = datetime.now()
    data = {}
    data["post"] = request.POST
    if not request.POST.get("action"):
        data["results"] = []
        return render_to_response('streak_search.html', data, context_instance=RequestContext(request))

    market_data = json.loads(open("/var/projects/tf2tags.com/assets/data/streak_search.json").read())

    # Process results
    results = []
    data["meta"] = market_data["meta"]
    max_price = request.POST.get("max_price", 32767)
    if max_price == "":
        max_price = 32767
    max_price = float(max_price)
    if market_data["meta"]["success"] != 1:
        return render_to_response('streak_search.html', data, context_instance=RequestContext(request))

    for row in market_data["data"]:
        # General Filters
        if row["name"][:13] == "Strange Part:":
            continue
        if float(row["price"][1:]) > max_price:
            continue
        #else:
        #    print float(row["price"][1:]), max_price
        #    print float(row["price"][1:]) > float(max_price), " greater than max"

        # Item filters
        if not request.POST.get("show_specialized_fabricator") and "Specialized" == row["name"][:11] and " Kit Fabricator" in row["name"]:
            continue
        if not request.POST.get("show_professional_fabricator") and "Professional" == row["name"][:12] and " Kit Fabricator" in row["name"]:
            continue
        if not request.POST.get("show_killstreak_kit") and "Kit" == row["name"][-3:] and "Killstreak" == row["name"][:10]:
            continue
        if not request.POST.get("show_specialized_kit") and "Kit" == row["name"][-3:] and "Specialized Killstreak" == row["name"][:22]:
            continue
        if not request.POST.get("show_professional_kit") and "Kit" == row["name"][-3:] and "Professional Killstreak" == row["name"][:23]:
            continue
        if not request.POST.get("show_killstreak_item") and " Kit" not in row["name"] and " Fabricator" not in row["name"] and "Killstreak" in row["name"] and "Professional Killstreak" not in row["name"] and "Specialized Killstreak" not in row["name"]:
            continue
        if not request.POST.get("show_specialized_killstreak_item") and " Kit" not in row["name"] and " Fabricator" not in row["name"] and "Specialized Killstreak" in row["name"]:
            continue
        if not request.POST.get("show_professional_killstreak_item") and " Kit" not in row["name"] and " Fabricator" not in row["name"] and "Professional Killstreak" in row["name"]:
            continue

        # Rarity filters
        if not request.POST.get("show_unique") and "Vintage" not in row["name"] and "Genuine" not in row["name"] and "Strange" not in row["name"] and "Collector's" not in row["name"] and "Haunted" not in row["name"]:
            continue
        if not request.POST.get("show_vintage") and "Vintage" in row["name"]:
            continue
        if not request.POST.get("show_genuine") and "Genuine" in row["name"]:
            continue
        if not request.POST.get("show_strange") and "Strange" in row["name"]:
            continue
        if not request.POST.get("show_collectors") and "Collector's" in row["name"]:
            continue
        if not request.POST.get("show_haunted") and "Haunted" in row["name"]:
            continue
        results.append({"name":row["name"], "quantity":row["quantity"], "price":row["price"], "link":row["link"]})

    data["results"] = sorted(results, key=lambda results: float(results["price"][1:]))
    data["displaying"] = len(results)
    return render_to_response('streak_search.html', data, context_instance=RequestContext(request))
    """

def submitComment(request):
    user = getUser(request.COOKIES.get("session", None))
    data = {}
    data["user"] = user

    if user["steamID"] == 0:
        return redirect("/")

    # Check the user isn't banned
    if banned(user["steamID"], request):
        return redirect("/error/banned")

    if request.POST["comment"] == "":
        return redirect("/")

    # Check the user still has comments left for today
    if data["user"]["posted_comments"] >= data["user"]["max_posted_comments"]:
        return redirect("/error/max_submissions")

    # Get user and update submission count
    user_account = Users.objects.get(pk=data["user"]["id"])
    user_account.posted_comments += 1
    user_account.save()
    data["user"]["posted_comments"] += 1

    # This is "temporary"
    if "toggaf "[::-1] in request.POST["comment"].lower():
        return redirect("/")

    # Save comment
    comment = Comments(itemID=int(request.POST["item"]), user_id=user["id"], ip=request.META["REMOTE_ADDR"], comment=request.POST["comment"][:500])
    comment.save()

    # Update item's comments counter
    item = Submissions.objects.get(pk=int(request.POST["item"]))
    item.comments += 1
    item.save()

    return redirect("/view-"+request.POST["item"])

def submitItem(request):
    data = {}
    data["user"] = getUser(request.COOKIES.get("session", None))

    ip = request.META["REMOTE_ADDR"]

    # Check the user isn't banned
    if banned(data["user"]["steamID"], request):
        return redirect("/error/banned")

    # Check the user still has submissions left for today
    if data["user"]["steamID"] == "0":
        if SPYCHECK:
            return redirect("/") # Spy Checking mode
        today = date.fromtimestamp(time.time())
        submitted = Submissions.objects.filter(ip=ip, timestamp__gte=today).count()
        if submitted >= 3:
            return redirect("/error/max_submissions")
    elif data["user"]["submitted"] >= data["user"]["max_submitted"]:
        return redirect("/error/max_submissions")

    # Get user
    user_account = Users.objects.get(pk=data["user"]["id"])

    # Prepare Data
    items = []
    post = json.loads(request.POST["submission"])
    now = time.time()

    # Manage set info
    if len(post["items"]) > 1:
        item_set = True
        if post["meta"]["set_name"] == "":
            post["meta"]["set_name"] == "The Set With No Name"
        if post["meta"]["set_icon"] == "":
            post["meta"]["set_icon"] = "-10"
        set_id = str(now).replace(".","") + "-" + ip.replace(".", "")
    else:
        item_set = False
        set_id = "0"

    # Check for an item with the same name + desc + base if it's not a set.
    #print("POST IS ", post)
    if not item_set and duplicate_check(post["items"][0]["name"], post["items"][0]["desc"], post["items"][0]["base"]):
        return redirect("/error/duplicate")

    # Loop over each item in the submission
    for item in post["items"]:
        if item["style"] == "":
            item["style"] = 0
        if item["color"] == "":
            item["color"] = "FFD700"
        if item["prefix"] == "Unique":
            item["prefix"] = ""

        # Confirm no-paint yes-style image exists
        if (int(item["style"]) > 0) and (item["paint"] == ""):
            if not os.path.isfile("/var/projects/tf2tags.com/assets/items/"+str(item["defindex"])+"-"+str(item["style"])+".png"):
                item["style"] = 0

        item = Submissions(set=set_id, defindex=item["defindex"], role=item["role"], slot=item["slot"], base=item["base"], name=item["name"][:40], desc=item["desc"][:80], prefix=item["prefix"],
            filter=item["filter"], color=item["color"], paint=item["paint"], particles=item["particles"], style=item["style"], keywords=post["meta"]["keywords"].lower(), user=user_account, ip=ip)

        # Slur check
        words = item.name.split(" ") + item.desc.split(" ")

        for slur in SLURS:
            if slur.lower() in words:
                # Congrats, you're getting banned
                if data["user"]["steamID"] == "0": # Ban anon
                    ban = Bans(ip=ip, steamID="-", notes="Automatic ban for slurs.", begins=date.fromtimestamp(time.time()), ends=date.fromtimestamp(time.time() + 86400))
                else:
                    ban = Bans(ip=ip, steamID=data["user"]["steamID"], notes="Automatic ban for slurs.", begins=date.fromtimestamp(time.time()), ends=date.fromtimestamp(time.time() + 43200))
                ban.save()
                return redirect("/error/banned")

        # Validate or Break
        valid = tf.validate(item)
        if valid == "SUCCESS":
            items.append(item)
        else:
            data["failure"] = json.dumps(item)
            data["errors"] = valid
            return render_to_response('submissionError.html', data, context_instance=RequestContext(request))

    # Save items
    for item in items:
        item.save()
    outgoing_id = items[-1].id

    # Save set head
    if item_set:
        item = Submissions(set=set_id, defindex=post["meta"]["set_icon"], slot="set", base="Set Head", name=post["meta"]["set_name"][:40], desc="Contains "+str(len(post["items"]))+" Items", keywords=post["meta"]["keywords"].lower(), user=user_account, ip=ip)
        item.save()
        outgoing_id = item.id

    if (len(items) > 0):

        # Update submission count
        user_account.submitted += 1
        user_account.save()
        data["user"]["submitted"] += 1

        return redirect(viewItem, item=outgoing_id)

    return redirect("/")

def submitReport(request):
    user = getUser(request.COOKIES.get("session", None))

    # Save report
    report = Flagged(itemID=int(request.POST["item"]), type=request.POST["reason"], explanation=request.POST["explanation"], ip=request.META["REMOTE_ADDR"], steamID=user["steamID"])
    report.save()

    # Get item
    item = Submissions.objects.filter(pk=int(request.POST["item"]))
    if len(item) != 1:
        return redirect("/view-"+request.POST["item"])

    item = item[0]

    start_date = datetime.now()
    end_date = start_date
    # Email me about it!
    REPORT_MAIL = "An item has been reported on tf2tags.\n\nThe item in question can be found here: http://tf2tags.com/view-{}\n\nSUBMISSION INFORMATION:\nBase: {}\nName: {}\nDesc: {}\n\nIP: {}\nSteamID: {}\nAuthor: {}\n\n\nREPORT INFORMATION:\nItem #: {}\nReason: {}\nExplanation: {}\nIP: {}\nSteamID: {}\nSteam Name: {}\n\nBAN QUERY:\n\nINSERT INTO tf2tags_bans (ip, steamID, notes, begins, ends) VALUES ('{}', '{}', 'NOTES', '{}', '{}');"
    #SERVER  = "tf2tags.com"
    SERVER  = "localhost"
    FROM    = "TODO"
    TO      = ["TODO"]
    SUBJ    = "Item #"+request.POST["item"]+" - Reported for " + request.POST["reason"]
    TEXT    = REPORT_MAIL.format(item.id, item.base, item.name, item.desc, item.ip, item.user.steamID, "---", item.id, request.POST["reason"], request.POST["explanation"], request.META["REMOTE_ADDR"], user["steamID"], user["name"], item.ip, item.user.steamID, start_date, end_date)

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJ, TEXT)

        #print message
    try:
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, TO, message)
        server.quit()
    except:
        print("Could not send email")
        print(message)
        None

    return redirect("/view-"+request.POST["item"])

def summary(request):
    steam_id = request.GET.get("steam_id")
    profile = getProfile(steam_id)
    return HttpResponse(json.dumps(profile))


def topItems(request, days=0, page=1):
    page = int(page)
    data = {}

    #Get items
    data["type"] = "top/"+str(days)
    data["items"] = loadItems(page, data["type"])

    if days == 0:
        data["itemCount"] = Submissions.objects.filter(Q(set="0") | Q(slot="set")).count()
        data["type"] = "top"
    else:
        days = int(days)
        now = datetime.utcnow().replace(tzinfo=utc)

        timediff = now - timedelta(days=days)

        data["itemCount"] = Submissions.objects.filter(Q(set="0") | Q(slot="set"), timestamp__gte=(timediff)).count()
    data["maxPage"] = int(math.ceil(data["itemCount"] / 10.0))

    #Navigation
    data["pageCurrent"] = page
    data["pageList"] = range(max(1, page-2), min(page+7, data["maxPage"]+1))

    return render(request, "browse.html", data)

def viewItem(request, item=1):
    data = {"viewing":True}

    items = Submissions.objects.filter(pk=item)

    if len(items) < 1:
        return redirect("/browse")


    if items[0].set != "0":
        items = Submissions.objects.filter(set=items[0].set)
    itemslist = []
    for item in items:
        item.prepare()
        if item.paint != "":
            for x in range(0,len(tf.hex)):
                if item.paint == tf.hex[x]:
                    item.paint_name = tf.paints[x]
                    break

        if item.style != 0:
            data["style_name"] = Style.objects.filter(defindex_id=item.defindex, style_num=item.style)[0].name
        itemslist.append(item)

    data["identifier"] = "Item #"+str(items[len(items)-1].id)
    data["upVotes"] = items[len(items)-1].upVotes
    data["downVotes"] = items[len(items)-1].downVotes
    data["ktd"] = items[len(items)-1].ktd
    data["ktdColor"] = items[len(items)-1].ktdColor
    if items[0].set != "0":
        data["identifier"] = items[len(items)-1].name

    # Get comments
    if (itemslist[-1].comments > 0):
        data["comments"] = Comments.objects.filter(itemID=itemslist[-1].id).order_by("-id")
    else:
        data["comments"] = []

    data['items'] = itemslist
    data["count"] = len(data["items"])
    return render(request, "viewItem.html", data)

def votes_item(request, item):
    data = {}
    offset = int(request.GET.get("offset", 0))
    data["next"] = offset + 25
    data["prev"] = max(offset - 25, 0)

    votes = Votes.objects.filter(itemID=item).order_by("-timestamp")[offset:offset+25]
    data["votes"] = votes

    return render(request, "votes_item.html", data)

def votes_user(request, vote_id):
    data = {}
    offset = int(request.GET.get("offset", 0))
    data["next"] = offset + 25
    data["prev"] = max(offset - 25, 0)
    source = Votes.objects.get(id=vote_id)
    votes = Votes.objects.filter(ip=source.ip).order_by("-timestamp")[offset:offset+25]

    # Find the submission authors
    item_ids = []
    for vote in votes:
        item_ids.append(vote.itemID)

    items = Submissions.objects.filter(id__in=item_ids)

    for vote in votes:
        for item in items:
            if vote.itemID == item.id:
                vote.author = item.user.name
                break

    data["votes"] = votes
    data["voter_key"] = source.public()
    data["item"] = source.itemID
    return render(request, "votes_user.html", data)

def winners(request, year=2013):
    data = {}
    #contests = Contest.objects.filter(endDate__gte=str(year)+"-01-01", endDate__lte=str(year)+"-12-31")
    contests = Contest.objects.all().order_by("-id")
    winners = []
    themes = []
    for winner in contests:
        if winner.winner != 0:
            winners.append(winner.winner)
            themes.append(winner.theme)

    # Get winning items
    items = Submissions.objects.filter(pk__in=winners).order_by('-id')
    prevDate = "1970-01-01"
    count = 0
    for item in items:
        prevDate = item.prepare(prevDate)
        item.theme = themes[count]
        count += 1

    data["items"] = items

    return render(request, "winners.html", data)

def test(request, page=1):
    from django import VERSION
    return HttpResponse("V"+str(VERSION))
