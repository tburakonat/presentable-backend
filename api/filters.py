import django_filters
from rest_framework import filters
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

# TODO: Filter the courses the user is enrolled in or teaching based on the role of the user.
# class IsEnrolledFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         print(request.user)
#         print(queryset)
#         user = request.user
#         return queryset.filter(students__in=[user])


# class IsTeachingFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         user = request.user
#         return queryset.filter(teachers__in=[user])

