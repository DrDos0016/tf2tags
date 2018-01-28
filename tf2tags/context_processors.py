# coding=utf-8
from tf2tags.models import Users
from tf2tags.common import ADMINS

def get_session(request):
    session = request.COOKIES.get("session")
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
    return {"user":user}