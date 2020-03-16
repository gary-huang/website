# Generated by Django 3.0.3 on 2020-03-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0002_prayerrequest_note'),
        ('church', '0007_delete_prayerrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='prayer_requests',
            field=models.ManyToManyField(related_name='services_pages', to='prayer.PrayerRequest'),
        ),
    ]