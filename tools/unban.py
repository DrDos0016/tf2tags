import django, os, sys
sys.path.append("/var/projects/tf2tags")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
django.setup()

from datetime import datetime
from tf2tags.models import Bans

def main():
    now = str(datetime.now())
    Bans.objects.filter(ends__lte=now).delete()

if __name__ == "__main__":main()
