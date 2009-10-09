
from south.db import db
from django.db import models
from muaccounts.models import *
from tracker.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Statistics'
        db.create_table('tracker_statistics', (
            ('id', orm['tracker.statistics:id']),
            ('daily_change', orm['tracker.statistics:daily_change']),
            ('total_today', orm['tracker.statistics:total_today']),
            ('total_this_week', orm['tracker.statistics:total_this_week']),
            ('daily_average', orm['tracker.statistics:daily_average']),
            ('latest', orm['tracker.statistics:latest']),
            ('most_active_source', orm['tracker.statistics:most_active_source']),
        ))
        db.send_create_signal('tracker', ['Statistics'])
        
        # Adding model 'PackStatistics'
        db.create_table('tracker_packstatistics', (
            ('id', orm['tracker.packstatistics:id']),
            ('created_date', orm['tracker.packstatistics:created_date']),
            ('pack', orm['tracker.packstatistics:pack']),
            ('stats', orm['tracker.packstatistics:stats']),
            ('trackerstats', orm['tracker.packstatistics:trackerstats']),
        ))
        db.send_create_signal('tracker', ['PackStatistics'])
        
        # Adding model 'ChannelStatistics'
        db.create_table('tracker_channelstatistics', (
            ('id', orm['tracker.channelstatistics:id']),
            ('created_date', orm['tracker.channelstatistics:created_date']),
            ('channel', orm['tracker.channelstatistics:channel']),
            ('stats', orm['tracker.channelstatistics:stats']),
            ('packstats', orm['tracker.channelstatistics:packstats']),
        ))
        db.send_create_signal('tracker', ['ChannelStatistics'])
        
        # Adding model 'TrackerStatistics'
        db.create_table('tracker_trackerstatistics', (
            ('id', orm['tracker.trackerstatistics:id']),
            ('created_date', orm['tracker.trackerstatistics:created_date']),
            ('tracker', orm['tracker.trackerstatistics:tracker']),
            ('stats', orm['tracker.trackerstatistics:stats']),
            ('trendstats', orm['tracker.trackerstatistics:trendstats']),
        ))
        db.send_create_signal('tracker', ['TrackerStatistics'])
        
        # Adding model 'TrendStatistics'
        db.create_table('tracker_trendstatistics', (
            ('id', orm['tracker.trendstatistics:id']),
            ('created_date', orm['tracker.trendstatistics:created_date']),
            ('trend', orm['tracker.trendstatistics:trend']),
            ('stats', orm['tracker.trendstatistics:stats']),
        ))
        db.send_create_signal('tracker', ['TrendStatistics'])
        
        # Adding field 'ParsedResult.query'
        db.add_column('tracker_parsedresult', 'query', orm['tracker.parsedresult:query'])
        
        # Adding field 'RawResult.query'
        db.add_column('tracker_rawresult', 'query', orm['tracker.rawresult:query'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Statistics'
        db.delete_table('tracker_statistics')
        
        # Deleting model 'PackStatistics'
        db.delete_table('tracker_packstatistics')
        
        # Deleting model 'ChannelStatistics'
        db.delete_table('tracker_channelstatistics')
        
        # Deleting model 'TrackerStatistics'
        db.delete_table('tracker_trackerstatistics')
        
        # Deleting model 'TrendStatistics'
        db.delete_table('tracker_trendstatistics')
        
        # Deleting field 'ParsedResult.query'
        db.delete_column('tracker_parsedresult', 'query')
        
        # Deleting field 'RawResult.query'
        db.delete_column('tracker_rawresult', 'query')
        
    
    
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
            'channel': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Channel']", 'unique': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packstats': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.PackStatistics']"}),
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Statistics']", 'unique': 'True'})
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pack': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Pack']", 'unique': 'True'}),
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Statistics']", 'unique': 'True'}),
            'trackerstats': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.TrackerStatistics']"})
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Statistics']", 'unique': 'True'}),
            'tracker': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Tracker']", 'unique': 'True'}),
            'trendstats': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.TrendStatistics']"})
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
            'stats': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Statistics']", 'unique': 'True'}),
            'trend': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Trend']", 'unique': 'True'})
        },
        'tracker.twitterresult': {
            'from_user': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'from_user_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_language_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'to_user_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['tracker']
