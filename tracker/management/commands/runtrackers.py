from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import CommandError
from django.core.management.base import LabelCommand
from tracker.models import Trend, Tracker, Channel, Query, RawResult, ParsedResult, TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics, Statistics
from livesearch.models import *
from yql.search import *
import simplejson as json
from datetime import datetime
import pysolr
import settings

class Command(LabelCommand):
    help = 'Runs trackers.'
    args = 'inject,fetch,parse,index'
    label = 'inject,fetch,parse,index'

    INJECT = 'inject'
    FETCH = 'fetch'
    PARSE = 'parse'
    INDEX = 'index'
    
    def handle_label(self, label, **options):
        if self.INJECT == label:
            self.inject()
        elif self.FETCH == label:
            self.fetch()
        elif self.PARSE == label:
            self.parse()
        elif self.INDEX == label:
            self.index()
        else:
            print 'Valid arguments are %s' % self.args

    def inject(self):
        pending_trackers = Tracker.objects.filter(status=Tracker.PENDING)
        for tracker in pending_trackers:
            tracker.status = Tracker.STARTED
            if not tracker.startdate:
                tracker.startdate = datetime.now()
                tracker.laststarted = datetime.now()
            else:
                tracker.laststarted = datetime.now()
            tracker.save()
            for pack in tracker.packs.all():
              for channel in pack.channels.all():
                  try:
                      q = Query.objects.get(query = tracker.query, channel=channel)
                  except ObjectDoesNotExist:
                      q = Query()
                      q.query = tracker.query
                      q.channel = channel
                      q.save()
            tracker.counter += 1
            tracker.status = Tracker.FINISHED
            tracker.save()

    def fetch(self):
        queries = Query.objects.all()
        for query in queries:
            api_class = globals()[query.channel.api]
            api = api_class()
            if issubclass(api_class, PipeSearch):
                api.init_options()
            result = api.fetch(query.query)
            res = RawResult()
            res.query = query.query
            res.result = json.dumps(result)
            res.channel = query.channel
            res.save()
        Query.objects.all().delete()
        finished_trackers = Tracker.objects.filter(status=Tracker.FINISHED)
        for tracker in finished_trackers:
            tracker.status = Tracker.PENDING
            tracker.save()

    def get_or_create_parsedres(self, url):
        try:
            res = ParsedResult.objects.get(url=url)
        except ObjectDoesNotExist:
            res = ParsedResult()
        res.url = url
        return res
    

    def parse(self):
        raw_results = RawResult.objects.all()
        for raw_result in raw_results:
            results = json.loads(raw_result.result)
            if 'twitter' in results:
                results = results['twitter']
                total = len(results)
                for result in results:
                    url = 'http://twitter.com/%s/statuses/%s' % (result['from_user'], result['id'])
                    res = self.get_or_create_parsedres(url)
                    res.query = raw_result.query
                    res.channel = raw_result.channel
                    res.total = total
                    res.title = result['text'] 
                    res.text = result['text']
#                    res.date = datetime.strptime(result['created_at'], '%a, %d %b %Y %H:%M:%S %z')
                    res.date = datetime.strptime(result['created_at'][:-6], '%a, %d %b %Y %H:%M:%S')
                    res.source = result['from_user'] 
                    res.thumb = result['profile_image_url']
                    res.save()
            if 'web' in results:
                total = results['web']['Total']
                results = results['web']['Results']
                for result in results:
                    url = result['Url']
                    res = self.get_or_create_parsedres(url)
                    res.channel = raw_result.channel
                    res.query = raw_result.query
                    res.total = total
                    res.title = result['Title'] 
                    res.text = result['Description'] if 'Description' in result else None
                    res.date = datetime.strptime(result['DateTime'], '%Y-%m-%dT%H:%M:%SZ')
                    res.save()
            if 'news' in results:
                total = results['news']['Total']
                results = results['news']['Results']
                for result in results:
                    url = result['Url']
                    res = self.get_or_create_parsedres(url)
                    res.channel = raw_result.channel
                    res.query = raw_result.query
                    res.total = total
                    res.title = result['Title'] 
                    res.text = result['Snippet']
                    res.date = datetime.strptime(result['Date'], '%Y-%m-%dT%H:%M:%SZ')
                    res.source = result['Source'] 
                    res.save()
            if 'images' in results:
                total = results['images']['Total']
                results = results['images']['Results']
                for result in results:
                    url = result['Url']
                    res = self.get_or_create_parsedres(url)
                    res.channel = raw_result.channel
                    res.query = raw_result.query
                    res.total = total
                    res.title = result['Title']
                    res.text = result['Title']
                    res.thumb = result['Thumbnail']['Url']
                    res.save()
            if 'video' in results:
                total = results['video']['Total']
                results = results['video']['Results']
                for result in results:
                    url = result['PlayUrl']
                    res = self.get_or_create_parsedres(url)
                    res.channel = raw_result.channel
                    res.query = raw_result.query
                    res.total = total
                    res.title = result['Title']
                    res.text = result['Title']
                    res.source = result['SourceTitle'] if 'SourceTitle' in result else None
                    res.thumb = result['StaticThumbnail']['Url']
                    res.save()
        RawResult.objects.all().delete()

    def index(self):
        self.stats()
        self.sorl()

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
                        channel_stats.count_stats()
                        channel_stats.save()
                    pack_stats.count_stats()
                    pack_stats.save()
                tracker_stats.count_stats()
                tracker_stats.save()
            trend_stats.count_stats()
            trend_stats.save()

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
            }
            if res.date:
                map.update({'date': res.date})
            if res.createddate:
                map.update({'createddate': res.createddate})
            if res.purgedate:
                map.update({'purgedate': res.purgedate})
            docs.append(map)
        conn.add(docs)

