
from south.db import db
from django.db import models
from muaccounts.models import *
from tracker.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TrackerStatistics'
        db.create_table('tracker_trackerstatistics', (
            ('id', orm['tracker.TrackerStatistics:id']),
            ('created_date', orm['tracker.TrackerStatistics:created_date']),
            ('tracker', orm['tracker.TrackerStatistics:tracker']),
            ('stats', orm['tracker.TrackerStatistics:stats']),
            ('trendstats', orm['tracker.TrackerStatistics:trendstats']),
        ))
        db.send_create_signal('tracker', ['TrackerStatistics'])
        
        # Adding model 'Query'
        db.create_table('tracker_query', (
            ('id', orm['tracker.Query:id']),
            ('query', orm['tracker.Query:query']),
            ('channel', orm['tracker.Query:channel']),
            ('createddate', orm['tracker.Query:createddate']),
            ('laststarted', orm['tracker.Query:laststarted']),
        ))
        db.send_create_signal('tracker', ['Query'])
        
        # Adding model 'Trend'
        db.create_table('tracker_trend', (
            ('id', orm['tracker.Trend:id']),
            ('name', orm['tracker.Trend:name']),
            ('description', orm['tracker.Trend:description']),
            ('muaccount', orm['tracker.Trend:muaccount']),
        ))
        db.send_create_signal('tracker', ['Trend'])
        
        # Adding model 'Pack'
        db.create_table('tracker_pack', (
            ('id', orm['tracker.Pack:id']),
            ('name', orm['tracker.Pack:name']),
            ('slug', orm['tracker.Pack:slug']),
            ('description', orm['tracker.Pack:description']),
        ))
        db.send_create_signal('tracker', ['Pack'])
        
        # Adding model 'PackStatistics'
        db.create_table('tracker_packstatistics', (
            ('id', orm['tracker.PackStatistics:id']),
            ('created_date', orm['tracker.PackStatistics:created_date']),
            ('pack', orm['tracker.PackStatistics:pack']),
            ('stats', orm['tracker.PackStatistics:stats']),
            ('trackerstats', orm['tracker.PackStatistics:trackerstats']),
        ))
        db.send_create_signal('tracker', ['PackStatistics'])
        
        # Adding model 'ParsedResult'
        db.create_table('tracker_parsedresult', (
            ('id', orm['tracker.ParsedResult:id']),
            ('query', orm['tracker.ParsedResult:query']),
            ('channel', orm['tracker.ParsedResult:channel']),
            ('total', orm['tracker.ParsedResult:total']),
            ('title', orm['tracker.ParsedResult:title']),
            ('url', orm['tracker.ParsedResult:url']),
            ('text', orm['tracker.ParsedResult:text']),
            ('date', orm['tracker.ParsedResult:date']),
            ('source', orm['tracker.ParsedResult:source']),
            ('thumb', orm['tracker.ParsedResult:thumb']),
            ('createddate', orm['tracker.ParsedResult:createddate']),
            ('purgedate', orm['tracker.ParsedResult:purgedate']),
        ))
        db.send_create_signal('tracker', ['ParsedResult'])
        
        # Adding model 'TrendStatistics'
        db.create_table('tracker_trendstatistics', (
            ('id', orm['tracker.TrendStatistics:id']),
            ('created_date', orm['tracker.TrendStatistics:created_date']),
            ('trend', orm['tracker.TrendStatistics:trend']),
            ('stats', orm['tracker.TrendStatistics:stats']),
        ))
        db.send_create_signal('tracker', ['TrendStatistics'])
        
        # Adding model 'RawResult'
        db.create_table('tracker_rawresult', (
            ('id', orm['tracker.RawResult:id']),
            ('query', orm['tracker.RawResult:query']),
            ('result', orm['tracker.RawResult:result']),
            ('channel', orm['tracker.RawResult:channel']),
            ('createddate', orm['tracker.RawResult:createddate']),
        ))
        db.send_create_signal('tracker', ['RawResult'])
        
        # Adding model 'ChannelStatistics'
        db.create_table('tracker_channelstatistics', (
            ('id', orm['tracker.ChannelStatistics:id']),
            ('created_date', orm['tracker.ChannelStatistics:created_date']),
            ('channel', orm['tracker.ChannelStatistics:channel']),
            ('stats', orm['tracker.ChannelStatistics:stats']),
            ('packstats', orm['tracker.ChannelStatistics:packstats']),
        ))
        db.send_create_signal('tracker', ['ChannelStatistics'])
        
        # Adding model 'Channel'
        db.create_table('tracker_channel', (
            ('id', orm['tracker.Channel:id']),
            ('name', orm['tracker.Channel:name']),
            ('slug', orm['tracker.Channel:slug']),
            ('description', orm['tracker.Channel:description']),
            ('api', orm['tracker.Channel:api']),
        ))
        db.send_create_signal('tracker', ['Channel'])
        
        # Adding model 'Statistics'
        db.create_table('tracker_statistics', (
            ('id', orm['tracker.Statistics:id']),
            ('daily_change', orm['tracker.Statistics:daily_change']),
            ('total_today', orm['tracker.Statistics:total_today']),
            ('total_this_week', orm['tracker.Statistics:total_this_week']),
            ('daily_average', orm['tracker.Statistics:daily_average']),
            ('latest', orm['tracker.Statistics:latest']),
            ('most_active_source', orm['tracker.Statistics:most_active_source']),
        ))
        db.send_create_signal('tracker', ['Statistics'])
        
        # Adding model 'Tracker'
        db.create_table('tracker_tracker', (
            ('id', orm['tracker.Tracker:id']),
            ('name', orm['tracker.Tracker:name']),
            ('status', orm['tracker.Tracker:status']),
            ('query', orm['tracker.Tracker:query']),
            ('startdate', orm['tracker.Tracker:startdate']),
            ('laststarted', orm['tracker.Tracker:laststarted']),
            ('is_public', orm['tracker.Tracker:is_public']),
            ('muaccount', orm['tracker.Tracker:muaccount']),
            ('counter', orm['tracker.Tracker:counter']),
            ('description', orm['tracker.Tracker:description']),
        ))
        db.send_create_signal('tracker', ['Tracker'])
        
        # Adding ManyToManyField 'Pack.channels'
        db.create_table('tracker_pack_channels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pack', models.ForeignKey(orm.Pack, null=False)),
            ('channel', models.ForeignKey(orm.Channel, null=False))
        ))
        
        # Adding ManyToManyField 'Tracker.packs'
        db.create_table('tracker_tracker_packs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tracker', models.ForeignKey(orm.Tracker, null=False)),
            ('pack', models.ForeignKey(orm.Pack, null=False))
        ))
        
        # Adding ManyToManyField 'Trend.trackers'
        db.create_table('tracker_trend_trackers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trend', models.ForeignKey(orm.Trend, null=False)),
            ('tracker', models.ForeignKey(orm.Tracker, null=False))
        ))
        
        # Adding ManyToManyField 'Pack.muaccounts'
        db.create_table('tracker_pack_muaccounts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pack', models.ForeignKey(orm.Pack, null=False)),
            ('muaccount', models.ForeignKey(orm['muaccounts.MUAccount'], null=False))
        ))
        
        # Creating unique_together for [pack, trackerstats] on PackStatistics.
        db.create_unique('tracker_packstatistics', ['pack_id', 'trackerstats_id'])
        
        # Creating unique_together for [channel, packstats] on ChannelStatistics.
        db.create_unique('tracker_channelstatistics', ['channel_id', 'packstats_id'])
        
        # Creating unique_together for [query, channel] on Query.
        db.create_unique('tracker_query', ['query', 'channel_id'])
        
        # Creating unique_together for [tracker, trendstats] on TrackerStatistics.
        db.create_unique('tracker_trackerstatistics', ['tracker_id', 'trendstats_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'TrackerStatistics'
        db.delete_table('tracker_trackerstatistics')
        
        # Deleting model 'Query'
        db.delete_table('tracker_query')
        
        # Deleting model 'Trend'
        db.delete_table('tracker_trend')
        
        # Deleting model 'Pack'
        db.delete_table('tracker_pack')
        
        # Deleting model 'PackStatistics'
        db.delete_table('tracker_packstatistics')
        
        # Deleting model 'ParsedResult'
        db.delete_table('tracker_parsedresult')
        
        # Deleting model 'TrendStatistics'
        db.delete_table('tracker_trendstatistics')
        
        # Deleting model 'RawResult'
        db.delete_table('tracker_rawresult')
        
        # Deleting model 'ChannelStatistics'
        db.delete_table('tracker_channelstatistics')
        
        # Deleting model 'Channel'
        db.delete_table('tracker_channel')
        
        # Deleting model 'Statistics'
        db.delete_table('tracker_statistics')
        
        # Deleting model 'Tracker'
        db.delete_table('tracker_tracker')
        
        # Dropping ManyToManyField 'Pack.channels'
        db.delete_table('tracker_pack_channels')
        
        # Dropping ManyToManyField 'Tracker.packs'
        db.delete_table('tracker_tracker_packs')
        
        # Dropping ManyToManyField 'Trend.trackers'
        db.delete_table('tracker_trend_trackers')
        
        # Dropping ManyToManyField 'Pack.muaccounts'
        db.delete_table('tracker_pack_muaccounts')
        
        # Deleting unique_together for [pack, trackerstats] on PackStatistics.
        db.delete_unique('tracker_packstatistics', ['pack_id', 'trackerstats_id'])
        
        # Deleting unique_together for [channel, packstats] on ChannelStatistics.
        db.delete_unique('tracker_channelstatistics', ['channel_id', 'packstats_id'])
        
        # Deleting unique_together for [query, channel] on Query.
        db.delete_unique('tracker_query', ['query', 'channel_id'])
        
        # Deleting unique_together for [tracker, trendstats] on TrackerStatistics.
        db.delete_unique('tracker_trackerstatistics', ['tracker_id', 'trendstats_id'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'muaccounts.muaccount': {
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '256', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'logo': ('RemovableImageField', [], {'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '256', 'unique': 'True', 'null': 'True'}),
            'theme': ('PickledObjectField', [], {'default': '( lambda :DEFAULT_THEME_DICT)'})
        },
        'tracker.channel': {
            'api': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
        },
        'tracker.channelstatistics': {
            'Meta': {'unique_together': "(('channel', 'packstats'),)"},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Channel']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channelstats'", 'to': "orm['tracker.PackStatistics']"}),
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'channel'", 'unique': 'True', 'null': 'True', 'to': "orm['tracker.Statistics']"})
        },
        'tracker.pack': {
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Channel']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muaccounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
        },
        'tracker.packstatistics': {
            'Meta': {'unique_together': "(('pack', 'trackerstats'),)"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Pack']"}),
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'pack'", 'unique': 'True', 'null': 'True', 'to': "orm['tracker.Statistics']"}),
            'trackerstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packstats'", 'to': "orm['tracker.TrackerStatistics']"})
        },
        'tracker.parsedresult': {
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parsed_results'", 'to': "orm['tracker.Channel']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purgedate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumb': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        },
        'tracker.query': {
            'Meta': {'unique_together': "(('query', 'channel'),)"},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'queries'", 'to': "orm['tracker.Channel']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laststarted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'tracker.rawresult': {
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'raw_results'", 'to': "orm['tracker.Channel']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'result': ('django.db.models.fields.TextField', [], {})
        },
        'tracker.statistics': {
            'daily_average': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'daily_change': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.ParsedResult']", 'null': 'True', 'blank': 'True'}),
            'most_active_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'total_this_week': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_today': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'tracker.tracker': {
            'counter': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'laststarted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'muaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackers'", 'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'packs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Pack']"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'startdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'})
        },
        'tracker.trackerstatistics': {
            'Meta': {'unique_together': "(('tracker', 'trendstats'),)"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'tracker'", 'unique': 'True', 'null': 'True', 'to': "orm['tracker.Statistics']"}),
            'tracker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Tracker']"}),
            'trendstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackerstats'", 'to': "orm['tracker.TrendStatistics']"})
        },
        'tracker.trend': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trends'", 'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trackers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Tracker']"})
        },
        'tracker.trendstatistics': {
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'trend'", 'unique': 'True', 'null': 'True', 'to': "orm['tracker.Statistics']"}),
            'trend': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Trend']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['tracker']
