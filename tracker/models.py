from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import datetime, timedelta
from muaccounts.models import MUAccount
from django.db.models import Q
import simplejson as json

from livesearch.models import *
from yql.search import *

class Channel(models.Model):
    SEARCH_MODELS = (
        ('BingNews','Bing News'),
        ('BingWeb','Bing Web'),
        ('BingImage','Bing Image'),
        ('BingVideo','Bing Video'),
        ('TwitterSearch','Twitter Search'),
        ('GoogleSearch','Google Search'),
        ('BingNewsRelated', 'Bing News+Related'),
        ('BingNewsRelatedSpell', 'Bing News+Related+Spell'),
        ('YqlSearch', 'Yahoo Query Language Search'),
    )
    """General class for any data source, like search engines, yql tables and so on"""
    name = models.CharField('name', max_length=255)
    slug = models.SlugField('url-friendly name', unique=True)
    description = models.TextField(blank=True, null=True)
    api = models.CharField(max_length=255, choices = SEARCH_MODELS)

    def __unicode__(self):
        return self.name

class Pack(models.Model):
    """Channel group, marketing thing"""
    name = models.CharField('name', max_length=255)
    slug = models.SlugField('url-friendly name', unique=True)
    description = models.TextField(blank=True, null=True)
    channels = models.ManyToManyField(Channel, related_name='packs')
    muaccounts = models.ManyToManyField(MUAccount, related_name='packs')

    def __unicode__(self):
        return self.name

class Tracker(models.Model):
    """Query tracker, must be unique for query, may be shared between muaccounts"""
    PENDING = 1
    STARTED = 2
    FINISHED = 3
    STATUSES = (
        (PENDING,'Pending start'),
        (STARTED,'Started'),
        (FINISHED,'Finished'),
    )
    DISTANCE = (
        (5,'5'),
        (10,'10'),
        (50,'50'),
        (75,'75'),
        (150,'150'),
        (250,'250'),
    )
    MAXCOUNT = 1000
    REQUESTCOUNT = 100
    
    name = models.CharField('name', max_length=255)
    status = models.DecimalField('status', choices = STATUSES, max_digits=1, decimal_places=0)
    query = models.CharField('query string', max_length=255)
    packs = models.ManyToManyField(Pack, related_name='trackers')
    startdate = models.DateTimeField('start date', blank=True, null=True)
    laststarted = models.DateTimeField('last started date', blank=True, null=True)
    is_public = models.BooleanField('is public')
    muaccount = models.ForeignKey(MUAccount, related_name='trackers')
    counter = models.PositiveIntegerField('run counter', default=0)
    description = models.TextField(blank=True, null=True)
    lang = models.CharField(max_length=5, choices = AdvancedSearch.MARKETS, default='en-US')
    location = models.CharField(max_length=255, blank=True, null=True)
    radius = models.PositiveIntegerField('Radius (miles)', max_length=255, blank=True, null=True, choices = DISTANCE)

    def __unicode__(self):
        return self.name

    def run(self):
        if self.PENDING == self.status:
            self.status = self.STARTED
            self.startdate = datetime.now()
        elif self.FINISHED == self.status:
            self.laststarted = datetime.now()
        else:
            return
        self.save()
        self.do_query()
        self.counter += 1
        self.status = self.PENDING
        self.save()

    def start(self):
        self.status = self.PENDING
        self.save()

    def stop(self):
        self.status = self.FINISHED
        self.save()

    def do_query(self):
        for pack in self.packs.all():
            for channel in pack.channels.all():
                api_class = globals()[channel.api]
                api = api_class()
                total = self.MAXCOUNT
                count = self.REQUESTCOUNT
                offset = 0
                if issubclass(api_class, PipeSearch):
                    api.init_options()
                    api.set_count(count)
                    api.set_offset(offset)
                    if self.lang:
                        api.set_market(self.lang)
                    try:
                        latest_result_date = ParsedResult.objects.filter(channel=channel, query=self.query).latest().date
                    except ObjectDoesNotExist:
                        latest_result_date = datetime.now() - timedelta(days=365)
                    latest_date = datetime.now()
                    while self.MAXCOUNT > offset:
                        if offset >= total or latest_date < latest_result_date:
                            break
                        api.set_count(count)
                        api.set_offset(offset)
                        result = api.fetch(self.query)
                        (total, count, latest_date) = self.parse_result(result, channel)
                        offset += count
                elif issubclass(api_class, YqlSearch):
                    pass
#                    result = api.fetch(self.query)
#                    print result['yql']
#                    count = self.parse_result(result, channel)

    def get_or_create_parsedres(self, url):
        try:
            res = ParsedResult.objects.get(url=url)
        except ObjectDoesNotExist:
            res = ParsedResult()
        res.url = url
        return res

    def parse_result(self, results, channel):
        if self.location:
            (lon,lat) = self.location.split()
        count = 0
        latest_date = None
        if 'twitter' in results:
            results = results['twitter']
            total = self.MAXCOUNT
            count = len(results)
            for result in results:
                url = 'http://twitter.com/%s/statuses/%s' % (result['from_user'], result['id'])
                res = self.get_or_create_parsedres(url)
                res.query = self.query
                res.channel = channel
                res.total = total
                res.title = result['text'] 
                res.text = result['text']
#                res.date = datetime.strptime(result['created_at'], '%a, %d %b %Y %H:%M:%S %z')
                res.date = datetime.strptime(result['created_at'][:-6], '%a, %d %b %Y %H:%M:%S')
                res.source = result['from_user'] 
                res.thumb = result['profile_image_url']
                res.lang = result['iso_language_code'] if 'iso_language_code' in result else self.lang
                if self.location:
                    res.lon = lon
                    res.lat = lat
                if self.radius:
                    res.radius = self.radius
                res.save()
                latest_date = res.date
        if 'web' in results:
            total = results['web']['Total']
            results = results['web']['Results']
            count = len(results)
            for result in results:
                url = result['Url']
                res = self.get_or_create_parsedres(url)
                res.channel = channel
                res.query = self.query
                res.total = total
                res.title = result['Title'] 
                res.text = result['Description'] if 'Description' in result else None
                res.date = datetime.strptime(result['DateTime'], '%Y-%m-%dT%H:%M:%SZ')
                res.lang = self.lang
                if self.location:
                    res.lon = lon
                    res.lat = lat
                if self.radius:
                    res.radius = self.radius
                res.save()
                latest_date = res.date
        if 'news' in results:
            total = results['news']['Total']
            results = results['news']['Results']
            count = len(results)
            for result in results:
                url = result['Url']
                res = self.get_or_create_parsedres(url)
                res.channel = channel
                res.query = self.query
                res.total = total
                res.title = result['Title'] 
                res.text = result['Snippet']
                res.date = datetime.strptime(result['Date'], '%Y-%m-%dT%H:%M:%SZ')
                res.source = result['Source'] 
                res.lang = self.lang
                if self.location:
                    res.lon = lon
                    res.lat = lat
                if self.radius:
                    res.radius = self.radius
                res.save()
                latest_date = res.date
        if 'images' in results:
            total = results['images']['Total']
            results = results['images']['Results']
            count = len(results)
            for result in results:
                url = result['Url']
                res = self.get_or_create_parsedres(url)
                res.channel = channel
                res.query = self.query
                res.total = total
                res.title = result['Title']
                res.text = result['Title']
                res.thumb = result['Thumbnail']['Url']
                res.lang = self.lang
                if self.location:
                    res.lon = lon
                    res.lat = lat
                if self.radius:
                    res.radius = self.radius
                res.save()
                latest_date = datetime.now()
        if 'video' in results:
            total = results['video']['Total']
            results = results['video']['Results']
            count = len(results)
            for result in results:
                url = result['PlayUrl']
                res = self.get_or_create_parsedres(url)
                res.channel = channel
                res.query = self.query
                res.total = total
                res.title = result['Title']
                res.text = result['Title']
                res.source = result['SourceTitle'] if 'SourceTitle' in result else None
                res.thumb = result['StaticThumbnail']['Url']
                res.lang = self.lang
                if self.location:
                    res.lon = lon
                    res.lat = lat
                if self.radius:
                    res.radius = self.radius
                res.save()
                latest_date = datetime.now()
        return (int(total), count, latest_date)
    
class Trend(models.Model):
    """Tracker groups"""
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True, null=True)
    trackers = models.ManyToManyField(Tracker, related_name='trends')
    muaccount = models.ForeignKey(MUAccount, related_name='trends')

    def __unicode__(self):
        return self.name

class ParsedResult(models.Model):
    query = models.CharField('query string', max_length=255)
    channel = models.ForeignKey(Channel, related_name="parsed_results")
    total = models.PositiveIntegerField() #api total results
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    text = models.CharField(max_length=255, blank=True, null=True) #any description, snippet or text
    date = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True) #any from, source etc
    thumb = models.URLField(blank=True, null=True) #any image/video url
    createddate = models.DateTimeField('creation date', auto_now_add=True)
    purgedate = models.DateTimeField('purge date', blank=True, null=True)
    lang = models.CharField(max_length=5, choices = AdvancedSearch.MARKETS, blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    radius = models.PositiveIntegerField(max_length=255, blank=True, null=True)

    class Meta:
        get_latest_by = 'date'

# statistics is tree-like with trends as roots,
#trend1 - tracker1 - pack1 - channel1
#      \           \       \ channel2
#       \           \pack2 - channel1
#        \                 \ channel2
#         tracker2 - pack1 - channel1
#                  \       \ channel2
#                   \pack2 - channel1
#                          \ channel2

class Statistics(models.Model):
    daily_change = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_24hours = models.PositiveIntegerField(blank=True, null=True)
    total_7days = models.PositiveIntegerField(blank=True, null=True)
    daily_average = models.IntegerField(blank=True, null=True)
    most_active_source = models.CharField(max_length=255, blank=True, null=True)

    @property
    def owner(self):
      try:
        return self.trend
      except ObjectDoesNotExist:
        try:
          return self.tracker
        except ObjectDoesNotExist:
          try:
            return self.pack
          except ObjectDoesNotExist:
            try:
              return self.channel
            except ObjectDoesNotExist:
              pass
      return None
    
    def __unicode__(self):
      return '%s' % self.owner

class StatisticMethods:
    def get_tracker(self):
        pass

    def get_startdate(self):
        pass

    def count_stats(self):
        if not self.stats:
            stats = Statistics()
            stats.save()
            self.stats = stats
        self.stats.daily_change = self.count_daily_change()
        self.stats.total_24hours = self.count_total_24hours()
        self.stats.total_7days = self.count_total_7days()
        self.stats.daily_average = self.count_daily_average()
        self.stats.save()

    def count_daily_change(self):
        today = self.count_total_24hours()
        yesterday = self.count_total_mentions(datetime.now()-timedelta(days=2), datetime.now()-timedelta(days=1))
        if 0 == yesterday:
            return None
        return '%s' % (float(today-yesterday)/yesterday*100)
        
    def count_daily_average(self):
        start = self.get_tracker().startdate
        delta = (datetime.now() - start).days + 1
        total = self.count_total_mentions(start, datetime.now())
        return total/delta
        
    def count_total_7days(self):
        return self.count_total_mentions(datetime.now() - timedelta(days=7), datetime.now())

    def count_total_24hours(self):
        return self.count_total_mentions(datetime.now() - timedelta(days=1), datetime.now())

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        return total

    def get_latest(self):
        pass

class TrendStatistics(models.Model, StatisticMethods):
    created_date = models.DateTimeField('creation date', auto_now_add=True)
    trend = models.OneToOneField(Trend)
    stats = models.OneToOneField(Statistics, blank=True, null=True, related_name='trend')

    class Meta:
        verbose_name = 'trend statistics'
        verbose_name_plural = 'trends statistics'

    def __unicode__(self):
        return '%s' % self.trend

    def get_startdate(self):
        startdates = []
        for tracker in self.trend.trackers.all():
            startdates.append(tracker.startdate)
        startdate = datetime.now()
        for date in startdates:
            if startdate > date:
                startdate = date
        return startdate

    def count_daily_average(self):
        return None

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        for tracker in self.trend.trackers.all():
          for pack in tracker.packs.all():
            for channel in pack.channels.all():
              total += ParsedResult.objects.filter(query=tracker.query, channel=channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        q_list = []
        for tracker in self.trend.trackers.all():
          channels = []
          for pack in tracker.packs.all():
              channels += list(pack.channels.all())
          q_list.append(Q(query=tracker.query, channel__in=channels))
        qs = Q()
        for q in q_list:
          qs = qs | q
        latest = ParsedResult.objects.filter(qs).order_by('-date')[:20]
        return latest

class TrackerStatistics(models.Model, StatisticMethods):
    created_date = models.DateTimeField('creation date', auto_now_add=True)
    tracker = models.ForeignKey(Tracker, related_name='stats')
    stats = models.OneToOneField(Statistics, blank=True, null=True, related_name='tracker')
    trendstats = models.ForeignKey(TrendStatistics, related_name='trackerstats')

    class Meta:
        unique_together = ('tracker', 'trendstats')
        verbose_name = 'tracker statistics'
        verbose_name_plural = 'trackers statistics'

    def __unicode__(self):
        return '%s' % self.tracker

    def get_tracker(self):
        return self.tracker

    def get_startdate(self):
        return self.get_tracker().startdate

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        for pack in self.tracker.packs.all():
          for channel in pack.channels.all():
            total += ParsedResult.objects.filter(query=self.tracker.query, channel=channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        channels = []
        for pack in self.get_tracker().packs.all():
            channels += list(pack.channels.all())
        latest = ParsedResult.objects.filter(query=self.get_tracker().query, channel__in=channels).order_by('-date')[:20]
        return latest
        
class PackStatistics(models.Model, StatisticMethods):
    created_date = models.DateTimeField('creation date', auto_now_add=True)
    pack = models.ForeignKey(Pack, related_name='stats')
    stats = models.OneToOneField(Statistics, blank=True, null=True, related_name='pack')
    trackerstats = models.ForeignKey(TrackerStatistics, related_name='packstats')

    class Meta:
        unique_together = ('pack', 'trackerstats')
        verbose_name = 'pack statistics'
        verbose_name_plural = 'packs statistics'

    def __unicode__(self):
        return '%s' % self.pack

    def get_tracker(self):
        return self.trackerstats.tracker

    def get_startdate(self):
        return self.get_tracker().startdate

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        for channel in self.pack.channels.all():
          total += ParsedResult.objects.filter(query=self.get_tracker().query, channel=channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        channels = list(self.pack.channels.all())
        latest = ParsedResult.objects.filter(query=self.get_tracker().query, channel__in=channels).order_by('-date')[:20]
        return latest

class ChannelStatistics(models.Model, StatisticMethods):
    created_date = models.DateTimeField('creation date', auto_now_add=True)
    channel = models.ForeignKey(Channel, related_name='stats')
    stats = models.OneToOneField(Statistics, blank=True, null=True, related_name='channel')
    packstats = models.ForeignKey(PackStatistics, related_name='channelstats')

    class Meta:
        unique_together = ('channel', 'packstats')
        verbose_name = 'channel statistics'
        verbose_name_plural = 'channels statistics'

    def __unicode__(self):
        return '%s' % self.channel

    def get_tracker(self):
        return self.packstats.trackerstats.tracker

    def get_startdate(self):
        return self.get_tracker().startdate

    def count_total_mentions(self, startdate, finishdate):
        total = ParsedResult.objects.filter(query=self.get_tracker().query, channel=self.channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        latest = ParsedResult.objects.filter(query=self.get_tracker().query, channel=self.channel).order_by('-date')[:20]
        return latest

