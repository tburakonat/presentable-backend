from django.contrib import admin
from .models import User, Course, Presentation, Feedback, FeedbackComment


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'course')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_by', 'presentation')


class FeedbackCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_by', 'feedback')


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackComment, FeedbackCommentAdmin)
