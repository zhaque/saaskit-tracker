from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import CommandError
from django.core.management.base import LabelCommand
from tracker.models import Tracker, Channel, Query, RawResult, TwitterResult
from livesearch.models import *
from yql.search import *
import simplejson as json

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
            for pack in tracker.packs.all():
              for channel in pack.channels.all():
                  try:
                      q = Query.objects.get(query = tracker.query, channel=channel)
                  except ObjectDoesNotExist:
                      q = Query()
                      q.query = tracker.query
                      q.channel = channel
                      q.save()

    def fetch(self):
        queries = Query.objects.all()
        for query in queries:
            api_class = globals()[query.channel.api]
            api = api_class()
            if issubclass(api_class, PipeSearch):
                api.init_options()
            result = api.fetch(query.query)
            res = RawResult()
            res.result = json.dumps(result)
            res.channel = query.channel
            res.save()
        Query.objects.all().delete()

    def parse(self):
        raw_results = RawResult.objects.all()
        for raw_result in raw_results:
            results = json.loads(raw_result.result)
            if 'twitter' in results:
                results = results['twitter']
                for result in results:
                    tw = TwitterResult()
                    tw.iso_language_code = result['iso_language_code']
                    tw.text = result['text']
                    tw.source = result['source']
                    tw.from_user = result['from_user']
                    tw.from_user_id = result['from_user_id']
                    tw.to_user_id = result['to_user_id']
                    tw.tweet_id = result['id']
                    tw.save()
        RawResult.objects.all().delete()

    def index(self):
        pass