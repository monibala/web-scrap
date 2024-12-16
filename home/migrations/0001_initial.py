# Generated by Django 5.1.3 on 2024-12-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedData',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('website', models.URLField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(default='NA')),
                ('query', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
