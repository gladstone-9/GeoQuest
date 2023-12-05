# Generated by Django 4.2.4 on 2023-11-06 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_alter_location_answer_alter_location_clue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='completed_locations',
            field=models.ManyToManyField(blank=True, related_name='completed_by', to='maps.location'),
        ),
        migrations.AddField(
            model_name='author',
            name='completed_quests',
            field=models.ManyToManyField(blank=True, related_name='completed_by', to='maps.quest'),
        ),
    ]