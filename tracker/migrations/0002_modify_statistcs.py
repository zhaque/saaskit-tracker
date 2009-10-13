
from south.db import db
from django.db import models
from muaccounts.models import *
from tracker.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Statistics.total_7days'
        db.add_column('tracker_statistics', 'total_7days', orm['tracker.statistics:total_7days'])
        
        # Adding field 'Statistics.total_24hours'
        db.add_column('tracker_statistics', 'total_24hours', orm['tracker.statistics:total_24hours'])
        
        # Deleting field 'Statistics.total_this_week'
        db.delete_column('tracker_statistics', 'total_this_week')
        
        # Deleting field 'Statistics.total_today'
        db.delete_column('tracker_statistics', 'total_today')
        
        # Deleting field 'Statistics.latest'
        db.delete_column('tracker_statistics', 'latest_id')
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Statistics.total_7days'
        db.delete_column('tracker_statistics', 'total_7days')
        
        # Deleting field 'Statistics.total_24hours'
        db.delete_column('tracker_statistics', 'total_24hours')
        
        # Adding field 'Statistics.total_this_week'
        db.add_column('tracker_statistics', 'total_this_week', orm['tracker.statistics:total_this_week'])
        
        # Adding field 'Statistics.total_today'
        db.add_column('tracker_statistics', 'total_today', orm['tracker.statistics:total_today'])
        
        # Adding field 'Statistics.latest'
        db.add_column('tracker_statistics', 'latest', orm['tracker.statistics:latest'])
        
    
    
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
            'most_active_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'total_24hours': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_7days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
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
