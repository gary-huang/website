# Generated by Django 3.0.4 on 2020-03-28 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0010_user_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='stream_link',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]