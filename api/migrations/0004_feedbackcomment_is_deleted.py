# Generated by Django 5.1.4 on 2025-01-24 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_feedbackcomment_parent_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackcomment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
