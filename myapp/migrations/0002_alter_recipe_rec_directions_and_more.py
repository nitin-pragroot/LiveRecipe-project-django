# Generated by Django 4.0 on 2022-01-28 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='rec_directions',
            field=models.CharField(blank='True', max_length=200, null='True'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='rec_nutfacts',
            field=models.CharField(blank='True', max_length=200, null='True'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]