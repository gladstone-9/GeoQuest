# Generated by Django 4.2.4 on 2023-11-11 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_quest_difficulty_quest_num_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='ratings_total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]