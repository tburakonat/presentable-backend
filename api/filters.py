import django_filters
from . import models


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = models.User
        fields = {
            'id': ['exact'],
            'username': ['exact'],
            'first_name': ['exact'],
            'last_name': ['exact'],
            'email': ['exact'],
            'role': ['exact'],
        }


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = models.Course
        fields = {
            'id': ['exact'],
            'name': ['exact'],
        }


class PresentationFilter(django_filters.FilterSet):
    class Meta:
        model = models.Presentation
        fields = {
            'id': ['exact'],
            'title': ['exact'],
            'created_by': ['exact'],
            'course': ['exact'],
        }


class FeedbackFilter(django_filters.FilterSet):
    class Meta:
        model = models.Feedback
        fields = {
            'id': ['exact'],
            'content': ['icontains'],
            'created_by': ['exact'],
            'presentation': ['exact'],
        }


class FeedbackCommentFilter(django_filters.FilterSet):
    class Meta:
        model = models.FeedbackComment
        fields = {
            'id': ['exact'],
            'content': ['icontains'],
            'created_by': ['exact'],
            'feedback': ['exact'],
        }

