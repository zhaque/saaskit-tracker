from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import CommandError
from django.core.management.base import NoArgsCommand
from tracker.models import Trend, Tracker, Channel, ParsedResult, TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics, Statistics
from datetime import datetime, timedelta
import settings

class Command(NoArgsCommand):
    help = 'Generate valid stats data.'
    DAYS = 10
    def handle_noargs(self, **options):
        self.generate()

    def generate(self):
        now = datetime.now()
        trackers = Tracker.objects.all()
        for tracker in trackers:
            tracker.startdate = now - timedelta(days=self.DAYS)
            tracker.save()
        results = ParsedResult.objects.all()
        i=0
        for result in results:
            if i > self.DAYS:
              i=0
#            print '%d' % i
            result.date = now - timedelta(days=i)
            result.save()
#            print '%s' % result.date
            i += 1