from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import datetime, timedelta
from muaccounts.models import MUAccount

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
#    api = models.ForeignKey(SearchApi, verbose_name = 'api')
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
#    DISABLED = 4
    STATUSES = (
        (PENDING,'Pending start'),
        (STARTED,'Started'),
        (FINISHED,'Finished'),
#        (DISABLED,'Disabled'),
    )
    
    name = models.CharField('name', max_length=255)
    status = models.DecimalField('status', choices = STATUSES, max_digits=1, decimal_places=0)
    query = models.CharField('query string', max_length=255)
    packs = models.ManyToManyField(Pack, related_name='trackers')
    startdate = models.DateTimeField('start date', blank=True, null=True)
    laststarted = models.DateTimeField('last started date', blank=True, null=True)
#    queries = models.ManyToManyField(Query
#    createddate = models.DateTimeField('creation date', auto_now_add=True)
    is_public = models.BooleanField('is public')
#    muaccounts = models.ManyToManyField(MUAccount, related_name='trackers')
    muaccount = models.ForeignKey(MUAccount, related_name='trackers')
    counter = models.PositiveIntegerField('run counter', default=0)
    description = models.TextField(blank=True, null=True)

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
        self.status = self.FINISHED
        self.save()

#    def disable(self):
#        self.status = self.DISABLED
#        self.save()

    def stop(self):
        self.status = self.FINISHED
        self.save()

    def do_query(self):
        for channel in self.pack.channels.all():
            api_class = globals()[channel.api]
            api = api_class()
            if issubclass(api_class, PipeSearch):
                api.init_options()
            result = api.raw_fetch(self.query)
            #save result to db

class Trend(models.Model):
    """Tracker groups"""
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True, null=True)
    trackers = models.ManyToManyField(Tracker, related_name='trends')
    muaccount = models.ForeignKey(MUAccount, related_name='trends')

    def __unicode__(self):
        return self.name

class Query(models.Model):
    """generalized query model"""
    query = models.CharField('query string', max_length=255)
    channel = models.ForeignKey(Channel, related_name='queries')
    createddate = models.DateTimeField('creation date', auto_now_add=True)
    laststarted = models.DateTimeField('last started date', blank=True, null=True)
#    nextstartdate
#    skipstarts
    
    class Meta:
        unique_together = ('query','channel')

    def __unicode__(self):
        return '%s in %s' % (self.query, self.channel)

class RawResult(models.Model):
    query = models.CharField('query string', max_length=255)
    result = models.TextField()
    channel = models.ForeignKey(Channel, related_name="raw_results")
    createddate = models.DateTimeField('creation date', auto_now_add=True)

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
        yesterday = self.count_total_mentions(datetime.now()-timedelta(days=2)) - today
        if 0 == yesterday:
            return None
        print float(today-yesterday)/yesterday*100
        return '%s' % (float(today-yesterday)/yesterday*100)
        
    def count_daily_average(self):
        start = self.get_tracker().startdate
        delta = (datetime.now() - start).days + 1
        total = self.count_total_mentions(start)
        return total/delta
        
    def count_total_7days(self):
        return self.count_total_mentions(datetime.now() - timedelta(days=7))

    def count_total_24hours(self):
        return self.count_total_mentions(datetime.now() - timedelta(days=1))

    def count_total_mentions(self, startdate):
        total = 0
        return total

class TrendStatistics(models.Model, StatisticMethods):
    created_date = models.DateTimeField('creation date', auto_now_add=True)
    trend = models.OneToOneField(Trend)
    stats = models.OneToOneField(Statistics, blank=True, null=True, related_name='trend')

    class Meta:
        verbose_name = 'trend statistics'
        verbose_name_plural = 'trends statistics'

    def __unicode__(self):
        return '%s' % self.trend

    def count_daily_average(self):
        return None

    def count_total_mentions(self, startdate):
        total = 0
        for tracker in self.trend.trackers.all():
          for pack in tracker.packs.all():
            for channel in pack.channels.all():
              total += ParsedResult.objects.filter(query=tracker.query, channel=channel, date__gte=startdate).count()
        return total
    
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

    def count_total_mentions(self, startdate):
        total = 0
        for pack in self.tracker.packs.all():
          for channel in pack.channels.all():
            total += ParsedResult.objects.filter(query=self.tracker.query, channel=channel, date__gte=startdate).count()
        return total

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

    def count_total_mentions(self, startdate):
        total = 0
        for channel in self.pack.channels.all():
          total += ParsedResult.objects.filter(query=self.get_tracker().query, channel=channel, date__gte=startdate).count()
        return total


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

    def count_total_mentions(self, startdate):
        total = ParsedResult.objects.filter(query=self.get_tracker().query, channel=self.channel, date__gte=startdate).count()
        return total

