# Generated by Django 5.1.3 on 2024-11-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapeddata',
            name='id',
            field=models.IntegerField(blank=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='scrapeddata',
            name='mobile',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
