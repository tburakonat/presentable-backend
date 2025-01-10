from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'role',
        )


class CourseSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True)
    students = UserSerializer(many=True)
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
    created_by = UserSerializer()
    course = CourseSerializer()
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
    created_by = UserSerializer()
    presentation = PresentationSerializer()
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
    created_by = UserSerializer()
    feedback = FeedbackSerializer()
    class Meta:
        model = models.FeedbackComment
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'feedback',
        )

