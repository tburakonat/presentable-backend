from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'courses_taught',
            'enrolled_courses',
        )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = (
            'id', 
            'name', 
            'description', 
            'teachers', 
            'students',
        )


class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Presentation
        fields = (
            'id',
            'title', 
            'description',
            'video_url',
            'video_duration',
            'created_at',
            'created_by',
            'course',
            'presentation_events',
            'transcription',
        )


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feedback
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'presentation',
        )


class FeedbackCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedbackComment
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'feedback',
        )

