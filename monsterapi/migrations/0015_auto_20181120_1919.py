# Generated by Django 2.1.3 on 2018-11-20 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monsterapi', '0014_auto_20181120_1918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='printer_id',
            new_name='printer',
        ),
    ]