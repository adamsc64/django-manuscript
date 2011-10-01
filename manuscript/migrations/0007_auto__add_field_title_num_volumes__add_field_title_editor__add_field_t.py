# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Title.num_volumes'
        db.add_column('manuscript_title', 'num_volumes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Title.editor'
        db.add_column('manuscript_title', 'editor', self.gf('django.db.models.fields.CharField')(default='', max_length=70, blank=True), keep_default=False)

        # Adding field 'Title.publisher'
        db.add_column('manuscript_title', 'publisher', self.gf('django.db.models.fields.CharField')(default='', max_length=70, blank=True), keep_default=False)

        # Adding field 'Title.place_of_publication'
        db.add_column('manuscript_title', 'place_of_publication', self.gf('django.db.models.fields.CharField')(default='', max_length=70, blank=True), keep_default=False)

        # Adding field 'Title.title_page'
        db.add_column('manuscript_title', 'title_page', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='title_page_of', unique=True, null=True, to=orm['manuscript.Page']), keep_default=False)

        # Adding field 'Title.copyright_page'
        db.add_column('manuscript_title', 'copyright_page', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='copyright_page_of', unique=True, null=True, to=orm['manuscript.Page']), keep_default=False)

        # Adding field 'Title.original_publication_title'
        db.add_column('manuscript_title', 'original_publication_title', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['manuscript.Title'], unique=True, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Title.num_volumes'
        db.delete_column('manuscript_title', 'num_volumes')

        # Deleting field 'Title.editor'
        db.delete_column('manuscript_title', 'editor')

        # Deleting field 'Title.publisher'
        db.delete_column('manuscript_title', 'publisher')

        # Deleting field 'Title.place_of_publication'
        db.delete_column('manuscript_title', 'place_of_publication')

        # Deleting field 'Title.title_page'
        db.delete_column('manuscript_title', 'title_page_id')

        # Deleting field 'Title.copyright_page'
        db.delete_column('manuscript_title', 'copyright_page_id')

        # Deleting field 'Title.original_publication_title'
        db.delete_column('manuscript_title', 'original_publication_title_id')


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
        'manuscript.compositeparagraph': {
            'Meta': {'object_name': 'CompositeParagraph'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.Chapter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'pages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['manuscript.Page']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
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
            'Meta': {'ordering': "('_order',)", 'object_name': 'Paragraph'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.Chapter']"}),
            'composite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manuscript.CompositeParagraph']", 'null': 'True', 'blank': 'True'}),
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
            'copyright_page': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'copyright_page_of'", 'unique': 'True', 'null': 'True', 'to': "orm['manuscript.Page']"}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_volumes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'original_publication_title': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['manuscript.Title']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {}),
            'place_of_publication': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'publication_year': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '70', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'title_page': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'title_page_of'", 'unique': 'True', 'null': 'True', 'to': "orm['manuscript.Page']"}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['manuscript']
