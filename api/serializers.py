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
            'is_private',
        )


class FeedbackWriteSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    presentation = serializers.PrimaryKeyRelatedField(queryset=models.Presentation.objects.all())
    class Meta:
        model = models.Feedback
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'presentation',
        )


class FeedbackReadSerializer(serializers.ModelSerializer):
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


class FeedbackCommentWriteSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    feedback = serializers.PrimaryKeyRelatedField(queryset=models.Feedback.objects.all())

    class Meta:
        model = models.FeedbackComment
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'feedback',
        )


class FeedbackCommentReadSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    feedback = FeedbackReadSerializer()

    class Meta:
        model = models.FeedbackComment
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'feedback',
        )

