# Generated by Django 2.1.3 on 2018-11-09 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monsterapi', '0006_auto_20181109_0931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monster',
            old_name='book_id',
            new_name='book',
        ),
    ]