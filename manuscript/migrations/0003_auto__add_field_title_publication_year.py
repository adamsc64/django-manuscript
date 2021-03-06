# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Title.publication_year'
        db.add_column('manuscript_title', 'publication_year', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Title.publication_year'
        db.delete_column('manuscript_title', 'publication_year')


    models = {
        'manuscript.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'manuscript.chapter': {
            'Meta': {'object_name': 'Chapter'},
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '70', 'blank': 'True'}),
            'start_page_no': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.Title']"}),
            'xml_chapter_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'manuscript.page': {
            'Meta': {'unique_together': "(('title', 'number'),)", 'object_name': 'Page'},
            'display': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'scan': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.Title']"})
        },
        'manuscript.paragraph': {
            'Meta': {'object_name': 'Paragraph'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.Chapter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'old_page_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.Page']"}),
            'split': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'manuscript.sitecopytext': {
            'Meta': {'object_name': 'SiteCopyText'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'manuscript.title': {
            'Meta': {'object_name': 'Title'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {}),
            'publication_year': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '70', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['manuscript']
