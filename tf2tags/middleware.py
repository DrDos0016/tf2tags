# coding=utf-8
from tf2tags.models import Users
from tf2tags.common import ADMINS

class UserMiddleware(object):

    def process_request(self, request):
        if request.session.session_key:
            try:
                request.session.user = Users.objects.get(session=request.session.session_key)
                request.session.user.logged_in = True
            except: 
                request.user = Users()
                request.user.logged_in = False
        else:
            request.session.user = Users()
            request.session.user.logged_in = False
        return None
        