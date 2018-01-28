from .common import *
from .other import *


#administration
def admin(request):
    data = {"id":id}
    data["user"] = getUser(request.COOKIES.get("session", None))
    if not data["user"]["admin"]:
        return redirect("tf2tags.views.index")
    return render(request, "admin/admin.html", data)

def contest_management(request):
    data = {}
    data["user"] = getUser(request.COOKIES.get("session", None))
    if not data["user"]["admin"]:
        return redirect("tf2tags.views.index")

    if (request.POST.get("start")):
        contest = Contest(theme=request.POST.get("theme"), startDate=request.POST.get("start"), endDate=request.POST.get("end"), winner=request.POST.get("winner"))
        contest = contest.save()

    return render(request, "admin/contest_management.html", data)

def flagged(request):
    data = {}
    data["user"] = getUser(request.COOKIES.get("session", None))
    if not data["user"]["admin"]:
        return redirect("tf2tags.views.index")

    # Save changes
    if request.POST.get("id", -1) != -1:
        report = Flagged.objects.get(pk=request.POST.get("id"))
        report.handled = request.POST.get("handled", "")
        report.save()


    offset = int(request.GET.get("offset", 0))
    data["older"] = offset + 50
    data["newer"] = max(0, offset - 50)
    data["flagged"] = Flagged.objects.all().order_by("-itemID", "-timestamp")[offset:offset + 50]
    return render(request, "admin/flagged.html", data)

def postNews(request, id=None):
    data = {"id":id}
    data["user"] = getUser(request.COOKIES.get("session", None))
    if not data["user"]["admin"]:
        return redirect("tf2tags.views.index")

    if request.method == "POST":
        if id == None:
            text = request.POST.get("news", "").replace("\r\n", "<br>")
            text = text.replace("\n", "<br>")
            n = News(title=request.POST.get("title", ""), author=request.POST.get("author", ""), image=request.POST.get("image", ""), text=text)
            n.save()

            if request.POST.get("tumblr"):
                tumblr_id = post_tumblr(n.title, n.text + u"<br><br><a href='http://tf2tags.com/news_archive/"+str(n.id)+"'>View on tf2tags</a>", ["tf2tags"] + request.POST.get("tags", "").split(", "))
        else:
            print("OLD")
            #Old


    imagelist = glob.glob("/var/projects/tf2tags/assets/images/portraits/*.*")
    images = []
    for image in imagelist:
        images.append(os.path.split(image)[1])

    data["POST"] = str(request.POST)
    data["images"] = images

    if (id != None):
        data["news"] = News.objects.get(pk=int(id))
        data["news"].plain = data["news"].text.replace("<br>", "\n")

    #c = RequestContext(request, data, [ip_address_processor])
    #return HttpResponse(t.render(c))

    return render(request, "admin/postNews.html", data)

def miss_bomb(request):
    data = {}
    output = ""
    data["user"] = getUser(request.COOKIES.get("session", None))
    if not data["user"]["admin"]:
        return redirect("tf2tags.views.index")


    if request.POST.get("csrfmiddlewaretoken"):
        # Find the SteamID's owner
        bad_user = Users.objects.get(steamID=request.POST.get("steamID"))
        bad_votes = Votes.objects.filter(user_id=bad_user.id, timestamp__gte="2016-01-01 00:00:00").values("itemID")

        ids = []
        for bad_vote in bad_votes:
            id = bad_vote["itemID"]
            ids.append(id)


        # Delete those votes
        Votes.objects.filter(user_id=bad_user.id, timestamp__gte="2016-01-01 00:00:00").delete()

        print(ids)

        # Loop over all the items voted on by the missbomber
        for id in ids:
            down = 0
            up = 0

            votes = Votes.objects.filter(itemID=id)

            for vote in votes:
                if vote.vote == -1:
                    down += 1
                if vote.vote == 1:
                    up += 1

            score = up - down

            try:
                submission = Submissions.objects.get(id=id)
                output += "OLD {} W/ {} {} {}<br>".format(id, submission.upVotes, submission.downVotes, submission.score)
                submission.upVotes = up
                submission.downVotes = down
                submission.score = up - down
                submission.save()
                output += "SAVED {} W/ {} {} {}<br>".format(id, up, down, score)
            except:
                output += "COULD NOT ADJUST: " + str(id) + "<br>"

    data["output"] = output
    return render(request, "admin/miss_bomb.html", data)


def user_management(request):
    data = {}
    data["user"] = getUser(request.COOKIES.get("session", None))
    if not data["user"]["admin"]:
        return redirect("tf2tags.views.index")

    submission_offset = int(request.GET.get("submission_offset", 0))
    comment_offset = int(request.GET.get("comment_offset", 0))

    data["submission_older"] = submission_offset + 20
    data["submission_newer"] = max(0, submission_offset - 20)
    data["comment_older"] = comment_offset + 20
    data["comment_newer"] = max(0, comment_offset - 20)

    action = request.POST.get("action")
    if action == "delete_submissions":
        delete = request.POST.getlist("delete")
        for item in delete:
            tf2.deleteItem(item)

    if action == "delete_comments":
        delete = request.POST.getlist("delete")
        for comment in delete:
            c = Comments.objects.get(pk=int(comment))
            c.delete()

    if action == "ban_user":
        ban_ip = request.POST.get("ip", "")
        if not ban_ip:
            ban_ip = "192.168.0.69"
        ban = Bans(ip=ban_ip, steamID=request.POST.get("steamID"), notes=request.POST.get("notes"), begins=request.POST.get("begins"), ends=request.POST.get("ends"))
        ban.save()

    if request.GET.get("item"):
        data["lookup"] = True
        item = Submissions.objects.get(pk=request.GET["item"])
        data["target"] = item.user

        data["items"] = Submissions.objects.filter(user__steamID=item.user.steamID).order_by('-id')[submission_offset:submission_offset + 20]
        data["comments"] = Comments.objects.filter(user__steamID=item.user.steamID).order_by('-id')[comment_offset:comment_offset + 20]
    elif request.GET.get("steam_id"):
        data["lookup"] = True
        data["target"] = Users.objects.get(steamID=request.GET.get("steam_id"))
        data["items"] = Submissions.objects.filter(user__steamID=request.GET.get("steam_id")).order_by('-id')[submission_offset:submission_offset + 20]
        data["comments"] = Comments.objects.filter(user__steamID=request.GET.get("steam_id")).order_by('-id')[comment_offset:comment_offset + 20]
    else:
        data["lookup"] = False

    return render(request, "admin/user_management.html", data)
