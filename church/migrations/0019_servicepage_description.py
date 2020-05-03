# Generated by Django 3.0.4 on 2020-04-19 03:57

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0018_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, default="Please join us for our Sunday service as we worship and listen to God's word."),
        ),
    ]