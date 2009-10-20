from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'tracker.views.index', name='tracker_index'),
    url(r'^add/$', 'tracker.views.add', name='tracker_add'),
    url(r'^filter/(?P<tracker_id>\d+)/$', 'tracker.views.advanced_query', name='tracker_advanced_query'),
    url(r'^edit/(?P<tracker_id>\d+)/$', 'tracker.views.edit', name='tracker_edit'),
    url(r'^delete/(?P<tracker_id>\d+)/$', 'tracker.views.delete', name='tracker_delete'),
    url(r'^trends/$', 'tracker.views.index_trends', name='tracker_trend_index'),
    url(r'^trend/add/$', 'tracker.views.add_trend', name='tracker_trend_add'),
    url(r'^trend/edit/(?P<trend_id>\d+)/$', 'tracker.views.edit_trend', name='tracker_trend_edit'),
    url(r'^trend/delete/(?P<trend_id>\d+)/$', 'tracker.views.delete_trend', name='tracker_trend_delete'),
    url(r'^stats/$', 'tracker.views.stats', name='tracker_list_stats'),
    url(r'^stats/(?P<stats_id>\d+)/$', 'tracker.views.stats', name='tracker_list_stats_clicked'),
)
