from tracker.models import TwitSourceGroup, TwitSource, Buzz, Tracker, Pack, Channel, SearchApi
from django.contrib import admin

class TwitSourceGroupAdmin(admin.ModelAdmin):
  pass
class TwitSourceAdmin(admin.ModelAdmin):
  list_display = ('name', 'type')

admin.site.register(TwitSourceGroup, TwitSourceGroupAdmin)
admin.site.register(TwitSource, TwitSourceAdmin)
admin.site.register(Buzz)
admin.site.register(Tracker)
admin.site.register(Pack)
admin.site.register(Channel)
admin.site.register(SearchApi)
