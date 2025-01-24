from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .filters import (
    UserFilter, 
    CourseFilter,
    PresentationFilter,
    FeedbackFilter,
    FeedbackCommentFilter,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import (
    Course, 
    User, 
    Presentation, 
    Feedback,
    FeedbackComment,
)
from .serializers import (
    CourseSerializer, 
    UserSerializer, 
    PresentationSerializer, 
    FeedbackWriteSerializer,
    FeedbackReadSerializer, 
    FeedbackCommentWriteSerializer,
    FeedbackCommentReadSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    @action(detail=False, methods=['GET'], url_path='me')
    def me(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='enrolled-courses')
    def enrolled_courses(self, request, pk=None):
        user = self.get_object()
        courses = user.enrolled_courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='taught-courses')
    def taught_courses(self, request, pk=None):
        user = self.get_object()
        taught_courses = user.courses_taught.all()
        serializer = CourseSerializer(taught_courses, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class PresentationViewSet(viewsets.ModelViewSet):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    filterset_class = PresentationFilter

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    filterset_class = FeedbackFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FeedbackWriteSerializer
        return FeedbackReadSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class FeedbackCommentViewSet(viewsets.ModelViewSet):
    queryset = FeedbackComment.objects.all()
    filterset_class = FeedbackCommentFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FeedbackCommentWriteSerializer
        return FeedbackCommentReadSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'detail': 'Comment marked as deleted'}, status=status.HTTP_204_NO_CONTENT)

