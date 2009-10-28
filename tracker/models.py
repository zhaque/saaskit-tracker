from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import datetime, timedelta
from muaccounts.models import MUAccount
from django.db.models import Q
import simplejson as json
import socket
from django_pipes.exceptions import ResourceNotAvailableException

from livesearch.models import *
from tracker.search import *

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
        ('FriendFeedFeedsYql', 'FriendFeed Feeds table YQL Search'),
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
    MAXCOUNT = 200
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
    location = models.CharField(max_length=255, blank=True, null=True, default='San Francisco')
    radius = models.PositiveIntegerField('Radius (miles)', max_length=255, blank=True, null=True, choices = DISTANCE, default=250)

    def __unicode__(self):
        return self.name

    def run(self):
        if self.PENDING == self.status:
            self.status = self.STARTED
            if not self.startdate:
                self.startdate = datetime.now()
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
                    if self.lang:
                        api.set_market(self.lang)
                if self.location:
                    (lon,lat) = self.location.split()
                    api.set_longitude(lon)
                    api.set_latitude(lat)
                    if self.radius:
                        api.set_radius(self.radius)
                api.set_count(count)
                api.set_offset(offset)
                try:
                    latest_result_date = ParsedResult.objects.filter(channel=channel, query=self.query).latest().date
                    if not latest_result_date:
                        latest_result_date = datetime.now() - timedelta(days=365)
                except ObjectDoesNotExist:
                    latest_result_date = datetime.now() - timedelta(days=365)
                latest_date = datetime.now()
                while self.MAXCOUNT > offset:
                    if offset >= total or latest_date < latest_result_date:
                        break
                    api.set_count(count)
                    api.set_offset(offset)
                    try:
                        result = api.fetch(self.query)
                        (total, count, latest_date) = self.parse_result(result, channel)
                        offset += count
                    except socket.timeout:
                        pass
                    except ResourceNotAvailableException:
                        pass

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
            count = len(results)
            if count:
                total = self.MAXCOUNT
            else:
                total = 0
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
        if 'friendfeed.feeds' in results:
            results = results['friendfeed.feeds']
            count = len(results)
            if count:
                total = self.MAXCOUNT
            else:
                total = 0
            for result in results:
                url = result['link']
                res = self.get_or_create_parsedres(url)
                res.channel = channel
                res.query = self.query
                res.total = total
                res.title = result['title'][:255]
                res.text = result['title'][:255]
                res.date = datetime.strptime(result['updated'], '%Y-%m-%dT%H:%M:%SZ')
                res.source = result['user']['name'] if 'user' in result else None
                res.thumb = result['service']['iconUrl'] if 'service' in result else None
                res.lang = self.lang
                if self.location:
                    res.lon = lon
                    res.lat = lat
                if self.radius:
                    res.radius = self.radius
                res.save()
                latest_date = res.date
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
