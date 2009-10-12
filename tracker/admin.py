from tracker.models import Trend, Tracker, Pack, Channel, Query, RawResult, ParsedResult, TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics, Statistics
from django.contrib import admin

class StatisticsInline(admin.TabularInline):
    model = Statistics

class TrendStatisticsAdmin(admin.ModelAdmin):
    pass
#    inlines = [StatisticsInline,]

admin.site.register(Trend)
admin.site.register(Tracker)
admin.site.register(Pack)
admin.site.register(Channel)
admin.site.register(Query)
admin.site.register(RawResult)
admin.site.register(ParsedResult)
admin.site.register(TrendStatistics, TrendStatisticsAdmin)
admin.site.register(TrackerStatistics)
admin.site.register(PackStatistics)
admin.site.register(ChannelStatistics)

