# Generated by Django 3.1 on 2022-06-26 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_reviewrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewrating',
            old_name='ratings',
            new_name='rating',
        ),
    ]