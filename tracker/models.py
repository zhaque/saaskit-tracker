from django.db import models
from datetime import datetime
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
    is_public = models.BooleanField('is public')
#    muaccounts = models.ManyToManyField(MUAccount, related_name='trackers')
    muaccount = models.ForeignKey(MUAccount, related_name='trackers')
    counter = models.PositiveIntegerField('run counter', default=0)

    def __unicode__(self):
        return self.name

    def run(self):
        if self.PENDING == self.status:
            self.status = self.STARTED
            self.startdate = datetime.now()
        elif self.FINISHED == self.status:
            self. laststarted = datetime.now()
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

class Buzz(models.Model):
    """Tracker groups"""
    name = models.CharField('name', max_length=255)
    description = models.TextField('description')
    trackers = models.ManyToManyField(Tracker, related_name='buzz')

    def __unicode__(self):
        return self.name

#class SearchResult(models.Model):
#    """Tracker search result object"""
#    pass
