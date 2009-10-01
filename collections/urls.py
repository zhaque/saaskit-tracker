from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^waw/$', 'tracker.views.waw', name='tweets_waw'),
#    url(r'^manage/(?P<group_id>\d+)/delete/(?P<source_id>\d+)/$', 'tweets.views.manage_groups', name='tweets_manage_delete_source'),
#    url(r'^manage/(?P<group_id>\d+)/$', 'tweets.views.manage_groups', name='tweets_manage_group'),
#    url(r'^manage/$', 'tweets.views.manage_groups', name='tweets_manage_groups'),
#    url(r'^twitsource/edit/(?P<object_id>\d+)/$', 'tweets.views.edit_twitsource', name='tweets_edit_source'),    
#    url(r'^twitsource/delete/(?P<object_id>\d+)/$', 'tweets.views.delete_twitsource', name='tweets_delete_source'),    
#    url(r'^twitgroup/delete/(?P<object_id>\d+)/$', 'tweets.views.delete_twitgroup', name='tweets_delete_group'),    
)
