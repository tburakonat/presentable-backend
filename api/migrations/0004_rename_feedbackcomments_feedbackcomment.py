# Generated by Django 5.1.4 on 2024-12-23 17:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_feedback_feedbackcomments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FeedbackComments',
            new_name='FeedbackComment',
        ),
    ]