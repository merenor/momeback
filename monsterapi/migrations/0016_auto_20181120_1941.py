# Generated by Django 2.1.3 on 2018-11-20 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monsterapi', '0015_auto_20181120_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_id',
            new_name='book_slug',
        ),
    ]
