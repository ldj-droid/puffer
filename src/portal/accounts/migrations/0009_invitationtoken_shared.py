# Generated by Django 2.0.8 on 2018-09-17 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180816_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitationtoken',
            name='shared',
            field=models.BooleanField(default=False),
        ),
    ]