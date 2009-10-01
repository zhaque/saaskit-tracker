class BaseSearch:
    # private: 
    # override it for custom fetch
    def private_fetch(self, query):
        pass
    # private:
    # override it for custom result parsing 
    def get_result(self, response):
        pass

    # public method, don't override it in child classes, do it with private_fetch instead
    def fetch(self, query):
        response = self.private_fetch(query)
        return self.get_result(response)

import settings
import yahoo.yql
import yahoo.application
class YqlSearch(BaseSearch):
    def private_fetch(self, query, oauth=False):
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
    def private_fetch(source, type=TwitSource.TERM, rpp=30):
        twitter = twython.setup()
        if type == TwitSource.TERM:
          #for terms
          response = twitter.searchTwitter(source.name, rpp)
          if 'results' in response:
            for result in response['results']:
              result['source'] = unescape(result['source'])
              result['text'] = unescape(result['text'])
        elif type == TwitSource.USER::
          #for users
          response = twitter.getUserTimeline(screen_name=source.name, count=rpp)
        return response

    def get_result(self, response):
        res = dict()
        if 'results' in response:
            res.update({'twitter':response['results'],})
        else
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

    def private_fetch(self, query, count=None, offset=None, market=None, version=None, adult=None):
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

class TwitterSearch(PipeSearch):
    uri = "http://search.twitter.com/search.json"
    cache_expiry = 300000

    def set_query(self, query):
        self.options.update({'q':query})

    def get_result(self, response):
        res = dict()
        if response and hasattr(response, "results"):
            res.update({'twitter':response.results,})
        return res

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

