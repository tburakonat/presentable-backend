from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
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

    def get_queryset(self):
        """
        Filter presentations for list views only.
        """
        user = self.request.user
        queryset = super().get_queryset()

        # Nur für die `list`-Aktion filtern
        if self.action == "list":
            if user.role == User.Role.STUDENT:
                return queryset.filter(created_by=user)

            if user.role == User.Role.TEACHER:
                course_id = self.request.query_params.get("course")
                if course_id:
                    return queryset.filter(
                        course_id=course_id,
                        course__in=user.courses_taught.all(),
                        is_private=False,
                    )
                return queryset.filter(course__in=user.courses_taught.all(), is_private=False)

        return queryset
    
    def get_object(self):
        """
        Fetch the object and apply additional access control checks.
        """
        obj = super().get_object()  # This retrieves the object without filtering by `get_queryset`

        user = self.request.user

        if user.role == User.Role.STUDENT and obj.created_by != user:
            raise PermissionDenied("You are not allowed to view this presentation.")

        if user.role == User.Role.TEACHER and (
            obj.course not in user.courses_taught.all() or obj.is_private
        ):
            raise PermissionDenied("You are not allowed to view this presentation.")

        return obj

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    filterset_class = FeedbackFilter

    def get_object(self):
        """
        Fetch the feedback and ensure the user has access to the related presentation.
        """
        feedback = super().get_object()
        presentation = feedback.presentation

        user = self.request.user

        # Apply the same access control as in the PresentationViewSet
        if user.role == User.Role.STUDENT and presentation.created_by != user:
            raise PermissionDenied("You are not allowed to view this feedback.")

        if user.role == User.Role.TEACHER and (
            presentation.course not in user.courses_taught.all() or presentation.is_private
        ):
            raise PermissionDenied("You are not allowed to view this feedback.")

        return feedback

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

    def get_queryset(self):
        """
        Filter comments by access control.
        """
        queryset = super().get_queryset()
        user = self.request.user

        # Ensure user has access to the related feedback's presentation
        if user.role == User.Role.STUDENT:
            queryset = queryset.filter(feedback__presentation__created_by=user)

        if user.role == User.Role.TEACHER:
            queryset = queryset.filter(
                feedback__presentation__course__in=user.courses_taught.all(),
                feedback__presentation__is_private=False
            )

        return queryset

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

