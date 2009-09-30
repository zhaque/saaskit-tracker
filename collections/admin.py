from tweets.models import TwitSourceGroup, TwitSource
from django.contrib import admin

class TwitSourceGroupAdmin(admin.ModelAdmin):
  pass
class TwitSourceAdmin(admin.ModelAdmin):
  list_display = ('name', 'type')

admin.site.register(TwitSourceGroup, TwitSourceGroupAdmin)
admin.site.register(TwitSource, TwitSourceAdmin)
