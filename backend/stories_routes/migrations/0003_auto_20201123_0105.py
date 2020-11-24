# Generated by Django 2.2 on 2020-11-23 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stories_routes', '0002_auto_20201120_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbyroute',
            name='story_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderbyroute',
            name='story_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stories_routes.OrderByRoute'),
        ),
    ]
