# Generated by Django 5.2 on 2025-05-18 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_recipe_meal_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='caloric_intake',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='carbs_intake',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='fat_intake',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='goal_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='protein_intake',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='weight',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
