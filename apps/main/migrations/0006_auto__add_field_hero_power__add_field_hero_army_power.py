# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Hero.power'
        db.add_column('main_hero', 'power',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Hero.army_power'
        db.add_column('main_hero', 'army_power',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Hero.power'
        db.delete_column('main_hero', 'power')

        # Deleting field 'Hero.army_power'
        db.delete_column('main_hero', 'army_power')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.hero': {
            'Meta': {'object_name': 'Hero'},
            'army_power': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'attack_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'attack_own': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'attentiveness_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'attentiveness_own': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avatar_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'blog': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'charm_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'charm_own': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'defence_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'defence_own': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'experience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'followers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hireable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'html_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'public_gists': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'public_repos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'race': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'hero'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.spell': {
            'Meta': {'object_name': 'Spell'},
            'cnt': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'hero': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spells'", 'to': "orm['main.Hero']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'main.unit': {
            'Meta': {'object_name': 'Unit'},
            'attack_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'attentiveness_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'charm_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'custom_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'defence_github': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'forks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hero': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units'", 'to': "orm['main.Hero']"}),
            'html_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'open_issues': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'race': ('django.db.models.fields.CharField', [], {'default': "'human'", 'max_length': '100'}),
            'watchers': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main']