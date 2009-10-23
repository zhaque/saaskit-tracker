
from south.db import db
from django.db import models
from muaccounts.models import *
from tracker.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'BaseStatistics'
        db.create_table('tracker_basestatistics', (
            ('id', orm['tracker.basestatistics:id']),
            ('created_date', orm['tracker.basestatistics:created_date']),
        ))
        db.send_create_signal('tracker', ['BaseStatistics'])
        
        # Adding field 'Statistics.interval'
        db.add_column('tracker_statistics', 'interval', orm['tracker.statistics:interval'])
        
        # Adding field 'TrackerStatistics.basestatistics_ptr'
        db.add_column('tracker_trackerstatistics', 'basestatistics_ptr', orm['tracker.trackerstatistics:basestatistics_ptr'])
        
        # Adding field 'Statistics.owner'
        db.add_column('tracker_statistics', 'owner', orm['tracker.statistics:owner'])
        
        # Adding field 'PackStatistics.basestatistics_ptr'
        db.add_column('tracker_packstatistics', 'basestatistics_ptr', orm['tracker.packstatistics:basestatistics_ptr'])
        
        # Adding field 'ChannelStatistics.basestatistics_ptr'
        db.add_column('tracker_channelstatistics', 'basestatistics_ptr', orm['tracker.channelstatistics:basestatistics_ptr'])
        
        # Adding field 'TrendStatistics.basestatistics_ptr'
        db.add_column('tracker_trendstatistics', 'basestatistics_ptr', orm['tracker.trendstatistics:basestatistics_ptr'])
        
        # Deleting field 'TrackerStatistics.created_date'
        db.delete_column('tracker_trackerstatistics', 'created_date')
        
        # Deleting field 'PackStatistics.id'
        db.delete_column('tracker_packstatistics', 'id')
        
        # Deleting field 'TrendStatistics.id'
        db.delete_column('tracker_trendstatistics', 'id')
        
        # Deleting field 'ChannelStatistics.created_date'
        db.delete_column('tracker_channelstatistics', 'created_date')
        
        # Deleting field 'TrackerStatistics.id'
        db.delete_column('tracker_trackerstatistics', 'id')
        
        # Deleting field 'TrackerStatistics.stats'
        db.delete_column('tracker_trackerstatistics', 'stats_id')
        
        # Deleting field 'PackStatistics.created_date'
        db.delete_column('tracker_packstatistics', 'created_date')
        
        # Deleting field 'TrendStatistics.created_date'
        db.delete_column('tracker_trendstatistics', 'created_date')
        
        # Deleting field 'ChannelStatistics.id'
        db.delete_column('tracker_channelstatistics', 'id')
        
        # Deleting field 'TrendStatistics.stats'
        db.delete_column('tracker_trendstatistics', 'stats_id')
        
        # Deleting field 'ChannelStatistics.stats'
        db.delete_column('tracker_channelstatistics', 'stats_id')
        
        # Deleting field 'PackStatistics.stats'
        db.delete_column('tracker_packstatistics', 'stats_id')
        
        # Creating unique_together for [owner, interval] on Statistics.
        db.create_unique('tracker_statistics', ['owner_id', 'interval'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'BaseStatistics'
        db.delete_table('tracker_basestatistics')
        
        # Deleting field 'Statistics.interval'
        db.delete_column('tracker_statistics', 'interval')
        
        # Deleting field 'TrackerStatistics.basestatistics_ptr'
        db.delete_column('tracker_trackerstatistics', 'basestatistics_ptr_id')
        
        # Deleting field 'Statistics.owner'
        db.delete_column('tracker_statistics', 'owner_id')
        
        # Deleting field 'PackStatistics.basestatistics_ptr'
        db.delete_column('tracker_packstatistics', 'basestatistics_ptr_id')
        
        # Deleting field 'ChannelStatistics.basestatistics_ptr'
        db.delete_column('tracker_channelstatistics', 'basestatistics_ptr_id')
        
        # Deleting field 'TrendStatistics.basestatistics_ptr'
        db.delete_column('tracker_trendstatistics', 'basestatistics_ptr_id')
        
        # Adding field 'TrackerStatistics.created_date'
        db.add_column('tracker_trackerstatistics', 'created_date', orm['tracker.trackerstatistics:created_date'])
        
        # Adding field 'PackStatistics.id'
        db.add_column('tracker_packstatistics', 'id', orm['tracker.packstatistics:id'])
        
        # Adding field 'TrendStatistics.id'
        db.add_column('tracker_trendstatistics', 'id', orm['tracker.trendstatistics:id'])
        
        # Adding field 'ChannelStatistics.created_date'
        db.add_column('tracker_channelstatistics', 'created_date', orm['tracker.channelstatistics:created_date'])
        
        # Adding field 'TrackerStatistics.id'
        db.add_column('tracker_trackerstatistics', 'id', orm['tracker.trackerstatistics:id'])
        
        # Adding field 'TrackerStatistics.stats'
        db.add_column('tracker_trackerstatistics', 'stats', orm['tracker.trackerstatistics:stats'])
        
        # Adding field 'PackStatistics.created_date'
        db.add_column('tracker_packstatistics', 'created_date', orm['tracker.packstatistics:created_date'])
        
        # Adding field 'TrendStatistics.created_date'
        db.add_column('tracker_trendstatistics', 'created_date', orm['tracker.trendstatistics:created_date'])
        
        # Adding field 'ChannelStatistics.id'
        db.add_column('tracker_channelstatistics', 'id', orm['tracker.channelstatistics:id'])
        
        # Adding field 'TrendStatistics.stats'
        db.add_column('tracker_trendstatistics', 'stats', orm['tracker.trendstatistics:stats'])
        
        # Adding field 'ChannelStatistics.stats'
        db.add_column('tracker_channelstatistics', 'stats', orm['tracker.channelstatistics:stats'])
        
        # Adding field 'PackStatistics.stats'
        db.add_column('tracker_packstatistics', 'stats', orm['tracker.packstatistics:stats'])
        
        # Deleting unique_together for [owner, interval] on Statistics.
        db.delete_unique('tracker_statistics', ['owner_id', 'interval'])
        
    
    
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
        'tracker.basestatistics': {
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Channel']"}),
            'packstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channelstats'", 'to': "orm['tracker.PackStatistics']"})
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
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
            'pack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Pack']"}),
            'trackerstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packstats'", 'to': "orm['tracker.TrackerStatistics']"})
        },
        'tracker.parsedresult': {
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parsed_results'", 'to': "orm['tracker.Channel']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'purgedate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'radius': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumb': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        },
        'tracker.statistics': {
            'Meta': {'unique_together': "(('owner', 'interval'),)"},
            'daily_average': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'daily_change': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'most_active_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.BaseStatistics']"}),
            'total_24hours': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_7days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'tracker.tracker': {
            'counter': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en-US'", 'max_length': '5'}),
            'laststarted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'muaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackers'", 'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'packs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Pack']"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'radius': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'})
        },
        'tracker.trackerstatistics': {
            'Meta': {'unique_together': "(('tracker', 'trendstats'),)"},
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
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
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
            'trend': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Trend']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['tracker']
