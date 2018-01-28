from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render_to_response, render
from django.shortcuts import redirect
from django.db import connection
from django.db.models import Count, Avg, Sum
from django.utils.timezone import utc
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login as auth_login
#from django_openid_auth.models import UserOpenID
#from django_openid_auth.views import parse_openid_response
from django.core.serializers.json import DjangoJSONEncoder

import urllib, json, glob, os, math, random
from tf2tags.models import *
from datetime import *
from datetime import timedelta as timedelta
from random import shuffle
import time
import tf2tags.tf2 as tf2
import hmac
import hashlib
import base64
import urllib.request

ADMINS      = ["76561197995251793", "76561198150261397"] #dr_dos0016
ADS         = True #Adsense
TRACKING    = True #Analytics

# I'd rather not put a bunch of slurs in a repo with my name, so here's a more
# complicated setup.
REV_SLURS       = ["reggin", "sreggin", "toggaf", "stoggaf", "gaf", "sgaf", "tnuc", "stnuc", "hctib", "sehctib", "regg1n", "sregg1n", "t0ggaf", "st0ggaf"]
SLURS = []
for slur in REV_SLURS:
    SLURS.append(slur[::-1])
SPYCHECK    = False # Disable anon submissions
tf = tf2.TF()

ROOT        = "/var/projects/tf2tags/"

if os.path.isfile("/var/projects/DEV"):
    URL = "http://django.pi:8000/"
else:
    URL = "http://tf2tags.com/"
