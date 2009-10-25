from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import CommandError
from django.core.management.base import LabelCommand
from tracker.models import Tracker, Trend, Pack, Channel, ParsedResult
from stats.models import BaseStatistics, Statistics, TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics
from livesearch.models import *
from yql.search import *
import simplejson as json
from datetime import datetime
import pysolr
import settings

class Command(LabelCommand):
    help = 'Runs trackers.'
    args = 'fetch,stats,index'
    label = 'fetch,stats,index'

    FETCH = 'fetch'
    STATS = 'stats'
    INDEX = 'index'
    
    def handle_label(self, label, **options):
        if self.FETCH == label:
            self.fetch()
        elif self.STATS == label:
            self.stats()
        elif self.INDEX == label:
            self.sorl()
        else:
            print 'Valid arguments are %s' % self.args

    def fetch(self):
        pending_trackers = Tracker.objects.filter(status=Tracker.PENDING)
        for tracker in pending_trackers:
            tracker.run()

    def stats(self):
        trends = Trend.objects.all()
        for trend in trends:
            try:
                trend_stats = TrendStatistics.objects.get(trend = trend)
            except ObjectDoesNotExist:
                trend_stats = TrendStatistics()
                trend_stats.trend = trend
                trend_stats.save()
            trackers = trend.trackers.all()
            for tracker in trackers:
                try:
                    tracker_stats = TrackerStatistics.objects.get(tracker = tracker, trendstats = trend_stats)
                except ObjectDoesNotExist:
                    tracker_stats = TrackerStatistics()
                    tracker_stats.tracker = tracker
                    tracker_stats.trendstats = trend_stats
                    tracker_stats.save()
                packs = tracker.packs.all()
                for pack in packs:
                    try:
                        pack_stats = PackStatistics.objects.get(pack = pack, trackerstats = tracker_stats)
                    except ObjectDoesNotExist:
                        pack_stats = PackStatistics()
                        pack_stats.pack = pack
                        pack_stats.trackerstats = tracker_stats
                        pack_stats.save()
                    channels = pack.channels.all()
                    for channel in channels:
                        try:
                            channel_stats = ChannelStatistics.objects.get(channel = channel, packstats = pack_stats)
                        except ObjectDoesNotExist:
                            channel_stats = ChannelStatistics()
                            channel_stats.channel = channel
                            channel_stats.packstats = pack_stats
                            channel_stats.save()
                        channel_stats.count_stats()
                    pack_stats.count_stats()
                tracker_stats.count_stats()
            trend_stats.count_stats()

    def sorl(self):
        results = ParsedResult.objects.all()
        conn = pysolr.Solr(settings.SOLR_URL)
        docs = []
        for res in results:
            packs = []
            trackers = []
            trends = []
            for pack in res.channel.packs.all():
                packs.append(pack.name)
                for tracker in pack.trackers.all():
                    if tracker.query == res.query:
                        trackers.append(tracker.name)
                        for trend in tracker.trends.all():
                            trends.append(trend.name)
            map = {
              'url': res.url,
              'query': res.query,
              'channel': res.channel.name,
              'packs': packs,
              'tracker': trackers,
              'trends': trends,
              'total': res.total,
              'title': res.title if res.title else '',
              'text': res.text if res.text else '',
              'source': res.source if res.source else '',
              'thumb': res.thumb if res.thumb else '',
              'lang': res.lang if res.lang else '',
            }
            if res.date:
                map.update({'date': res.date})
            if res.createddate:
                map.update({'createddate': res.createddate})
            if res.purgedate:
                map.update({'purgedate': res.purgedate})
            if res.lon:
                map.update({'lon': res.lon})
            if res.lat:
                map.update({'lat': res.lat})
            if res.radius:
                map.update({'radius': res.radius})
            docs.append(map)
        conn.add(docs)

