from django.db import models
from datetime import datetime
#from muaccount.models import MUAccount

class TwitSourceGroup(models.Model):
  """
  Model groups twitter sources, Every plan owner has its own list of groups
  """
  # group name
  name = models.CharField('name', max_length=255)
  slug = models.SlugField('slug')
  description = models.TextField('description', blank=True)
  # max status, default value is maximum
  max_status = models.PositiveSmallIntegerField('max status', default=100)
  # update interval in minuites, default value is a minimum
  update_interval = models.PositiveSmallIntegerField('update interval', default=30)

  # muaccount this group belongs to, groups are not reusable by others, so we use ForeignKey instead of ManyToManyField
#  account = models.ForeignKey(MUAccount, verbose_name='account')
  
  class Meta:
#    unique_together = ('name', 'account')
    ordering = ['name']
    verbose_name = 'twitter source group'
    verbose_name_plural = 'twitter source groups'

  def __unicode__(self):
    return self.name

class TwitSource(models.Model):
  """
  TwitSource model describes twitter data source, i.e. twitter user or search terms/phrases, 
  TwitSources are organized in groups and belong to payed account owner (muaccount).
  """
  USER = 1
  TERM = 2
  SOURCE_TYPES = (
    (USER, 'user'),
    (TERM, 'search term')
  )
  # source name, i.e. twitter user name or twitter search term/phrase
  name = models.CharField('name', max_length=255)
  # TwitSource may be of 2 types: user or term
  type = models.DecimalField('type', choices = SOURCE_TYPES, max_digits=1, decimal_places=0)
  # muaccount this source is connected to, if we delete TwitSource for defined muaccount, it should not disappear for others
#  accounts = models.ManyToManyField(MUAccount, verbose_name='accounts')
  # TwitSource may be in any amount of groups (TwitSourceGroup) or may be in 'uncategorized' default group if NULL
  groups = models.ManyToManyField(TwitSourceGroup, verbose_name='groups', blank=True, null=True, related_name='twit_sources')

  class Meta:
    unique_together = ('name', 'type')
    ordering = ['name']
    verbose_name = 'twitter source'
    verbose_name_plural = 'twitter sources'

  def __unicode__(self):
    return self.name

#------------------- Channel staff -----

class SearchApi(models.Model):
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
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    muaccount = models.ManyToManyField(MUAccount, blank=True, null=True, related_name='searchapis')
    search_model = models.CharField(max_length=255, choices = SEARCH_MODELS)

    def __unicode__(self):
        return self.name

class Channel(models.Model):
    """General class for any data source, like search engines, yql tables and so on"""
    name = models.CharField('name', max_length=255)
    slug = models.SlugFields('url-friendly name', unique=True)
    description = models.TextField()
    api = models.ForeignKey(SearchApi, verbose_name = 'api')

class Pack(models.Model):
    """Channel group, marketing thing"""
    name = models.CharField('name', max_length=255)
    slug = models.SlugFields('url-friendly name', unique=True)
    description = models.TextField()
    channels = models.ManyToManyField(Channel, related_name='packs')

class Tracker(models.Model):
    """Query tracker, must be unique for query, may be shared between muaccounts"""
    PENDING = 1
    STARTED = 2
    FINISHED = 3
    DISABLED = 4
    STATUSES = (
        (PENDING,'Pending start'),
        (STARTED,'Started'),
        (FINISHED,'Finished'),
        (DISABLED,'Disabled'),
    )
    
    name = models.CharField('name', max_length=255)
    status = models.DecimalField('status', choices = STATUSES, max_digits=1, decimal_places=0)
    query = models.CharField('query string', max_length=255)
    pack = models.ForeignKey(Pack, related_name='trackers')
    startdate = models.DateTimeField('start date')
    laststarted = models.DateTimeField('last started date')
    is_public = models.BooleanField('is public')
    muaccounts = models.ManyToManyField(MUAccount, related_name='trackers')
#    muaccount = models.ForeignKey(MUAccount, null=True, black=True, related_name='trackers')

    def start(self):
        if self.PENDING == self.status:
            self.status = self.STARTED
            self.startdate = datetime.now()
        elif self.STARTED == self.status:
            self. laststarted = datetime.now()
        self.save()
        #do some query staff

    def disable(self):
        self.status = self.DISABLED
        self.save()

    def stop(self):
        self.status = self.FINISHED
        self.save()

class Buzz(models.Model):
    """Tracker groups"""
    name = models.CharField('name', max_length=255)
    description = models.TextField('description')
    trackers = models.ManyToManyField(Tracker, related_name='buzz')

class SearchResult(models.Model):
    """Tracker search result object"""
    pass
