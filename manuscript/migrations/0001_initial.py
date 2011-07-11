# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Chapter'
        db.create_table('manuscript_chapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manuscript.Title'])),
            ('start_page_no', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=70, blank=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('xml_chapter_id', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('manuscript', ['Chapter'])

        # Adding model 'Page'
        db.create_table('manuscript_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manuscript.Title'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('scan', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('manuscript', ['Page'])

        # Adding unique constraint on 'Page', fields ['title', 'number']
        db.create_unique('manuscript_page', ['title_id', 'number'])

        # Adding model 'Paragraph'
        db.create_table('manuscript_paragraph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manuscript.Chapter'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manuscript.Page'])),
            ('split', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('old_page_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('manuscript', ['Paragraph'])

        # Adding model 'Title'
        db.create_table('manuscript_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manuscript.Author'])),
            ('volume', self.gf('django.db.models.fields.IntegerField')()),
            ('pages', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=70, blank=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('manuscript', ['Title'])

        # Adding model 'Author'
        db.create_table('manuscript_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('manuscript', ['Author'])

        # Adding model 'SiteCopyText'
        db.create_table('manuscript_sitecopytext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('manuscript', ['SiteCopyText'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Page', fields ['title', 'number']
        db.delete_unique('manuscript_page', ['title_id', 'number'])

        # Deleting model 'Chapter'
        db.delete_table('manuscript_chapter')

        # Deleting model 'Page'
        db.delete_table('manuscript_page')

        # Deleting model 'Paragraph'
        db.delete_table('manuscript_paragraph')

        # Deleting model 'Title'
        db.delete_table('manuscript_title')

        # Deleting model 'Author'
        db.delete_table('manuscript_author')

        # Deleting model 'SiteCopyText'
        db.delete_table('manuscript_sitecopytext')


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
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '70', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['manuscript']
