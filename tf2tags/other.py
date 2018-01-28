from .common import *

#Other

def banned(steamID, request):
    banned = Bans.objects.filter(Q(ip=request.META["REMOTE_ADDR"]) | Q(steamID=steamID))
    if banned:
        return True
    return False

def duplicate_check(name, desc, base):
    return Submissions.objects.filter(name=name, desc=desc, base=base).exists()

def getProfile(steamID):
    data = {}
    user = Users.objects.get(steamID=steamID)
    data["steamID"] = steamID
    data["name"] = user.name
    data["profile"] = user.profile
    data["avatar"] = user.avatar[:-4] + "_medium.jpg"
    data["submitted"] = user.submitted
    data["maxSubmitted"] = user.maxSubmitted
    data["admin"] = user.steamID in ADMINS
    data["points"] = Submissions.objects.filter(user_id=user.id).aggregate(Sum("score"))["score__sum"]
    data["submissions"] = Submissions.objects.filter(Q(set="0") | Q(slot="set"), user_id=user.id).aggregate(Count("id"))["id__count"]
    data["today"] = user.submitted
    data["max"] = user.maxSubmitted

    data["posted_comments"] = user.posted_comments
    data["max_posted_comments"] = user.max_posted_comments

    data["rank"] = tf.getRank(data["points"])
    return data

def getUser(session):
    # You'd think this would be deprecated by the context processor get_session, but haha it's not. submit comments uses it, for one
    user = {"isUser":False, "id":0, "steamID":"0", "name":"", "profile":"", "avatar":"", "avatarM":"", "avatarL":"", "submitted":0, "max_submitted":32767, "admin":False, "posted_comments":0, "max_posted_comments":0}
    if session == None:
        #return user
        data = Users.objects.filter(pk=0)
        user["isUser"] = False
    else:
        data = Users.objects.filter(session=session)
        user["isUser"] = True
    if len(data) == 1:
        user["id"] = data[0].id
        user["steamID"] = data[0].steamID
        user["name"] = data[0].name
        user["profile"] = data[0].profile
        user["avatar"] = data[0].avatar
        user["avatarM"] = data[0].avatar[:-4] + "_medium.jpg"
        user["avatarL"] = data[0].avatar[:-4] + "_full.jpg"
        user["submitted"] = data[0].submitted
        user["max_submitted"] = data[0].maxSubmitted
        user["posted_comments"] = data[0].posted_comments
        user["max_posted_comments"] = data[0].max_posted_comments

        if data[0].steamID in ADMINS:
            user["admin"] = True
    return user

def loadItems(page=1, type="browse"):
    # Get all items for whichever page
    if type == "browse":
        items = Submissions.objects.filter(Q(set="0") | Q(slot="set")).order_by("-id")[(page-1)*10:(page-1)*10+10]
    if type[:7] == "browse-":
        steamID = type[7:]
        items = Submissions.objects.filter(Q(set="0") | Q(slot="set"), user__steamID=steamID).order_by("-id")[(page-1)*10:(page-1)*10+10]
    if type == "random":
        population = range(1, Submissions.objects.count()+1)
        choices = random.sample(population, 50)
        items = Submissions.objects.filter(Q(set="0"), id__in=choices).order_by("?")[:10]
    if type[:4] == "top/":
        days = int(type[4:])
        now = datetime.utcnow().replace(tzinfo=utc)
        timediff = now - (timedelta(days=days))

        if days > 0:
            items = Submissions.objects.filter(Q(set="0") | Q(slot="set"), timestamp__gte=(timediff)).order_by("-score")[(page-1)*10:(page-1)*10+10]
        else:
            items = Submissions.objects.filter(Q(set="0") | Q(slot="set")).order_by("-score", "-id")[(page-1)*10:(page-1)*10+10]
    if type[:8] == "contest/":
        theme = type[8:].lower()

        contest = Contest.objects.filter(theme=theme)[0]
        items = Submissions.objects.filter(Q(set="0") | Q(slot="set"), keywords__contains=theme, timestamp__gte=contest.startDate, timestamp__lte=contest.endDate).order_by("-id")[(page-1)*10:(page-1)*10+10]

    prevDate = "1970-01-01"
    for item in items:
        prevDate = item.prepare(prevDate)

    #print "========== QUERY =========="
    #print items.query
    return items
