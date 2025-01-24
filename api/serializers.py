from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_field

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
    parent_comment = serializers.PrimaryKeyRelatedField(
        queryset=models.FeedbackComment.objects.all(), 
        required=False, 
        allow_null=True
    )


    class Meta:
        model = models.FeedbackComment
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'feedback',
            'parent_comment',
        )


class FeedbackCommentReadSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    feedback = serializers.PrimaryKeyRelatedField(queryset=models.Feedback.objects.all())
    parent_comment = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = models.FeedbackComment
        fields = (
            'id',
            'content',
            'created_at',
            'created_by',
            'feedback',
            'parent_comment',
            'replies',
            'is_deleted',
        )

    # Use a type hint to specify the return type of the method -- drf-spectacular will use this information to generate the OpenAPI schema.
    def get_replies(self, obj):
        replies = obj.replies.all()
        return FeedbackCommentReadSerializer(replies, many=True).data

