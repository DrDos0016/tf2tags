#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
This script will recalculate scores after votes have been deleted.
"""

import django, os, sys
sys.path.append("/var/projects/tf2tags")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tags.settings")
django.setup()
from tf2tags.models import Votes, Submissions

to_recalculate = []

print("Recaculate scores")
print(len(to_recalculate), " submissions to recalculate")
input("Press enter to begin recalculating")

for id in to_recalculate:
    down = 0
    up = 0

    votes = Votes.objects.filter(itemID=id)

    for vote in votes:
        if vote.vote == -1:
            down += 1
        if vote.vote == 1:
            up += 1

    score = up - down
    print("Item", id, " votes:", up, "up", down, "down", score, "score")

    try:
        submission = Submissions.objects.get(id=id)
        submission.upVotes = up
        submission.downVotes = down
        submission.score = up - down
        submission.save()
    except:
        print("COULD NOT ADJUST", id)
