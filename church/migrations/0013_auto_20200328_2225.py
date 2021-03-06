# Generated by Django 3.0.4 on 2020-03-28 22:25

import church.models
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0012_auto_20200328_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepage',
            name='bulletin',
            field=wagtail.core.fields.StreamField([('bulletin_section', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('items', wagtail.core.blocks.ListBlock(church.models.BulletinItemBlock, label='Bulletin item'))], name='Bulletin Section'))], blank=True),
        ),
    ]
