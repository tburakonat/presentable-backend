from django.contrib import admin
from . import models

admin.site.register(models.Course)
admin.site.register(models.Presentation)
admin.site.register(models.Feedback)
admin.site.register(models.FeedbackComment)
