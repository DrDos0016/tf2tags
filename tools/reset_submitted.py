import django, os, sys
sys.path.append("/var/projects/tf2tags")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
django.setup()
from tf2tags.models import Users
Users.objects.all().update(submitted=0, posted_comments=0)
