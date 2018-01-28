# tf2tags

tf2tags was a website hosted at http://tf2tags.com from 2011-2018 intended to
let fans of Valve's _Team Fortress 2_ submit their own names/descriptions for
items in the game. It was a modest success that fell apart and went from a
website I was proud of to one I wanted to forget about.

However, its complete destruction would be unfair to the community it formed
where for better or for worse, people made some friends and lasting
relationships. Plus I can't dare bring myself to erase over 200,000 submissions.

The site was my first time working with Python and Django for web development
and there are countless instances of poor decisions, unncessary code, and
duplicating functionality that exists elsewhere in the codebase.

It is almost certainly, for both beginning and experienced programmers alike,
a very poor idea to use this repo as-is for to create a site fulfilling the same
purpose.

I am still releasing it in its current state as it would still be more helpful
than not doing so. When working with this code, you will need to make a lot of
changes such as:

* Updating paths - Many of these are hardcoded, expecting the site to reside at
/var/projects/tf2tags or /var/projects/tf2tags.com. /var/projects shows up on
its on a few times as well. As my original dev server was a raspberry pi, I used
a hostsfile entry to point http://django.pi to my pi. This is used when the site
thinks it is running a dev copy as opposed to a production environment.

* Updating credentials - I am not so dumb as to commit code with database
credentials still inside. You'll want to set them in tf2tags/settings.py. If you
intend to download the item schema from Valve's API, you'll need to get your own
API key as well for tools/update_tf2tags.py

* Updating code for more recent versions of Python - The site was originally coded for
Python 2.6, but eventually ported over to Python 3.5.2. It was also coded for a
much earlier version of Django, but for the sake of getting it ready to be made
open source, I've at least done some basic confirmation that it will work with
Django 2.0.1. I make no promises that code used isn't deprecated and about to be
removed in future versions. Also jQuery! Good lord the site is running on 1.2!!

* Identifying unused files - Whoops, there's a ton of garbage this site has
collected over the years.

* Half the admin tools half work - When you're the only staff for several years,
it's easier to just directly access the database instead of coding good tools
for admins

* Look for "TODO". I've placed it where sensitive information like credentials
or names like "Dr. Dos" showed up. There's also plenty of TODO comments that
were things I intended to do at some point.

* April Fool's Week - In tf2tags/tf2.py set APRIL to True to enable, then
reload the server. The rest is handled automatically.

* Assets - When running a Django dev server, it will serve files from /assets on
its own. On a production environment (such as Apache), you need an alias in your
virtual host entry to have Apache serve the files. It should just be
"Alias /assets/ /path/to/site/assets/"

## Requirements
* MySQL/MariaDB if importing the existing database
* Python 3.X
* Django 2.*
* Pillow

## Files of Interest

Whether you are using this repo as a base, or just to reference when creating a
new site from scratch, some files will be particularly helpful:

* tf2tags/models.py - Database structure for the main site
* schema/models.py - Database structure for TF2's own item data
* templates/create.html - Item creation process
* assets/js/create.js - Item creation process
* tools/update_tf2tags.py - Update available items and acquire images
* tools/reset_submitted.py - Reset Submission/Comment limit each day
* tools/max_submissions.py - Increase Submission/Comment limits for users
* tools/unban.py - Remove bans from database that have expired

## Files Not Included

To be respectful of Valve's rights to their own assets, some files are
deliberately not included in this repository.

* assets/fonts - Rips of the fonts used by Team Fortress 2
* assets/items - All the graphics for items. These can theoretically all be
reobtained by running tools/update_tf2tags.py, but it may be better to download
them from the current tf2tags website instead.

## The Database

An almost unmodified copy of the site's full database is included for the sake
of easier debugging. (It's much easier to verify things when you have thousands
of items and users saved.) A few changes have been made by running these two
MySQL queries:

```SQL
DELETE FROM django_session WHERE 1;
UPDATE tf2tags_users SET steamID = id, profile = "http://tf2tags.com",
session = "" WHERE 1;
```

These queries log out all users, and purposely removes links to their SteamIDs
and Steam profiles. I feel it would not be respectful to other user's privacy to
host this information in such a visible location. The site updates this
information when a user logs in so it will become accurate again once any user
visits the site again.

Since the SteamID is used as an identifier on the site for profile and author
submission pages, it's set to the database ID instead.

## Acquiring Non-Repository Files

The assets directory is public at http://tf2tags.com/assets/ (the trailing slash
is required).

A compressed tarball of the item images can be obtained at
http://tf2tags.com/assets/data/items.tar.gz

When the time comes either to close down the current site, or move from the
current site to a new site, I will be more than happy to provide a rip of the
database that is completely up to date with the same modifications as the one
included in the repository.

## A Farewell

tf2tags was fun for a little bit. Please do not contact me for help. I wish you
all the best of luck in continuing the community you made.
