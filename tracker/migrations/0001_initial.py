
from south.db import db
from django.db import models
from muaccounts.models import *
from tracker.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Pack'
        db.create_table('tracker_pack', (
            ('id', orm['tracker.Pack:id']),
            ('name', orm['tracker.Pack:name']),
            ('slug', orm['tracker.Pack:slug']),
            ('description', orm['tracker.Pack:description']),
        ))
        db.send_create_signal('tracker', ['Pack'])
        
        # Adding model 'Channel'
        db.create_table('tracker_channel', (
            ('id', orm['tracker.Channel:id']),
            ('name', orm['tracker.Channel:name']),
            ('slug', orm['tracker.Channel:slug']),
            ('description', orm['tracker.Channel:description']),
            ('api', orm['tracker.Channel:api']),
        ))
        db.send_create_signal('tracker', ['Channel'])
        
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
            ('lang', orm['tracker.Tracker:lang']),
            ('location', orm['tracker.Tracker:location']),
            ('radius', orm['tracker.Tracker:radius']),
        ))
        db.send_create_signal('tracker', ['Tracker'])
        
        # Adding model 'Trend'
        db.create_table('tracker_trend', (
            ('id', orm['tracker.Trend:id']),
            ('name', orm['tracker.Trend:name']),
            ('description', orm['tracker.Trend:description']),
            ('muaccount', orm['tracker.Trend:muaccount']),
        ))
        db.send_create_signal('tracker', ['Trend'])
        
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
            ('lang', orm['tracker.ParsedResult:lang']),
            ('lon', orm['tracker.ParsedResult:lon']),
            ('lat', orm['tracker.ParsedResult:lat']),
            ('radius', orm['tracker.ParsedResult:radius']),
        ))
        db.send_create_signal('tracker', ['ParsedResult'])
        
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
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Pack'
        db.delete_table('tracker_pack')
        
        # Deleting model 'Channel'
        db.delete_table('tracker_channel')
        
        # Deleting model 'Tracker'
        db.delete_table('tracker_tracker')
        
        # Deleting model 'Trend'
        db.delete_table('tracker_trend')
        
        # Deleting model 'ParsedResult'
        db.delete_table('tracker_parsedresult')
        
        # Dropping ManyToManyField 'Pack.channels'
        db.delete_table('tracker_pack_channels')
        
        # Dropping ManyToManyField 'Tracker.packs'
        db.delete_table('tracker_tracker_packs')
        
        # Dropping ManyToManyField 'Trend.trackers'
        db.delete_table('tracker_trend_trackers')
        
        # Dropping ManyToManyField 'Pack.muaccounts'
        db.delete_table('tracker_pack_muaccounts')
        
    
    
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
        'tracker.pack': {
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Channel']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muaccounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
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
        'tracker.trend': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trends'", 'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trackers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Tracker']"})
        }
    }
    
    complete_apps = ['tracker']
