# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SiteCopyText'
        db.create_table('wyclif_sitecopytext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('wyclif', ['SiteCopyText'])


    def backwards(self, orm):
        
        # Deleting model 'SiteCopyText'
        db.delete_table('wyclif_sitecopytext')


    models = {
        'wyclif.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'wyclif.chapter': {
            'Meta': {'object_name': 'Chapter'},
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'start_page_no': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wyclif.Title']"}),
            'xml_chapter_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'wyclif.page': {
            'Meta': {'unique_together': "(('title', 'number'),)", 'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'scan': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wyclif.Title']"})
        },
        'wyclif.paragraph': {
            'Meta': {'object_name': 'Paragraph'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wyclif.Chapter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'old_page_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wyclif.Page']"}),
            'split': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'wyclif.sitecopytext': {
            'Meta': {'object_name': 'SiteCopyText'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'wyclif.title': {
            'Meta': {'object_name': 'Title'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wyclif.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '70', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['wyclif']
