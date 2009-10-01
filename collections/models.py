from django.db import models
from datetime import datetime
from muaccounts.models import MUAccount

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
    slug = models.SlugField('url-friendly name', unique=True)
    description = models.TextField()
    api = models.ForeignKey(SearchApi, verbose_name = 'api')

    def __unicode__(self):
        return self.name

class Pack(models.Model):
    """Channel group, marketing thing"""
    name = models.CharField('name', max_length=255)
    slug = models.SlugField('url-friendly name', unique=True)
    description = models.TextField()
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
    pack = models.ForeignKey(Pack, related_name='trackers')
    startdate = models.DateTimeField('start date')
    laststarted = models.DateTimeField('last started date')
    is_public = models.BooleanField('is public')
    muaccounts = models.ManyToManyField(MUAccount, related_name='trackers')
#    muaccount = models.ForeignKey(MUAccount, null=True, black=True, related_name='trackers')
    counter = models.PositiveIntegerField('run counter')

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
            api = globals()[channel.api.search_model]()
            result = api.raw_fetch(self.query)
            print result
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

class BaseSearch:
    # override it for custom fetch
    def raw_fetch(self, query):
        pass

    # override it for custom result parsing 
    def get_result(self, response):
        pass

    # public method, don't override it in child classes, do it with raw_fetch instead
    def fetch(self, query):
        response = self.raw_fetch(query)
        return self.get_result(response)

import settings
import yahoo.yql
import yahoo.application
class YqlSearch(BaseSearch):
    def raw_fetch(self, query, oauth=False):
        if oauth:
            oauthapp = yahoo.application.OAuthApplication(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.APPLICATION_ID, settings.CALLBACK_URL)
            request_token = oauthapp.get_request_token()
            redirect_url  = oauthapp.get_authorization_url(request_token, settings.CALLBACK_URL)
            access_token  = oauthapp.get_access_token(request_token)
            oauthapp.token = access_token
            response = oauthapp.yql(query)
        else:
            response = yahoo.yql.YQLQuery().execute(query)
        return response

    def get_result(self, response):
        res = dict()
        if 'query' in response and 'results' in response['query']:
            res.update({'yql':response['query']['results']})
        elif 'error' in response:
            res.update({'errors':('YQL query failed with error: "%s".' % response['error']['description'],)})
        else:
            res.update({'errors':('YQL response malformed.',)})
        return res

import twython
from xml.sax.saxutils import unescape
class TwitterSearch(BaseSearch):
    def raw_fetch(source, type=TwitSource.TERM, rpp=30):
        twitter = twython.setup()
        if type == TwitSource.TERM:
          #for terms
          response = twitter.searchTwitter(source.name, rpp)
          if 'results' in response:
            for result in response['results']:
              result['source'] = unescape(result['source'])
              result['text'] = unescape(result['text'])
        elif type == TwitSource.USER:
          #for users
          response = twitter.getUserTimeline(screen_name=source.name, count=rpp)
        return response

    def get_result(self, response):
        res = dict()
        if 'results' in response:
            res.update({'twitter':response['results'],})
        else:
            res.update({'twitter':response,})
        return res

import django_pipes as pipes
class PipeSearch(BaseSearch, pipes.Pipe):
    uri = ''
    cache_expiry = 3000000000

    def init_options(self):
        self.options = dict()

    def set_query(self, query):
        pass

    def set_count(self, count=10):
        pass

    def set_offset(self, offset=0):
        pass

    def set_market(self, market=''):
        pass

    def set_version(self, version=''):
        pass

    def set_adult(self, adult=''):
        pass

    def raw_fetch(self, query, count=None, offset=None, market=None, version=None, adult=None):
        self.set_query(query)
        if count:
            self.set_count(count)
        if offset:
            self.set_offset(offset)
        if market:
            self.set_market(market)
        if version:
            self.set_version(version)
        if adult:
            self.set_adult(adult)

        return self.fetch_with_options(self.options)

    def fetch_with_options(self, options):
        resp = self.objects.get(options)
        if resp:
            return resp
        return None

class GoogleSearch(PipeSearch):
    uri = "http://ajax.googleapis.com/ajax/services/search/web"

    def init_options(self):
        super(GoogleSearch, self).init_options()
        self.options.update({'v':1.0})
    
    def set_query(self, query):
        self.options.update({'q':query})

    def get_result(self, response):
        res = dict()
        if response and hasattr(response, "responseData") and hasattr(response.responseData, "results"):
            res.update({'google':response.responseData.results,})
        return res

#class TwitterSearch(PipeSearch):
#    uri = "http://search.twitter.com/search.json"
#    cache_expiry = 300000
#
#    def set_query(self, query):
#        self.options.update({'q':query})
#
#    def get_result(self, response):
#        res = dict()
#        if response and hasattr(response, "results"):
#            res.update({'twitter':response.results,})
#        return res

class BingMultiple(PipeSearch):
    uri = "http://api.bing.net/json.aspx"

    def init_options(self):
        super(BingMultiple, self).init_options()
        self.options.update({
            'AppId':settings.APPID,
            'JsonType': 'raw',
        })
        self.set_count()
        self.set_offset()
        self.set_market()
        self.set_version()
        self.set_adult()

    def set_query(self, query):
        self.options.update({'Query':query})

    def set_market(self, market='en-US'):
        self.options.update({'Market':market})

    def set_version(self, version='2.2'):
        self.options.update({'Version':version})

    def get_result(self, response):
        if response and hasattr(response, "SearchResponse"):
            response = response.SearchResponse
        else:
            return None

        res = dict()
        if hasattr(response, "Web") and hasattr(response.Web, 'Results'):
            res.update({'web':response.Web,})
        if hasattr(response, "News") and hasattr(response.News, 'Results'):
            res.update({'news':response.News,})
        if hasattr(response, "Image") and hasattr(response.Image, 'Results'):
            res.update({'images':response.Image,})
        if hasattr(response, "Video") and hasattr(response.Video, 'Results'):
            res.update({'video':response.Video,})
        if hasattr(response, 'RelatedSearch') and hasattr(response.RelatedSearch, 'Results'):
            res.update({'related': response.RelatedSearch.Results})
        if hasattr(response, 'InstantAnswer') and hasattr(response.InstantAnswer, 'Results'):
            res.update({'related': response.InstantAnswer.Results})
        if hasattr(response, "Spell") and hasattr(response.Spell, 'Results'):
            res.update({'spell': response.Spell})
        if hasattr(response, 'Errors'):
            res.update({'errors': response.Errors})
        return res

# BingNews searches InstantAnswer
class BingInstant(BingMultiple):
    """
    resp.InstantAnswer.Results[0].keys()
[u'Url', u'ClickThroughUrl', u'ContentType', u'InstantAnswerSpecificData', u'Title']
    """

    def init_options(self):
        super(BingInstant, self).init_options()
        self.options.update({'Sources': 'InstantAnswer',})

class BingRelated(BingMultiple):
    """
    resp.RelatedSearch.Results[3].keys()
[u'Url', u'Title']
    """

    def init_options(self):
        super(BingRelated, self).init_options()
        self.options.update({'Sources': 'RelatedSearch',})

# BingNews searches news
class BingNews(BingMultiple):

    def init_options(self):
        super(BingNews, self).init_options()
        self.options.update({
            'Sources': 'News',
        })
        self.set_sortby()

    def set_count(self, count=15):
        self.options.update({'News.Count':15}) #we have to hardcode it because if count>15 Bing return error

    def set_offset(self, offset=0):
        self.options.update({'News.Offset':offset})

    def set_sortby(self, sortby='Relevance'):
        self.options.update({'News.SortBy':sortby})

class BingNewsRelated(BingNews):

    def init_options(self):
        super(BingNewsRelated, self).init_options()
        self.options.update({
            'Sources': 'News RelatedSearch',
        })

class BingNewsRelatedSpell(BingNews):

    def init_options(self):
        super(BingNewsRelatedSpell, self).init_options()
        self.options.update({
            'Sources': 'News RelatedSearch Spell',
        })

class BingWeb(BingMultiple):
    """
    resp.Web.Results[0].keys()
[u'Url', u'Title', u'DisplayUrl', u'Description', u'DateTime']

    """
      # 'Web.Options':'DisableHostCollapsing+DisableQueryAlterations',

    def init_options(self):
        super(BingWeb, self).init_options()
        self.options.update({
            'Sources':'Web',
        })

    def set_count(self, count=10):
        self.options.update({'Web.Count':count})

    def set_offset(self, offset=0):
        self.options.update({'Web.Offset':offset})

    def set_adult(self, adult='Moderate'):
        self.options.update({'Adult':adult})

class BingImage(BingWeb):

    def init_options(self):
        super(BingImage, self).init_options()
        self.options.update({
            'Sources':'Image',
        })

    def set_count(self, count=10):
        self.options.update({'Image.Count':count})

    def set_offset(self, offset=0):
        self.options.update({'Image.Offset':offset})

class BingVideo(BingWeb):
    """
    resp2.Video.keys()
[u'Total', u'Results', u'Offset']
    resp2.Video.Results[0].keys()
[u'Title', u'SourceTitle', u'StaticThumbnail', u'ClickThroughPageUrl', u'RunTime', u'PlayUrl']
    """

    def init_options(self):
        super(BingVideo, self).init_options()
        self.options.update({
            'Sources':'Video',
        })

    def set_count(self, count=10):
        self.options.update({'Video.Count':count})

    def set_offset(self, offset=0):
        self.options.update({'Video.Offset':offset})
