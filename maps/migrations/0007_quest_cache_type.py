# Generated by Django 4.2.4 on 2023-11-07 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_remove_author_completed_locations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='cache_type',
            field=models.CharField(choices=[('Traditional', 'Traditional'), ('Event', 'Event'), ('Virtual', 'Virtual'), ('Locationless', 'Locationless')], default='Traditional', max_length=20),
        ),
    ]