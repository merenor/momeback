# Generated by Django 2.1.3 on 2018-11-04 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monsterapi', '0002_monster_bible_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monster',
            name='name',
        ),
    ]
