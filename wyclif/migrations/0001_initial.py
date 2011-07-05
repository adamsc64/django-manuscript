# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Chapter'
        db.create_table('wyclif_chapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wyclif.Title'])),
            ('start_page_no', self.gf('django.db.models.fields.IntegerField')()),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('xml_chapter_id', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('wyclif', ['Chapter'])

        # Adding model 'Page'
        db.create_table('wyclif_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wyclif.Title'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('scan', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('wyclif', ['Page'])

        # Adding unique constraint on 'Page', fields ['title', 'number']
        db.create_unique('wyclif_page', ['title_id', 'number'])

        # Adding model 'Paragraph'
        db.create_table('wyclif_paragraph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wyclif.Chapter'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wyclif.Page'])),
            ('split', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('old_page_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('wyclif', ['Paragraph'])

        # Adding model 'Title'
        db.create_table('wyclif_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wyclif.Author'])),
            ('volume', self.gf('django.db.models.fields.IntegerField')()),
            ('pages', self.gf('django.db.models.fields.IntegerField')()),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('wyclif', ['Title'])

        # Adding model 'Author'
        db.create_table('wyclif_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('wyclif', ['Author'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Page', fields ['title', 'number']
        db.delete_unique('wyclif_page', ['title_id', 'number'])

        # Deleting model 'Chapter'
        db.delete_table('wyclif_chapter')

        # Deleting model 'Page'
        db.delete_table('wyclif_page')

        # Deleting model 'Paragraph'
        db.delete_table('wyclif_paragraph')

        # Deleting model 'Title'
        db.delete_table('wyclif_title')

        # Deleting model 'Author'
        db.delete_table('wyclif_author')


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
            'scan': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
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
        'wyclif.title': {
            'Meta': {'object_name': 'Title'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wyclif.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['wyclif']
