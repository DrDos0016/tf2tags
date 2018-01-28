from django.conf.urls import include, url
from django.views.static import *
from django.conf import settings

import tf2tags.views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', tf2tags.views.browse),

    url(r'^awards$', tf2tags.views.awards),
    url(r'^browse-(?P<steamID>[0-9]+)/(?P<page>[0-9]+)$', tf2tags.views.browseUser),
    url(r'^browse-(?P<steamID>[0-9]+)$', tf2tags.views.browseUser),
    url(r'^browse/(?P<page>[0-9]+)$', tf2tags.views.browse),
    url(r'^browse$', tf2tags.views.browse),
    url(r'^create$', tf2tags.views.create),
    url(r'^credits$', tf2tags.views.generic, {"template":"credits.html"}),
    url(r'^contest/(?P<theme>[0-9a-zA-Z_]+)/(?P<page>[0-9]+)$', tf2tags.views.contest),
    url(r'^contest/(?P<theme>[0-9a-zA-Z_]+)$', tf2tags.views.contest),
    url(r'^contest_rules$', tf2tags.views.generic, {"template":"contest_rules.html"}),
    url(r'^data$', tf2tags.views.generic, {"template":"data.html"}),
    url(r'^delete$', tf2tags.views.delete_comment),
    url(r'^error/(?P<type>[a-z_]+)$', tf2tags.views.error),
    url(r'^openid/login$', tf2tags.views.login),
    url(r'^logout$', tf2tags.views.logout),
    url(r'^misc$', tf2tags.views.generic, {"template":"misc.html"}),
    url(r'^modify/(?P<item>[0-9]+)$', tf2tags.views.modifyItem),
    url(r'^news$', tf2tags.views.newsArchive, {"id":"latest"}),
    url(r'^news_archive/(?P<id>[0-9]+)$', tf2tags.views.newsArchive),
    url(r'^news_archive$', tf2tags.views.newsArchive),
    url(r'^profile/(?P<steamID>[0-9]+)$', tf2tags.views.profile),
    url(r'^random$', tf2tags.views.random),
    url(r'^results$', tf2tags.views.results),
    url(r'^results/(?P<page>[0-9]+)$', tf2tags.views.results),
    url(r'^search$', tf2tags.views.generic, {"template":"search.html"}),
    url(r'^site_rules$', tf2tags.views.generic, {"template":"site_rules.html"}),
    url(r'^streak_search$', tf2tags.views.streak_search),
    url(r'^submit_comment$', tf2tags.views.submitComment),
    url(r'^submit_item$', tf2tags.views.submitItem),
    url(r'^submit_report$', tf2tags.views.submitReport),
    url(r'^top/(?P<days>[0-9]+)/(?P<page>[0-9]+)$', tf2tags.views.topItems),
    url(r'^top/(?P<page>[0-9]+)$', tf2tags.views.topItems),
    url(r'^top$', tf2tags.views.topItems),
    url(r'^view/(?P<item>[0-9]+)$', tf2tags.views.viewItem),
    url(r'^view-(?P<item>[0-9]+)$', tf2tags.views.viewItem),
    url(r'^votes/item/(?P<item>[0-9]+)$', tf2tags.views.votes_item),
    url(r'^votes/user/(?P<vote_id>[0-9]+)$', tf2tags.views.votes_user),
    url(r'^winners/(?P<year>[0-9]+)$', tf2tags.views.winners),
    url(r'^winners$', tf2tags.views.winners),


    #Misc
    url(r'^item-data$', tf2tags.views.generic, {"template":"data.html", "title":" - Item Data"}),
    url(r'^images/(?P<item>[0-9]+)$', tf2tags.views.images),


    #AJAX
    url(r'^ajax/getItems$', tf2tags.views.getItems),
    url(r'^ajax/getItem/(?P<defindex>[0-9]+)$', tf2tags.views.getItem),
    url(r'^ajax/getItem/(?P<defindex>[-0-9]+)$', tf2tags.views.getItem),
    url(r'^ajax/getAttributes$', tf2tags.views.getAttributes),
    url(r'^ajax/verify$', tf2tags.views.verify),
    url(r'^ajax/summary$', tf2tags.views.summary),
    url(r'^ajax/vote/(?P<item>[0-9]+)/(?P<vote>-?[1])$', tf2tags.views.vote),

    #OpenID
    url(r'^openid/complete/', tf2tags.views.login),

    #Admin
    url(r'^admin/contest_management', tf2tags.views.contest_management),
    url(r'^admin/miss_bomb', tf2tags.views.miss_bomb),
    url(r'^admin/postNews/(?P<id>[0-9]+)$', tf2tags.views.postNews),
    url(r'^admin/postNews', tf2tags.views.postNews),
    url(r'^admin/user_management', tf2tags.views.user_management),
    url(r'^admin/flagged', tf2tags.views.flagged),
    url(r'^admin$', tf2tags.views.admin),

    url(r'^test$', tf2tags.views.test),
]
