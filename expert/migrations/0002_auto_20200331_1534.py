# Generated by Django 3.0.4 on 2020-03-31 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expert',
            old_name='url_short',
            new_name='short_url',
        ),
        migrations.RemoveField(
            model_name='expert',
            name='url',
        ),
        migrations.AddField(
            model_name='expert',
            name='long_url',
            field=models.URLField(default='', verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expert',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]